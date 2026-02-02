"""
Agent Reasoning and Reflection Module
Enables the agent to think, plan, and self-correct its actions.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json


class AgentReasoning:
    """Handles agent's reasoning, planning, and reflection capabilities."""
    
    def __init__(self, llm_client, llm_provider: str, model_name: str, temperature: float = 0.7):
        """
        Initialize the reasoning module.
        
        Args:
            llm_client: The LLM client instance
            llm_provider: 'openai', 'anthropic', or 'gemini'
            model_name: Model name
            temperature: Sampling temperature
        """
        self.llm_client = llm_client
        self.llm_provider = llm_provider
        self.model_name = model_name
        self.temperature = temperature
        self.reasoning_history = []
    
    def _clean_json_response(self, response_text: str) -> str:
        """
        Clean LLM response by removing markdown code blocks.
        
        Args:
            response_text: Raw response from LLM
            
        Returns:
            Cleaned JSON string
        """
        response_text = response_text.strip()
        
        # Remove markdown code blocks
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        elif response_text.startswith("```"):
            response_text = response_text[3:]
        
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        return response_text.strip()
    
    def think(self, task: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Perform reasoning about a task.
        
        Args:
            task: The task to reason about
            context: Additional context
            
        Returns:
            Dictionary containing reasoning steps and plan
        """
        system_prompt = """You are an AI agent with strong reasoning capabilities. 
Your task is to think through problems step by step before taking action.
When given a task, you should:
1. Understand the goal clearly
2. Break it down into actionable steps
3. Identify what tools or resources you'll need
4. Consider potential challenges
5. Create a clear execution plan

Respond in JSON format with the following structure:
{
    "understanding": "What you understand about the task",
    "steps": ["Step 1", "Step 2", ...],
    "tools_needed": ["tool1", "tool2", ...],
    "potential_challenges": ["challenge1", "challenge2", ...],
    "execution_plan": "Your detailed plan"
}"""
        
        user_message = f"Task: {task}"
        if context:
            user_message += f"\n\nAdditional Context: {context}"
        
        response_text = self._call_llm(system_prompt, user_message)
        
        # Parse JSON response
        try:
            response_text = self._clean_json_response(response_text)
            reasoning = json.loads(response_text)
        except json.JSONDecodeError:
            # Fallback if LLM doesn't return proper JSON
            reasoning = {
                "understanding": response_text,
                "steps": [],
                "tools_needed": [],
                "potential_challenges": [],
                "execution_plan": response_text
            }
        
        # Log reasoning
        self.reasoning_history.append({
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "reasoning": reasoning
        })
        
        return reasoning
    
    def reflect(self, action_taken: str, result: Any, expected_outcome: Optional[str] = None, actual_success: bool = True) -> Dict[str, Any]:
        """
        Reflect on an action and its outcome.
        
        Args:
            action_taken: Description of the action
            result: The actual result
            expected_outcome: What was expected (if any)
            actual_success: The actual success status of the action
            
        Returns:
            Dictionary containing reflection and suggestions
        """
        system_prompt = f"""You are an AI agent capable of self-reflection.
Analyze the action taken and its result. The action was {'SUCCESSFUL' if actual_success else 'UNSUCCESSFUL'}.
Evaluate:
1. What was achieved?
2. What went well or what went wrong?
3. What could be improved for future tasks?
4. Are there any lessons learned?

Respond in JSON format:
{{
    "success": {str(actual_success).lower()},
    "analysis": "Your analysis of what happened and why",
    "strengths": ["What went well"],
    "weaknesses": ["What could improve"],
    "next_steps": ["Recommended next actions"],
    "lessons_learned": ["Key takeaways"]
}}"""
        
        user_message = f"""Action Taken: {action_taken}
Result: {result}"""
        
        if expected_outcome:
            user_message += f"\nExpected Outcome: {expected_outcome}"
        
        response_text = self._call_llm(system_prompt, user_message)
        
        try:
            response_text = self._clean_json_response(response_text)
            reflection = json.loads(response_text)
            # Ensure success matches actual outcome
            reflection["success"] = actual_success
        except json.JSONDecodeError:
            reflection = {
                "success": actual_success,
                "analysis": response_text,
                "strengths": [],
                "weaknesses": [],
                "next_steps": [],
                "lessons_learned": []
            }
        
        # Log reflection
        self.reasoning_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": "reflection",
            "action": action_taken,
            "reflection": reflection
        })
        
        return reflection
    
    def evaluate_tool_choice(self, task: str, available_tools: List[str]) -> Dict[str, Any]:
        """
        Decide which tool(s) to use for a task.
        
        Args:
            task: The task to accomplish
            available_tools: List of available tool names
            
        Returns:
            Dictionary with recommended tools and reasoning
        """
        system_prompt = f"""You are an AI agent selecting the best tools for a task.
Available tools: {', '.join(available_tools)}

Analyze the task carefully and select ONLY the tool(s) that are explicitly needed.
- If the user asks for ONE specific output (e.g., "create a PDF"), select ONLY that tool
- Only select multiple tools if the task explicitly requires multiple actions (e.g., "create a PDF and email it")
- generate_html creates HTML pages
- generate_pdf creates PDF documents
- DO NOT select both generate_html and generate_pdf unless explicitly asked for both

Respond in JSON format:
{{
    "selected_tools": ["tool1"],
    "reasoning": "Why this tool is appropriate",
    "sequence": "The order to use them in",
    "confidence": 0.0-1.0
}}"""
        
        user_message = f"Task: {task}"
        
        response_text = self._call_llm(system_prompt, user_message)
        
        try:
            response_text = self._clean_json_response(response_text)
            tool_choice = json.loads(response_text)
        except json.JSONDecodeError:
            tool_choice = {
                "selected_tools": [],
                "reasoning": response_text,
                "sequence": "",
                "confidence": 0.5
            }
        
        return tool_choice
    
    def critique_output(self, task: str, output: str, criteria: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Critique the quality of generated output.
        
        Args:
            task: Original task
            output: Generated output
            criteria: Evaluation criteria
            
        Returns:
            Dictionary with critique and quality score
        """
        default_criteria = [
            "Relevance to the task",
            "Clarity and coherence",
            "Completeness",
            "Accuracy",
            "Professional quality"
        ]
        
        criteria_list = criteria or default_criteria
        
        system_prompt = f"""You are an AI quality evaluator.
Evaluate the output based on these criteria:
{chr(10).join(f"{i+1}. {c}" for i, c in enumerate(criteria_list))}

Respond in JSON format:
{{
    "overall_score": 0.0-1.0,
    "criteria_scores": {{"criterion": score, ...}},
    "strengths": ["strength1", "strength2"],
    "improvements": ["improvement1", "improvement2"],
    "revised_output": "Improved version if needed (or empty if good)",
    "meets_requirements": true/false
}}"""
        
        user_message = f"""Task: {task}

Output to Evaluate:
{output}"""
        
        response_text = self._call_llm(system_prompt, user_message)
        
        try:
            response_text = self._clean_json_response(response_text)
            critique = json.loads(response_text)
        except json.JSONDecodeError:
            critique = {
                "overall_score": 0.7,
                "criteria_scores": {},
                "strengths": [],
                "improvements": [],
                "revised_output": "",
                "meets_requirements": True
            }
        
        return critique
    
    def _call_llm(self, system_prompt: str, user_message: str, max_tokens: int = 2000) -> str:
        """
        Call the LLM with the appropriate provider.
        
        Args:
            system_prompt: System instructions
            user_message: User message
            max_tokens: Maximum tokens in response
            
        Returns:
            LLM response text
        """
        try:
            if self.llm_provider == "openai":
                response = self.llm_client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    temperature=self.temperature,
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content
            
            elif self.llm_provider == "anthropic":
                response = self.llm_client.messages.create(
                    model=self.model_name,
                    max_tokens=max_tokens,
                    temperature=self.temperature,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": user_message}
                    ]
                )
                return response.content[0].text
            
            elif self.llm_provider == "gemini":
                import google.generativeai as genai
                full_prompt = f"{system_prompt}\n\n{user_message}"
                response = self.llm_client.generate_content(
                    full_prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=self.temperature,
                        max_output_tokens=max_tokens,
                    )
                )
                return response.text
            
        except Exception as e:
            return f"Error calling LLM: {e}"
    
    def get_reasoning_history(self) -> List[Dict]:
        """Get all reasoning and reflection history."""
        return self.reasoning_history
    
    def clear_history(self):
        """Clear reasoning history."""
        self.reasoning_history = []
