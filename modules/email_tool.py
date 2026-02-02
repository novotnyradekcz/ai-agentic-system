"""
Email Sending Tool
Tool for sending emails via Gmail API with OAuth2 authentication.
"""

from typing import Dict, Any
from modules.agent_tools import Tool
import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

# Gmail API imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


class EmailSenderTool(Tool):
    """Tool for sending emails via Gmail API with OAuth2."""
    
    def __init__(self, credentials_path: str = "credentials.json", token_path: str = "token.json"):
        """
        Initialize the Gmail API email tool.
        
        Args:
            credentials_path: Path to OAuth2 credentials file from Google Cloud Console
            token_path: Path where the OAuth2 token will be stored after authentication
        """
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = None
    
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
    
    def _get_gmail_service(self):
        """Authenticate and return Gmail API service."""
        creds = None
        
        # Check if token already exists
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
        
        # If no valid credentials, let user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception:
                    # Refresh failed, need to re-authenticate
                    creds = None
            
            if not creds:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"OAuth2 credentials file not found: {self.credentials_path}\n"
                        "Please download credentials.json from Google Cloud Console."
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
        
        return build('gmail', 'v1', credentials=creds)
    
    def execute(self, recipient: str, subject: str, body: str, is_html: bool = False, **kwargs) -> Dict[str, Any]:
        """Send email via Gmail API."""
        try:
            # Validate recipient email
            if not self._is_valid_email(recipient):
                return {
                    "success": False,
                    "result": None,
                    "error": f"Invalid recipient email address: {recipient}"
                }
            
            # Get Gmail service
            try:
                service = self._get_gmail_service()
            except FileNotFoundError as e:
                return {
                    "success": False,
                    "result": None,
                    "error": str(e)
                }
            except Exception as e:
                return {
                    "success": False,
                    "result": None,
                    "error": f"Gmail authentication failed: {str(e)}"
                }
            
            # Create message
            message = MIMEMultipart('alternative')
            message['To'] = recipient
            message['Subject'] = subject
            
            # Attach body
            if is_html:
                message.attach(MIMEText(body, 'html'))
            else:
                message.attach(MIMEText(body, 'plain'))
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            # Send via Gmail API
            send_message = service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            return {
                "success": True,
                "result": {
                    "message": f"Email sent successfully to {recipient}",
                    "recipient": recipient,
                    "subject": subject,
                    "message_id": send_message.get('id')
                },
                "error": None
            }
            
        except HttpError as e:
            return {
                "success": False,
                "result": None,
                "error": f"Gmail API error: {str(e)}"
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
