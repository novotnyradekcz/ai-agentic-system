"""
Email Sending Tool
Tool for sending emails with generated content.
"""

from typing import Dict, Any
from modules.agent_tools import Tool
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()


class EmailSenderTool(Tool):
    """Tool for sending emails."""
    
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")
    
    @property
    def name(self) -> str:
        return "send_email"
    
    @property
    def description(self) -> str:
        return "Send an email with content. Requires recipient email address, subject, and message body."
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "recipient": "str - Recipient email address",
            "subject": "str - Email subject line",
            "body": "str - Email body content",
            "is_html": "bool - Whether body is HTML formatted (default: False)"
        }
    
    def execute(self, recipient: str, subject: str, body: str, is_html: bool = False, **kwargs) -> Dict[str, Any]:
        """Send email."""
        try:
            # Validate configuration
            if not self.sender_email or not self.sender_password:
                return {
                    "success": False,
                    "result": None,
                    "error": "Email credentials not configured. Please set SENDER_EMAIL and SENDER_PASSWORD in .env file."
                }
            
            # Validate recipient email
            if not self._is_valid_email(recipient):
                return {
                    "success": False,
                    "result": None,
                    "error": f"Invalid recipient email address: {recipient}"
                }
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.sender_email
            msg['To'] = recipient
            msg['Subject'] = subject
            
            # Attach body
            if is_html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            return {
                "success": True,
                "result": {
                    "message": f"Email sent successfully to {recipient}",
                    "recipient": recipient,
                    "subject": subject
                },
                "error": None
            }
        except smtplib.SMTPAuthenticationError:
            return {
                "success": False,
                "result": None,
                "error": "Email authentication failed. Check your email credentials."
            }
        except smtplib.SMTPException as e:
            return {
                "success": False,
                "result": None,
                "error": f"SMTP error: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "result": None,
                "error": str(e)
            }
    
    def _is_valid_email(self, email: str) -> bool:
        """Basic email validation."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
