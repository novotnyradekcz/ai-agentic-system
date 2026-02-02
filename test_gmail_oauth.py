#!/usr/bin/env python3
"""
Test script for Gmail OAuth2 setup
This will verify the OAuth2 credentials are set up correctly.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from modules.email_tool import EmailSenderTool

def test_gmail_oauth():
    """Test Gmail OAuth2 authentication."""
    print("\n" + "="*80)
    print("TESTING GMAIL OAUTH2 SETUP")
    print("="*80 + "\n")
    
    try:
        # Initialize the email tool
        print("Initializing Gmail API email tool...")
        email_tool = EmailSenderTool()
        
        print("✓ Email tool initialized successfully")
        print("\nCredentials file: credentials.json")
        print("Token will be saved to: token.json")
        
        # Check if credentials file exists
        import os
        if not os.path.exists("credentials.json"):
            print("\n❌ ERROR: credentials.json not found!")
            print("Please download OAuth2 credentials from Google Cloud Console.")
            print("See README.md for setup instructions.")
            return False
        
        print("\n✓ credentials.json found")
        
        # Test authentication (this will open browser if not already authenticated)
        print("\n📝 Testing Gmail API authentication...")
        print("(A browser window may open for OAuth2 consent)")
        
        service = email_tool._get_gmail_service()
        print("\n✓ Gmail API authentication successful!")
        print("✓ token.json has been created/updated")
        
        print("\n" + "="*80)
        print("GMAIL OAUTH2 SETUP COMPLETE")
        print("="*80)
        print("\nYou can now use the email sending feature in the agent!")
        print("Example: 'Send an email to test@example.com about AI'")
        
        return True
        
    except FileNotFoundError as e:
        print(f"\n❌ ERROR: {e}")
        print("\nPlease follow the setup instructions in README.md")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nIf you're having authentication issues:")
        print("1. Make sure you enabled Gmail API in Google Cloud Console")
        print("2. Download fresh credentials.json")
        print("3. Delete token.json if it exists and try again")
        return False


if __name__ == "__main__":
    success = test_gmail_oauth()
    sys.exit(0 if success else 1)
