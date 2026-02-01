"""
Agent Evaluation Module
Measures and tracks agent performance metrics.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json
from pathlib import Path


class AgentEvaluator:
    """Evaluates agent performance across multiple dimensions."""
    
    def __init__(self):
        self.metrics = {
            "total_tasks": 0,
            "successful_tasks": 0,
            "failed_tasks": 0,
            "tools_used": {},
            "average_reasoning_steps": 0,
            "reflections_performed": 0,
            "task_history": []
        }
    
    def evaluate_task_execution(
        self,
        task: str,
        result: Dict[str, Any],
        reasoning_steps: int,
        tools_used: List[str],
        reflection: Optional[Dict] = None
    ) -> Dict[str, float]:
        """
        Evaluate a single task execution.
        
        Args:
            task: The task description
            result: Task execution result
            reasoning_steps: Number of reasoning steps taken
            tools_used: List of tools used
            reflection: Reflection on the task
            
        Returns:
            Dictionary of evaluation scores
        """
        scores = {}
        
        # Success rate
        success = result.get("success", False)
        scores["success"] = 1.0 if success else 0.0
        
        # Efficiency (fewer reasoning steps is more efficient, normalize to 0-1)
        # Assume optimal is 1-5 steps
        scores["efficiency"] = max(0.0, min(1.0, 1.0 - (reasoning_steps - 1) / 10))
        
        # Tool usage appropriateness
        # This is a simple heuristic - could be made more sophisticated
        scores["tool_usage"] = min(1.0, len(tools_used) / 3.0) if tools_used else 0.0
        
        # Reflection quality (if reflection was performed)
        if reflection:
            scores["reflection_quality"] = self._evaluate_reflection(reflection)
        else:
            scores["reflection_quality"] = 0.0
        
        # Overall score (weighted average)
        weights = {
            "success": 0.4,
            "efficiency": 0.2,
            "tool_usage": 0.2,
            "reflection_quality": 0.2
        }
        
        scores["overall"] = sum(scores[k] * weights[k] for k in weights.keys())
        
        # Update metrics
        self._update_metrics(task, success, reasoning_steps, tools_used, reflection is not None)
        
        # Record task
        self.metrics["task_history"].append({
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "success": success,
            "scores": scores,
            "tools_used": tools_used
        })
        
        return scores
    
    def _evaluate_reflection(self, reflection: Dict) -> float:
        """Evaluate the quality of a reflection."""
        score = 0.0
        
        # Check if reflection identified success/failure correctly
        if "success" in reflection:
            score += 0.2
        
        # Check if analysis was provided
        if reflection.get("analysis"):
            score += 0.3
        
        # Check if next steps were identified
        if reflection.get("next_steps"):
            score += 0.3
        
        # Check if alternatives were considered for failures
        if not reflection.get("success", True) and reflection.get("alternative_approach"):
            score += 0.2
        
        return score
    
    def _update_metrics(
        self,
        task: str,
        success: bool,
        reasoning_steps: int,
        tools_used: List[str],
        reflected: bool
    ):
        """Update running metrics."""
        self.metrics["total_tasks"] += 1
        
        if success:
            self.metrics["successful_tasks"] += 1
        else:
            self.metrics["failed_tasks"] += 1
        
        # Update average reasoning steps
        total = self.metrics["total_tasks"]
        current_avg = self.metrics["average_reasoning_steps"]
        self.metrics["average_reasoning_steps"] = (
            (current_avg * (total - 1) + reasoning_steps) / total
        )
        
        # Track tool usage
        for tool in tools_used:
            self.metrics["tools_used"][tool] = self.metrics["tools_used"].get(tool, 0) + 1
        
        if reflected:
            self.metrics["reflections_performed"] += 1
    
    def evaluate_answer_quality(
        self,
        question: str,
        answer: str,
        expected_keywords: Optional[List[str]] = None,
        sources_used: Optional[List[Dict]] = None
    ) -> Dict[str, float]:
        """
        Evaluate the quality of a generated answer.
        
        Args:
            question: The original question
            answer: Generated answer
            expected_keywords: Optional keywords that should appear
            sources_used: Optional list of sources with relevance scores
            
        Returns:
            Quality scores
        """
        scores = {}
        
        # Completeness (based on answer length - simple heuristic)
        word_count = len(answer.split())
        if word_count < 20:
            scores["completeness"] = 0.3
        elif word_count < 50:
            scores["completeness"] = 0.6
        elif word_count < 100:
            scores["completeness"] = 0.8
        else:
            scores["completeness"] = 1.0
        
        # Relevance (keyword matching if provided)
        if expected_keywords:
            answer_lower = answer.lower()
            matches = sum(1 for kw in expected_keywords if kw.lower() in answer_lower)
            scores["relevance"] = matches / len(expected_keywords)
        else:
            scores["relevance"] = 0.8  # Default assumption
        
        # Source quality (if sources provided)
        if sources_used:
            avg_relevance = sum(s.get("relevance", 0.5) for s in sources_used) / len(sources_used)
            scores["source_quality"] = avg_relevance
        else:
            scores["source_quality"] = 0.5
        
        # Clarity (simple heuristic based on sentence structure)
        sentences = answer.count('.') + answer.count('!') + answer.count('?')
        avg_sentence_length = word_count / max(sentences, 1)
        # Optimal sentence length is 15-25 words
        if 15 <= avg_sentence_length <= 25:
            scores["clarity"] = 1.0
        else:
            scores["clarity"] = max(0.5, 1.0 - abs(avg_sentence_length - 20) / 20)
        
        # Overall quality
        scores["overall"] = (
            scores["completeness"] * 0.3 +
            scores["relevance"] * 0.3 +
            scores["source_quality"] * 0.2 +
            scores["clarity"] * 0.2
        )
        
        return scores
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get overall performance summary."""
        success_rate = (
            self.metrics["successful_tasks"] / self.metrics["total_tasks"]
            if self.metrics["total_tasks"] > 0 else 0.0
        )
        
        reflection_rate = (
            self.metrics["reflections_performed"] / self.metrics["total_tasks"]
            if self.metrics["total_tasks"] > 0 else 0.0
        )
        
        # Calculate average scores from task history
        if self.metrics["task_history"]:
            avg_scores = {}
            for key in ["overall", "efficiency", "tool_usage", "reflection_quality"]:
                scores = [t["scores"].get(key, 0) for t in self.metrics["task_history"]]
                avg_scores[key] = sum(scores) / len(scores) if scores else 0.0
        else:
            avg_scores = {
                "overall": 0.0,
                "efficiency": 0.0,
                "tool_usage": 0.0,
                "reflection_quality": 0.0
            }
        
        return {
            "total_tasks": self.metrics["total_tasks"],
            "success_rate": success_rate,
            "reflection_rate": reflection_rate,
            "average_reasoning_steps": round(self.metrics["average_reasoning_steps"], 2),
            "average_scores": avg_scores,
            "tools_usage_count": self.metrics["tools_used"],
            "most_used_tool": max(
                self.metrics["tools_used"].items(),
                key=lambda x: x[1],
                default=("none", 0)
            )[0]
        }
    
    def save_evaluation_report(self, filepath: Optional[str] = None):
        """Save evaluation report to file."""
        if filepath is None:
            output_dir = Path(__file__).parent.parent / "logs"
            output_dir.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = output_dir / f"evaluation_report_{timestamp}.json"
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": self.get_performance_summary(),
            "detailed_metrics": self.metrics
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✓ Evaluation report saved to: {filepath}")
        return filepath
    
    def print_summary(self):
        """Print a formatted summary of performance."""
        summary = self.get_performance_summary()
        
        print("\n" + "="*80)
        print("AGENT PERFORMANCE SUMMARY")
        print("="*80)
        print(f"Total Tasks Executed: {summary['total_tasks']}")
        print(f"Success Rate: {summary['success_rate']:.1%}")
        print(f"Reflection Rate: {summary['reflection_rate']:.1%}")
        print(f"Average Reasoning Steps: {summary['average_reasoning_steps']}")
        print(f"\nAverage Scores:")
        print(f"  Overall: {summary['average_scores']['overall']:.2f}")
        print(f"  Efficiency: {summary['average_scores']['efficiency']:.2f}")
        print(f"  Tool Usage: {summary['average_scores']['tool_usage']:.2f}")
        print(f"  Reflection Quality: {summary['average_scores']['reflection_quality']:.2f}")
        print(f"\nMost Used Tool: {summary['most_used_tool']}")
        print("="*80)
