"""
AI Agentic System - Main Agent
Orchestrates reasoning, tool-calling, reflection, and evaluation.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

# Add modules to path
sys.path.append(str(Path(__file__).parent / "modules"))

from modules.agent_reasoning import AgentReasoning
from modules.agent_tools import ToolRegistry, RAGQueryTool, KnowledgeSearchTool
from modules.content_tools import BlogPostGeneratorTool, NewsletterGeneratorTool, HTMLGeneratorTool
from modules.email_tool import EmailSenderTool
from modules.agent_evaluator import AgentEvaluator
from modules.rag_system import RAGSystem
from modules.vector_database import VectorDatabase

# Import LLM clients
from openai import OpenAI
from anthropic import Anthropic
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class AgenticSystem:
    """
    Main AI Agentic System that combines reasoning, tool-calling, and reflection.
    """
    
    def __init__(
        self,
        vector_db: VectorDatabase,
        llm_provider: str = "gemini",
        model_name: Optional[str] = None,
        temperature: float = 0.7
    ):
        """
        Initialize the Agentic System.
        
        Args:
            vector_db: Vector database instance
            llm_provider: 'openai', 'anthropic', or 'gemini' (default: 'gemini')
            model_name: Specific model name
            temperature: Sampling temperature
        """
        print("\n" + "="*80)
        print("INITIALIZING AI AGENTIC SYSTEM")
        print("="*80)
        
        self.llm_provider = llm_provider.lower()
        self.temperature = temperature
        
        # Initialize LLM client
        if self.llm_provider == "openai":
            self.llm_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model_name = model_name or "gpt-3.5-turbo"
        elif self.llm_provider == "anthropic":
            self.llm_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            self.model_name = model_name or "claude-3-sonnet-20240229"
        elif self.llm_provider == "gemini":
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            self.model_name = model_name or "gemini-2.5-flash"
            self.llm_client = genai.GenerativeModel(self.model_name)
        else:
            raise ValueError(f"Unsupported LLM provider: {llm_provider}")
        
        print(f"✓ LLM: {self.llm_provider} ({self.model_name})")
        
        # Initialize RAG system
        self.rag_system = RAGSystem(
            vector_db=vector_db,
            llm_provider=self.llm_provider,
            model_name=self.model_name,
            temperature=self.temperature
        )
        print("✓ RAG System initialized")
        
        # Initialize reasoning module
        self.reasoning = AgentReasoning(
            llm_client=self.llm_client,
            llm_provider=self.llm_provider,
            model_name=self.model_name,
            temperature=self.temperature
        )
        print("✓ Reasoning Module initialized")
        
        # Initialize tool registry
        self.tools = ToolRegistry()
        self._register_tools()
        
        # Initialize evaluator
        self.evaluator = AgentEvaluator()
        print("✓ Evaluator initialized")
        
        print("="*80)
        print("SYSTEM READY")
        print("="*80 + "\n")
    
    def _register_tools(self):
        """Register all available tools."""
        # RAG tools
        self.tools.register(RAGQueryTool(self.rag_system))
        self.tools.register(KnowledgeSearchTool(self.rag_system.vector_db))
        
        # Content generation tools
        self.tools.register(BlogPostGeneratorTool(
            self.llm_client,
            self.llm_provider,
            self.model_name,
            self.rag_system
        ))
        self.tools.register(NewsletterGeneratorTool(
            self.llm_client,
            self.llm_provider,
            self.model_name,
            self.rag_system
        ))
        self.tools.register(HTMLGeneratorTool(
            self.llm_client,
            self.llm_provider,
            self.model_name,
            self.rag_system
        ))
        
        # Email tool
        self.tools.register(EmailSenderTool())
        
        print(f"✓ Registered {len(self.tools.list_tools())} tools")
    
    def execute_task(self, task: str, auto_reflect: bool = True) -> Dict[str, Any]:
        """
        Execute a task with full agentic capabilities: reasoning, tool-calling, and reflection.
        
        Args:
            task: The task to execute
            auto_reflect: Whether to automatically reflect on the result
            
        Returns:
            Dictionary with execution results and metadata
        """
        print(f"\n{'='*80}")
        print(f"TASK: {task}")
        print(f"{'='*80}\n")
        
        # Step 1: Reasoning
        print("🧠 REASONING...")
        reasoning = self.reasoning.think(task)
        print(f"✓ Understanding: {reasoning.get('understanding', 'N/A')}")
        print(f"✓ Steps planned: {len(reasoning.get('steps', []))}")
        
        # Step 2: Tool Selection
        print("\n🔧 SELECTING TOOLS...")
        tool_choice = self.reasoning.evaluate_tool_choice(
            task,
            self.tools.list_tools()
        )
        selected_tools = tool_choice.get("selected_tools", [])
        print(f"✓ Selected tools: {', '.join(selected_tools) if selected_tools else 'None'}")
        print(f"✓ Reasoning: {tool_choice.get('reasoning', 'N/A')}")
        
        # Step 3: Tool Execution
        print("\n⚡ EXECUTING...")
        results = []
        for tool_name in selected_tools:
            print(f"\n  Using tool: {tool_name}")
            result = self._execute_tool_intelligently(tool_name, task, reasoning)
            results.append({
                "tool": tool_name,
                "result": result
            })
            
            if result.get("success"):
                print(f"  ✓ Success")
            else:
                print(f"  ✗ Failed: {result.get('error', 'Unknown error')}")
        
        # If no tools were selected, provide direct answer
        if not results:
            print("  No tools needed - providing direct answer...")
            answer = self._generate_direct_answer(task)
            results.append({
                "tool": "direct_answer",
                "result": {
                    "success": True,
                    "result": answer,
                    "error": None
                }
            })
        
        # Step 4: Reflection
        reflection = None
        if auto_reflect:
            print("\n🔍 REFLECTING...")
            overall_success = all(r["result"].get("success", False) for r in results)
            reflection = self.reasoning.reflect(
                action_taken=f"Executed {len(results)} actions for task: {task}",
                result=results,
                expected_outcome=reasoning.get("execution_plan", "")
            )
            print(f"✓ Success assessment: {'Yes' if reflection.get('success', False) else 'No'}")
            print(f"✓ Analysis: {reflection.get('analysis', 'N/A')[:100]}...")
        
        # Step 5: Evaluation
        print("\n📊 EVALUATING...")
        evaluation = self.evaluator.evaluate_task_execution(
            task=task,
            result={"success": all(r["result"].get("success", False) for r in results)},
            reasoning_steps=len(reasoning.get("steps", [])),
            tools_used=selected_tools,
            reflection=reflection
        )
        print(f"✓ Overall score: {evaluation.get('overall', 0):.2f}")
        
        # Compile final result
        final_result = {
            "task": task,
            "reasoning": reasoning,
            "tool_selection": tool_choice,
            "execution_results": results,
            "reflection": reflection,
            "evaluation": evaluation,
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"\n{'='*80}")
        print("TASK COMPLETED")
        print(f"{'='*80}\n")
        
        return final_result
    
    def _execute_tool_intelligently(self, tool_name: str, task: str, reasoning: Dict) -> Dict[str, Any]:
        """
        Execute a tool with intelligent parameter extraction.
        
        Args:
            tool_name: Name of the tool
            task: Original task
            reasoning: Reasoning results
            
        Returns:
            Tool execution result
        """
        # Extract parameters from task based on tool
        params = self._extract_tool_parameters(tool_name, task, reasoning)
        
        # Execute tool
        return self.tools.execute_tool(tool_name, **params)
    
    def _extract_tool_parameters(self, tool_name: str, task: str, reasoning: Dict) -> Dict[str, Any]:
        """
        Extract parameters for a tool from the task description.
        Uses LLM to intelligently parse the task.
        """
        tool = self.tools.get_tool(tool_name)
        if not tool:
            return {}
        
        # Use LLM to extract parameters
        system_prompt = f"""You are a parameter extraction assistant.
