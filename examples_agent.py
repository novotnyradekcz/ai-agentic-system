"""
AI Agentic System - Example Usage
Demonstrates various capabilities of the agentic system.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from agent import AgenticSystem
from modules.vector_database import VectorDatabase


def example_simple_query():
    """Example 1: Simple knowledge base query."""
    print("\n" + "="*80)
    print("EXAMPLE 1: Simple Knowledge Base Query")
    print("="*80)
    
    # Initialize components
    vector_db = VectorDatabase(collection_name="demo_kb")
    agent = AgenticSystem(vector_db=vector_db, llm_provider="gemini")
    
    # Execute a simple query
    result = agent.execute_task("What is machine learning?")
    
    # Access results
    print("\n📊 Task Summary:")
    print(f"Success: {result['evaluation']['overall'] > 0.5}")
    print(f"Quality Score: {result['evaluation']['overall']:.2f}")


def example_content_generation():
    """Example 2: Generate blog post."""
    print("\n" + "="*80)
    print("EXAMPLE 2: Content Generation")
    print("="*80)
    
    vector_db = VectorDatabase(collection_name="demo_kb")
    agent = AgenticSystem(vector_db=vector_db, llm_provider="gemini")
    
    # Generate a blog post
    result = agent.execute_task(
        "Create a short professional blog post about artificial intelligence"
    )
    
    # Check execution results
    for exec_result in result["execution_results"]:
        if exec_result["result"].get("success"):
            content = exec_result["result"].get("result", {})
            if isinstance(content, dict) and "filepath" in content:
                print(f"\n✅ Content saved to: {content['filepath']}")


def example_with_reflection():
    """Example 3: Task execution with reflection analysis."""
    print("\n" + "="*80)
    print("EXAMPLE 3: Task with Reflection")
    print("="*80)
    
    vector_db = VectorDatabase(collection_name="demo_kb")
    agent = AgenticSystem(vector_db=vector_db, llm_provider="gemini")
    
    result = agent.execute_task(
        "Generate a newsletter about neural networks",
        auto_reflect=True
    )
    
    # Analyze reflection
    reflection = result.get("reflection")
    if reflection:
        print("\n🔍 Reflection Analysis:")
        print(f"Success: {reflection.get('success', False)}")
        print(f"Strengths: {reflection.get('strengths', [])}")
        print(f"Improvements: {reflection.get('improvements', [])}")


def example_reasoning_inspection():
    """Example 4: Inspect agent's reasoning process."""
    print("\n" + "="*80)
    print("EXAMPLE 4: Reasoning Inspection")
    print("="*80)
    
    vector_db = VectorDatabase(collection_name="demo_kb")
    agent = AgenticSystem(vector_db=vector_db, llm_provider="gemini")
    
    result = agent.execute_task("Create an HTML page about deep learning")
    
    # Inspect reasoning
    reasoning = result.get("reasoning", {})
    print("\n🧠 Agent's Reasoning:")
    print(f"Understanding: {reasoning.get('understanding', 'N/A')}")
    print(f"\nPlanned Steps:")
    for i, step in enumerate(reasoning.get('steps', []), 1):
        print(f"  {i}. {step}")
    print(f"\nTools Identified: {reasoning.get('tools_needed', [])}")


def example_performance_metrics():
    """Example 5: Track performance across multiple tasks."""
    print("\n" + "="*80)
    print("EXAMPLE 5: Performance Tracking")
    print("="*80)
    
    vector_db = VectorDatabase(collection_name="demo_kb")
    agent = AgenticSystem(vector_db=vector_db, llm_provider="gemini")
    
    # Execute multiple tasks
    tasks = [
        "What is deep learning?",
        "Create a short social media post about AI",
        "Generate a newsletter about machine learning"
    ]
    
    for task in tasks:
        print(f"\nExecuting: {task}")
        agent.execute_task(task, auto_reflect=False)
    
    # Show performance summary
    agent.evaluator.print_summary()
    
    # Save evaluation report
    agent.evaluator.save_evaluation_report()


def example_tool_selection():
    """Example 6: Observe tool selection process."""
    print("\n" + "="*80)
    print("EXAMPLE 6: Tool Selection Process")
    print("="*80)
    
    vector_db = VectorDatabase(collection_name="demo_kb")
    agent = AgenticSystem(vector_db=vector_db, llm_provider="gemini")
    
    result = agent.execute_task(
        "Search for information about transformers and create a blog post"
    )
    
    # Analyze tool selection
    tool_choice = result.get("tool_selection", {})
    print("\n🔧 Tool Selection:")
    print(f"Selected Tools: {tool_choice.get('selected_tools', [])}")
    print(f"Reasoning: {tool_choice.get('reasoning', 'N/A')}")
    print(f"Confidence: {tool_choice.get('confidence', 0):.2f}")


def run_all_examples():
    """Run all examples sequentially."""
    examples = [
        ("Simple Query", example_simple_query),
        ("Content Generation", example_content_generation),
        ("With Reflection", example_with_reflection),
        ("Reasoning Inspection", example_reasoning_inspection),
        ("Performance Metrics", example_performance_metrics),
        ("Tool Selection", example_tool_selection),
    ]
    
    print("\n" + "="*80)
    print("AI AGENTIC SYSTEM - EXAMPLES")
    print("="*80)
    
    for i, (name, func) in enumerate(examples, 1):
        print(f"\n[{i}/{len(examples)}] Running: {name}")
        try:
            func()
        except Exception as e:
            print(f"❌ Error in {name}: {e}")
        
        if i < len(examples):
            input("\nPress Enter to continue to next example...")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run agent examples")
    parser.add_argument(
        '--example',
        type=int,
        choices=range(1, 7),
        help='Run specific example (1-6), or omit to run all'
    )
    
    args = parser.parse_args()
    
    if args.example:
        examples = [
            example_simple_query,
            example_content_generation,
            example_with_reflection,
            example_reasoning_inspection,
            example_performance_metrics,
            example_tool_selection,
        ]
        examples[args.example - 1]()
    else:
        run_all_examples()
