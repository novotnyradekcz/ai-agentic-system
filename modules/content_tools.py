"""
Content Generation Tools
Tools for creating various types of content (blog posts, PDFs, HTML, etc.)
"""

from typing import Dict, Any, Optional
from modules.agent_tools import Tool
from datetime import datetime
from pathlib import Path
import json


class BlogPostGeneratorTool(Tool):
    """Tool for generating blog posts from knowledge base topics."""
    
    def __init__(self, llm_client, llm_provider: str, model_name: str, rag_system=None):
        self.llm_client = llm_client
        self.llm_provider = llm_provider
        self.model_name = model_name
        self.rag_system = rag_system
    
    @property
    def name(self) -> str:
        return "generate_blog_post"
    
    @property
    def description(self) -> str:
        return "Generate a blog post or social media content about a specific topic from the knowledge base."
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "topic": "str - The topic to write about",
            "style": "str - Writing style: 'professional', 'casual', 'technical', 'social_media' (default: 'professional')",
            "length": "str - Content length: 'short' (300 words), 'medium' (600 words), 'long' (1000+ words) (default: 'medium')",
            "save_to_file": "bool - Whether to save to a file (default: True)"
        }
    
    def execute(self, topic: str, style: str = "professional", length: str = "medium", save_to_file: bool = True, **kwargs) -> Dict[str, Any]:
        """Generate blog post."""
        try:
            # Get relevant information from RAG if available
            context = ""
            if self.rag_system:
                rag_result = self.rag_system.answer_question(
                    f"Provide comprehensive information about {topic}",
                    n_results=7,
                    return_context=True
                )
                context = "\n".join([ctx['text'] for ctx in rag_result.get('context', [])])
            
            # Define word counts
            word_counts = {
                "short": "300-400",
                "medium": "600-800",
                "long": "1000-1500"
            }
            target_words = word_counts.get(length, "600-800")
            
            # Style-specific instructions
            style_instructions = {
                "professional": "Use a professional, authoritative tone suitable for a business blog.",
                "casual": "Use a conversational, friendly tone as if talking to a friend.",
                "technical": "Use technical language and precise terminology for a technical audience.",
                "social_media": "Use engaging, concise language with emojis, hashtags at the end. Keep it punchy and shareable."
            }
            style_instruction = style_instructions.get(style, style_instructions["professional"])
            
            system_prompt = f"""You are a professional content writer and educator.
Create engaging, informative content based on the provided information.
{style_instruction}
Target length: {target_words} words.

For social media posts:
- Include attention-grabbing opening
- Use short paragraphs
- Add 3-5 relevant hashtags at the end

For blog posts:
- Include a compelling title
- Start with a hook
- Use clear section headings
- Include a conclusion/call-to-action"""

            user_message = f"""Topic: {topic}

Context Information:
{context if context else "Use your general knowledge about this topic."}

Please create {length} {style} content about this topic."""

            response_text = self._call_llm(system_prompt, user_message, max_tokens=2000)
            
            # Save to file if requested
            filepath = None
            if save_to_file:
                filepath = self._save_content(response_text, topic, "blog_post", style)
            
            return {
                "success": True,
                "result": {
                    "content": response_text,
                    "filepath": str(filepath) if filepath else None,
                    "word_count": len(response_text.split()),
                    "style": style,
                    "topic": topic
                },
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "result": None,
                "error": str(e)
            }
    
    def _call_llm(self, system_prompt: str, user_message: str, max_tokens: int = 2000) -> str:
        """Call the LLM."""
        if self.llm_provider == "openai":
            response = self.llm_client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        
        elif self.llm_provider == "anthropic":
            response = self.llm_client.messages.create(
                model=self.model_name,
                max_tokens=max_tokens,
                temperature=0.7,
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
                    temperature=0.7,
                    max_output_tokens=max_tokens,
                )
            )
            return response.text
    
    def _save_content(self, content: str, topic: str, content_type: str, style: str) -> Path:
        """Save content to file."""
        output_dir = Path(__file__).parent.parent / "outputs"
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_topic = safe_topic.replace(' ', '_')[:50]
        
        filename = f"{content_type}_{style}_{safe_topic}_{timestamp}.txt"
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Topic: {topic}\n")
            f.write(f"Style: {style}\n")
            f.write("="*80 + "\n\n")
            f.write(content)
        
        return filepath


