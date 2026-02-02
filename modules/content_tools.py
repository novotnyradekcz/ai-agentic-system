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
            # Get content from RAG with increased token limit for comprehensive content
            content = ""
            if self.rag_system:
                # Temporarily increase max_tokens for HTML generation
                original_max_tokens = self.rag_system.max_tokens
                self.rag_system.max_tokens = 3000  # Allow for comprehensive HTML content
                
                rag_result = self.rag_system.answer_question(
                    f"Provide comprehensive, detailed information about {topic}. Include multiple sections with clear headings. Write at least 5-6 detailed paragraphs covering different aspects of the topic.",
                    n_results=7,
                    return_context=True
                )
                content = rag_result.get('answer', '')
                
                # Restore original max_tokens
                self.rag_system.max_tokens = original_max_tokens
            
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
        h3 {{
            color: #667eea;
            margin-top: 25px;
            font-size: 1.3em;
        }}
        h4 {{
            color: #764ba2;
            margin-top: 20px;
            font-size: 1.1em;
        }}
        p {{
            text-align: justify;
            margin: 15px 0;
        }}
        ul, ol {{
            margin: 15px 0;
            padding-left: 30px;
        }}
        li {{
            margin: 8px 0;
            line-height: 1.6;
        }}
        strong {{
            color: #333;
            font-weight: 600;
        }}
        em {{
            color: #555;
            font-style: italic;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            color: #d63384;
        }}
        a {{
            color: #667eea;
            text-decoration: none;
            border-bottom: 1px solid #667eea;
        }}
        a:hover {{
            color: #764ba2;
            border-bottom-color: #764ba2;
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
        """Convert markdown content to HTML."""
        import re
        
        # Split by double newlines first, but also handle headings followed by single newlines
        paragraphs = content.split('\n\n')
        html_parts = []
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # Check for headings (must check longer patterns first)
            # Extract only the first line as heading if it starts with #
            if para.startswith('####'):
                lines = para.split('\n', 1)
                heading = lines[0].lstrip('#').strip()
                heading = self._convert_inline_markdown(heading)
                html_parts.append(f"<h4>{heading}</h4>")
                # If there's content after the heading, process it as a paragraph
                if len(lines) > 1 and lines[1].strip():
                    remaining = self._convert_inline_markdown(lines[1].strip())
                    html_parts.append(f"<p>{remaining}</p>")
            elif para.startswith('###'):
                lines = para.split('\n', 1)
                heading = lines[0].lstrip('#').strip()
                heading = self._convert_inline_markdown(heading)
                html_parts.append(f"<h3>{heading}</h3>")
                if len(lines) > 1 and lines[1].strip():
                    remaining = self._convert_inline_markdown(lines[1].strip())
                    html_parts.append(f"<p>{remaining}</p>")
            elif para.startswith('##'):
                lines = para.split('\n', 1)
                heading = lines[0].lstrip('#').strip()
                heading = self._convert_inline_markdown(heading)
                html_parts.append(f"<h2>{heading}</h2>")
                if len(lines) > 1 and lines[1].strip():
                    remaining = self._convert_inline_markdown(lines[1].strip())
                    html_parts.append(f"<p>{remaining}</p>")
            elif para.startswith('#'):
                lines = para.split('\n', 1)
                heading = lines[0].lstrip('#').strip()
                heading = self._convert_inline_markdown(heading)
                html_parts.append(f"<h2>{heading}</h2>")
                if len(lines) > 1 and lines[1].strip():
                    remaining = self._convert_inline_markdown(lines[1].strip())
                    html_parts.append(f"<p>{remaining}</p>")
            # Check for bullet lists
            elif para.startswith('- ') or para.startswith('* ') or para.startswith('• '):
                # Handle multi-line bullet lists
                list_items = []
                lines = para.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith('- ') or line.startswith('* ') or line.startswith('• '):
                        item_text = re.sub(r'^[-*•]\s+', '', line)
                        item_text = self._convert_inline_markdown(item_text)
                        list_items.append(f"<li>{item_text}</li>")
                if list_items:
                    items_html = '\n            '.join(list_items)
                    html_parts.append(f"<ul>\n            {items_html}\n        </ul>")
            # Check for numbered lists
            elif re.match(r'^\d+\.\s', para):
                list_items = []
                lines = para.split('\n')
                for line in lines:
                    line = line.strip()
                    if re.match(r'^\d+\.\s', line):
                        item_text = re.sub(r'^\d+\.\s+', '', line)
                        item_text = self._convert_inline_markdown(item_text)
                        list_items.append(f"<li>{item_text}</li>")
                if list_items:
                    items_html = '\n            '.join(list_items)
                    html_parts.append(f"<ol>\n            {items_html}\n        </ol>")
            # Regular paragraph
            else:
                para = self._convert_inline_markdown(para)
                html_parts.append(f"<p>{para}</p>")
        
        return '\n        '.join(html_parts)
    
    def _convert_inline_markdown(self, text: str) -> str:
        """Convert inline markdown formatting to HTML."""
        import re
        
        # Bold: **text** or __text__
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)
        
        # Italic: *text* or _text_ (but not in middle of words)
        text = re.sub(r'(?<!\w)\*(.+?)\*(?!\w)', r'<em>\1</em>', text)
        text = re.sub(r'(?<!\w)_(.+?)_(?!\w)', r'<em>\1</em>', text)
        
        # Inline code: `code`
        text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
        
        # Links: [text](url)
        text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2" target="_blank">\1</a>', text)
        
        return text


class PDFGeneratorTool(Tool):
    """Tool for generating PDF documents/reports."""
    
    def __init__(self, llm_client, llm_provider: str, model_name: str, rag_system=None):
        self.llm_client = llm_client
        self.llm_provider = llm_provider
        self.model_name = model_name
        self.rag_system = rag_system
    
    @property
    def name(self) -> str:
        return "generate_pdf"
    
    @property
    def description(self) -> str:
        return "Generate a professional PDF document or report about a specific topic."
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "topic": "str - The topic for the PDF document",
            "style": "str - Document style: 'report', 'guide', 'tutorial', 'whitepaper' (default: 'report')",
            "save_to_file": "bool - Whether to save to file (default: True)"
        }
    
    def execute(self, topic: str, style: str = "report", save_to_file: bool = True, **kwargs) -> Dict[str, Any]:
        """Generate PDF document."""
        try:
            # Import PDF library
            try:
                from reportlab.lib.pagesizes import letter
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.lib.units import inch
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
                from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
            except ImportError:
                return {
                    "success": False,
                    "result": None,
                    "error": "reportlab library not installed. Run: pip install reportlab"
                }
            
            # Get relevant information from RAG if available
            context = ""
            if self.rag_system:
                rag_result = self.rag_system.answer_question(
                    f"Provide comprehensive information about {topic}",
                    n_results=10,
                    return_context=True
                )
                context = "\n".join([ctx['text'] for ctx in rag_result.get('context', [])])
            
            # Generate content based on style
            content = self._generate_pdf_content(topic, style, context)
            
            if not save_to_file:
                return {
                    "success": True,
                    "result": {"content": content},
                    "error": None
                }
            
            # Create PDF
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{topic.lower().replace(' ', '_')}_{timestamp}.pdf"
            filepath = Path("outputs") / filename
            filepath.parent.mkdir(exist_ok=True)
            
            # Create PDF document
            doc = SimpleDocTemplate(str(filepath), pagesize=letter,
                                   topMargin=1*inch, bottomMargin=0.75*inch,
                                   leftMargin=1*inch, rightMargin=1*inch)
            
            # Container for content
            story = []
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor='#1a1a1a',
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                textColor='#2c3e50',
                spaceAfter=12,
                spaceBefore=12
            )
            
            subheading_style = ParagraphStyle(
                'CustomSubHeading',
                parent=styles['Heading3'],
                fontSize=13,
                textColor='#34495e',
                spaceAfter=10,
                spaceBefore=10
            )
            
            body_style = ParagraphStyle(
                'CustomBody',
                parent=styles['BodyText'],
                fontSize=11,
                alignment=TA_JUSTIFY,
                spaceAfter=12
            )
            
            # Parse and add content
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if not line:
                    story.append(Spacer(1, 0.2*inch))
                elif line.startswith('#### '):
                    # Fourth-level heading (render as subheading)
                    story.append(Paragraph(line[5:], subheading_style))
                elif line.startswith('### '):
                    # Third-level heading
                    story.append(Paragraph(line[4:], subheading_style))
                elif line.startswith('## '):
                    # Second-level heading
                    story.append(Spacer(1, 0.1*inch))
                    story.append(Paragraph(line[3:], heading_style))
                elif line.startswith('# '):
                    # Title (first-level heading)
                    story.append(Paragraph(line[2:], title_style))
                elif line.startswith('* ') or line.startswith('- '):
                    # Bullet point
                    bullet_text = line[2:] if line.startswith('* ') else line[2:]
                    bullet_text = self._format_markdown_text(bullet_text)
                    story.append(Paragraph(f"• {bullet_text}", body_style))
                else:
                    # Body text - format markdown
                    formatted_line = self._format_markdown_text(line)
                    story.append(Paragraph(formatted_line, body_style))
            
            # Add footer with metadata
            story.append(Spacer(1, 0.5*inch))
            footer_style = ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=8,
                textColor='#666666',
                alignment=TA_CENTER
            )
            story.append(Paragraph(
                f"Generated by AI Agentic System | {datetime.now().strftime('%B %d, %Y')}",
                footer_style
            ))
            
            # Build PDF
            doc.build(story)
            
            return {
                "success": True,
                "result": {
                    "filepath": str(filepath),
                    "content": content,
                    "filename": filename
                },
                "error": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "result": None,
                "error": str(e)
            }
    
    def _format_markdown_text(self, text: str) -> str:
        """
        Convert markdown formatting to reportlab HTML tags.
        Handles: **bold**, *italic*, and code.
        """
        import re
        
        # Bold: **text** or __text__ -> <b>text</b>
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'__(.+?)__', r'<b>\1</b>', text)
        
        # Italic: *text* or _text_ -> <i>text</i>
        text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
        text = re.sub(r'_(.+?)_', r'<i>\1</i>', text)
        
        # Code: `text` -> <font name="Courier">text</font>
        text = re.sub(r'`(.+?)`', r'<font name="Courier">\1</font>', text)
        
        return text
    
    def _generate_pdf_content(self, topic: str, style: str, context: str = "") -> str:
        """Generate PDF content using LLM."""
        style_instructions = {
            "report": "Create a professional report with an executive summary, detailed sections, and conclusions.",
            "guide": "Create a practical guide with step-by-step instructions and best practices.",
            "tutorial": "Create an educational tutorial with clear explanations and examples.",
            "whitepaper": "Create a comprehensive whitepaper with technical depth and research-backed insights."
        }
        
        instruction = style_instructions.get(style, style_instructions["report"])
        
        system_prompt = f"""You are a professional technical writer creating high-quality PDF documents.
{instruction}

Format your response with markdown-style headers:
- Use '# Title' for the main title
- Use '## Section' for section headings
- Write clear paragraphs for body text
- Ensure the content is well-structured and informative

Topic: {topic}"""
        
        if context:
            system_prompt += f"\n\nReference Context:\n{context[:3000]}"
        
        user_message = f"Create a comprehensive {style} about: {topic}"
        
        try:
            if self.llm_provider == "openai":
                response = self.llm_client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    temperature=0.7,
                    max_tokens=3000
                )
                return response.choices[0].message.content
            
            elif self.llm_provider == "anthropic":
                response = self.llm_client.messages.create(
                    model=self.model_name,
                    max_tokens=3000,
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
                        max_output_tokens=3000,
                    )
                )
                return response.text
        
        except Exception as e:
            return f"Error generating content: {e}"