Given a task and a tool, extract the appropriate parameters.

Tool: {tool.name}
Description: {tool.description}
Parameters: {json.dumps(tool.parameters, indent=2)}

Respond ONLY with a valid JSON object containing the parameters. No other text."""

        user_message = f"""Task: {task}

Extract the parameters for the {tool.name} tool from this task.
If a parameter is not explicitly mentioned, use a sensible default or leave it out."""

        try:
            if self.llm_provider == "openai":
                response = self.llm_client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    temperature=0.3,
                    max_tokens=500
                )
                response_text = response.choices[0].message.content
            
            elif self.llm_provider == "anthropic":
                response = self.llm_client.messages.create(
                    model=self.model_name,
                    max_tokens=500,
                    temperature=0.3,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": user_message}
                    ]
                )
                response_text = response.content[0].text
            
            elif self.llm_provider == "gemini":
                full_prompt = f"{system_prompt}\n\n{user_message}"
                response = self.llm_client.generate_content(
                    full_prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.3,
                        max_output_tokens=500,
                    )
                )
                response_text = response.text
            
            # Clean response and parse JSON
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            params = json.loads(response_text)
            return params
        
        except Exception as e:
            print(f"  Warning: Could not extract parameters: {e}")
            # Return minimal parameters based on task
            return {"query": task} if "query" in str(tool.parameters) else {}
    
    def _generate_direct_answer(self, task: str) -> str:
        """Generate a direct answer when no tools are needed."""
        system_prompt = """You are a helpful educational assistant.