class NewsletterGeneratorTool(Tool):
    """Tool for generating newsletter-style content."""
    
    def __init__(self, llm_client, llm_provider: str, model_name: str, rag_system=None):
        self.llm_client = llm_client
        self.llm_provider = llm_provider
        self.model_name = model_name
        self.rag_system = rag_system
    
    @property
    def name(self) -> str:
        return "generate_newsletter"
    
    @property
    def description(self) -> str:
        return "Generate a professional newsletter about a topic, ready to be sent via email."
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "topic": "str - The main topic or theme",
            "sections": "int - Number of sections (default: 3)",
            "save_to_file": "bool - Whether to save to file (default: True)"
        }
    
    def execute(self, topic: str, sections: int = 3, save_to_file: bool = True, **kwargs) -> Dict[str, Any]:
        """Generate newsletter."""
        try:
            # Get relevant information
            context = ""
            if self.rag_system:
                rag_result = self.rag_system.answer_question(
                    f"Provide comprehensive information about {topic} suitable for a newsletter",
                    n_results=7,
                    return_context=True
                )
                context = "\n".join([ctx['text'] for ctx in rag_result.get('context', [])])
            
            system_prompt = """You are a professional newsletter writer.
Create an engaging, informative newsletter with:
- A catchy subject line
- A warm greeting
- Clear sections with headings
- Engaging but professional tone
- A call-to-action or conclusion
- Professional sign-off

Format the newsletter ready for email distribution."""

            user_message = f"""Topic: {topic}
Number of sections: {sections}

Context Information:
{context if context else "Use your general knowledge about this topic."}

Create a newsletter about this topic."""

            response_text = self._call_llm(system_prompt, user_message)
            
            # Save to file
            filepath = None
            if save_to_file:
                output_dir = Path(__file__).parent.parent / "outputs"
                output_dir.mkdir(exist_ok=True)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()
                safe_topic = safe_topic.replace(' ', '_')[:50]
                
                filename = f"newsletter_{safe_topic}_{timestamp}.txt"
                filepath = output_dir / filename
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(response_text)
            
            return {
                "success": True,
                "result": {
                    "content": response_text,
                    "filepath": str(filepath) if filepath else None,
                    "topic": topic
                },
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "result": None,
                "error": str(e)
            }
    
    def _call_llm(self, system_prompt: str, user_message: str, max_tokens: int = 2000) -> str:
        """Call the LLM."""
        if self.llm_provider == "openai":
            response = self.llm_client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        
        elif self.llm_provider == "anthropic":
            response = self.llm_client.messages.create(
                model=self.model_name,
                max_tokens=max_tokens,
                temperature=0.7,
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
                    temperature=0.7,
                    max_output_tokens=max_tokens,
                )
            )
            return response.text


class HTMLGeneratorTool(Tool):
    """Tool for generating simple HTML pages."""
    
    def __init__(self, llm_client, llm_provider: str, model_name: str, rag_system=None):
        self.llm_client = llm_client
        self.llm_provider = llm_provider
        self.model_name = model_name
        self.rag_system = rag_system
    
    @property
    def name(self) -> str:
        return "generate_html"
    
    @property
    def description(self) -> str:
        return "Generate a simple, attractive HTML page about a topic."
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "topic": "str - The topic for the HTML page",
            "save_to_file": "bool - Whether to save to file (default: True)"
        }
    
    def execute(self, topic: str, save_to_file: bool = True, **kwargs) -> Dict[str, Any]:
        """Generate HTML page."""
        try:
            # Get content from RAG
            content = ""
            if self.rag_system:
                rag_result = self.rag_system.answer_question(
                    f"Provide comprehensive information about {topic}",
                    n_results=7,
                    return_context=True
                )
                content = rag_result.get('answer', '')
            
            # Create HTML template
            html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}
        h1 {{
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #764ba2;
            margin-top: 30px;
        }}
        p {{
            text-align: justify;
            margin: 15px 0;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{topic}</h1>
        {self._format_content_as_html(content)}
        <div class="footer">
            <p>Generated by AI Educational Assistant | {datetime.now().strftime('%B %d, %Y')}</p>
        </div>
    </div>
</body>
</html>"""
            
            # Save to file
            filepath = None
            if save_to_file:
                output_dir = Path(__file__).parent.parent / "outputs"
                output_dir.mkdir(exist_ok=True)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()
                safe_topic = safe_topic.replace(' ', '_')[:50]
                
                filename = f"webpage_{safe_topic}_{timestamp}.html"
                filepath = output_dir / filename
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html_content)
            
            return {
                "success": True,
                "result": {
                    "html": html_content,
                    "filepath": str(filepath) if filepath else None,
                    "topic": topic
                },
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "result": None,
                "error": str(e)
            }
    
    def _format_content_as_html(self, content: str) -> str:
        """Convert plain text content to HTML paragraphs."""
        paragraphs = content.split('\n\n')
        html_parts = []
        
        for para in paragraphs:
            para = para.strip()
            if para:
                if para.startswith('#'):
                    # Heading
                    heading = para.lstrip('#').strip()
                    html_parts.append(f"<h2>{heading}</h2>")
                else:
                    html_parts.append(f"<p>{para}</p>")
        
        return '\n        '.join(html_parts)
