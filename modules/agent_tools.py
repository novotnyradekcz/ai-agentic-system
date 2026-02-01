"""
Agent Tools Framework
Base classes and registry for agent tools.
"""

from typing import Dict, Any, List, Callable, Optional
from abc import ABC, abstractmethod
import inspect


class Tool(ABC):
    """Base class for all agent tools."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Tool description for the agent to understand when to use it."""
        pass
    
    @property
    def parameters(self) -> Dict[str, Any]:
        """
        Tool parameters schema.
        Override this if your tool needs specific parameters.
        """
        return {}
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool.
        
        Returns:
            Dictionary with 'success', 'result', and optional 'error'
        """
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert tool to dictionary representation."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }


class ToolRegistry:
    """Registry to manage all available tools."""
    
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
    
    def register(self, tool: Tool):
        """Register a new tool."""
        self.tools[tool.name] = tool
        print(f"✓ Registered tool: {tool.name}")
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """Get a tool by name."""
        return self.tools.get(name)
    
    def list_tools(self) -> List[str]:
        """List all available tool names."""
        return list(self.tools.keys())
    
    def get_tools_description(self) -> str:
        """Get formatted description of all tools."""
        descriptions = []
        for tool in self.tools.values():
            desc = f"- {tool.name}: {tool.description}"
            if tool.parameters:
                params = ", ".join(f"{k}: {v}" for k, v in tool.parameters.items())
                desc += f"\n  Parameters: {params}"
            descriptions.append(desc)
        return "\n".join(descriptions)
    
    def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a tool by name.
        
        Args:
            tool_name: Name of the tool to execute
            **kwargs: Parameters for the tool
            
        Returns:
            Tool execution result
        """
        tool = self.get_tool(tool_name)
        if not tool:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not found",
                "result": None
            }
        
        try:
            result = tool.execute(**kwargs)
            return result
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "result": None
            }


class RAGQueryTool(Tool):
    """Tool for querying the RAG knowledge base."""
    
    def __init__(self, rag_system):
        self.rag_system = rag_system
    
    @property
    def name(self) -> str:
        return "rag_query"
    
    @property
    def description(self) -> str:
        return "Query the knowledge base to retrieve information. Use this when you need to find specific information from the loaded documents."
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "query": "str - The question or search query",
            "n_results": "int - Number of relevant chunks to retrieve (default: 5)"
        }
    
    def execute(self, query: str, n_results: int = 5, **kwargs) -> Dict[str, Any]:
        """Execute RAG query."""
        try:
            result = self.rag_system.answer_question(query, n_results=n_results, return_context=True)
            return {
                "success": True,
                "result": {
                    "answer": result["answer"],
                    "sources": [
                        {
                            "source": ctx["metadata"].get("source", "unknown"),
                            "relevance": ctx["score"]
                        }
                        for ctx in result.get("context", [])
                    ]
                },
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "result": None,
                "error": str(e)
            }


class KnowledgeSearchTool(Tool):
    """Tool for searching the knowledge base without generating an answer."""
    
    def __init__(self, vector_db):
        self.vector_db = vector_db
    
    @property
    def name(self) -> str:
        return "knowledge_search"
    
    @property
    def description(self) -> str:
        return "Search for relevant information in the knowledge base. Returns raw context chunks without generating an answer."
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "query": "str - The search query",
            "n_results": "int - Number of results (default: 5)"
        }
    
    def execute(self, query: str, n_results: int = 5, **kwargs) -> Dict[str, Any]:
        """Execute knowledge search."""
        try:
            results = self.vector_db.query(query, n_results=n_results)
            
            chunks = []
            for i in range(len(results['documents'])):
                chunks.append({
                    'text': results['documents'][i],
                    'source': results['metadatas'][i].get('source', 'unknown'),
                    'relevance': 1 - results['distances'][i]
                })
            
            return {
                "success": True,
                "result": chunks,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "result": None,
                "error": str(e)
            }