Provide clear, concise, and accurate answers to questions."""
        
        try:
            if self.llm_provider == "openai":
                response = self.llm_client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": task}
                    ],
                    temperature=self.temperature,
                    max_tokens=1000
                )
                return response.choices[0].message.content
            
            elif self.llm_provider == "anthropic":
                response = self.llm_client.messages.create(
                    model=self.model_name,
                    max_tokens=1000,
                    temperature=self.temperature,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": task}
                    ]
                )
                return response.content[0].text
            
            elif self.llm_provider == "gemini":
                full_prompt = f"{system_prompt}\n\n{task}"
                response = self.llm_client.generate_content(
                    full_prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=self.temperature,
                        max_output_tokens=1000,
                    )
                )
                return response.text
        
        except Exception as e:
            return f"Error generating answer: {e}"
    
    def interactive_mode(self):
        """
        Start interactive mode where user can give tasks to the agent.
        """
        print("\n" + "="*80)
        print("AI AGENTIC SYSTEM - INTERACTIVE MODE")
        print("="*80)
        print("\nAvailable commands:")
        print("  - Ask any question or give a task")
        print("  - 'tools' - List available tools")
        print("  - 'stats' - Show performance statistics")
        print("  - 'save' - Save evaluation report")
        print("  - 'quit' - Exit")
        print("\nExamples:")
        print("  • What is machine learning?")
        print("  • Create a blog post about neural networks")
        print("  • Generate a newsletter about AI and email it to user@example.com")
        print("  • Create an HTML page about deep learning")
        print("="*80 + "\n")
        
        while True:
            try:
                task = input("\n🤖 Task: ").strip()
                
                if not task:
                    continue
                
                if task.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Shutting down agent...")
                    self.evaluator.print_summary()
                    save = input("\nSave evaluation report? (y/n): ").strip().lower()
                    if save == 'y':
                        self.evaluator.save_evaluation_report()
                    print("Goodbye!")
                    break
                
                if task.lower() == 'tools':
                    print("\n📦 Available Tools:")
                    print(self.tools.get_tools_description())
                    continue
                
                if task.lower() == 'stats':
                    self.evaluator.print_summary()
                    continue
                
                if task.lower() == 'save':
                    self.evaluator.save_evaluation_report()
                    continue
                
                # Execute task
                result = self.execute_task(task)
                
                # Display results
                self._display_results(result)
            
            except KeyboardInterrupt:
                print("\n\nInterrupted by user.")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
    
    def _display_results(self, result: Dict[str, Any]):
        """Display task execution results in a user-friendly format."""
        print("\n" + "─"*80)
        print("📋 RESULTS")
        print("─"*80)
        
        # Show execution results
        for exec_result in result.get("execution_results", []):
            tool = exec_result["tool"]
            tool_result = exec_result["result"]
            
            if tool_result.get("success"):
                content = tool_result.get("result", {})
                
                if tool == "rag_query":
                    print(f"\n💡 Answer: {content.get('answer', 'N/A')}")
                    sources = content.get('sources', [])
                    if sources:
                        print("\n📚 Sources:")
                        for i, src in enumerate(sources[:3], 1):
                            print(f"  {i}. {src.get('source', 'unknown')} (relevance: {src.get('relevance', 0):.2f})")
                
                elif tool == "direct_answer":
                    print(f"\n💡 Answer: {content}")
                
                elif "generate" in tool:
                    print(f"\n✍️  Content Generated:")
                    if isinstance(content, dict):
                        if content.get('filepath'):
                            print(f"   Saved to: {content['filepath']}")
                        if content.get('content'):
                            preview = content['content'][:200] + "..." if len(content['content']) > 200 else content['content']
                            print(f"\n   Preview:\n   {preview}")
                    else:
                        print(f"   {content}")
                
                elif tool == "send_email":
                    print(f"\n✉️  {content.get('message', 'Email sent')}")
            else:
                print(f"\n❌ {tool} failed: {tool_result.get('error', 'Unknown error')}")
        
        # Show evaluation score
        evaluation = result.get("evaluation", {})
        print(f"\n📊 Quality Score: {evaluation.get('overall', 0):.2f}/1.00")
        print("─"*80)


if __name__ == "__main__":
    # This will be called from a separate runner script
    pass
