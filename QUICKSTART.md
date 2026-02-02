# 🚀 Quick Start Guide - AI Agentic System

## 5-Minute Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up API Key
Create a `.env` file:
```bash
cp .env.example .env
```

Edit `.env` and add at least one API key:
```
GOOGLE_API_KEY=your_actual_key_here
```

### 3. Add Documents (Optional)
```bash
# Place PDF files in data/ directory
cp your_documents.pdf data/
```

### 4. Run the Agent
```bash
python run_agent.py
```

## First Tasks to Try

Once running, try these commands:

### Simple Q&A
```
🤖 Task: What is artificial intelligence?
```

### Generate Content
```
🤖 Task: Create a short social media post about machine learning
```

### Check System
```
🤖 Task: tools
🤖 Task: stats
```

## Command-Line Options

```bash
# Use different LLM provider
python run_agent.py --llm openai

# Specify model
python run_agent.py --llm openai --model gpt-4

# Custom data directory
python run_agent.py --data-dir ./my_docs

# See all options
python run_agent.py --help
```

## Getting API Keys

### Google Gemini (Free & Recommended)
1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy key to `.env`

### OpenAI
1. Go to: https://platform.openai.com/api-keys
2. Sign up/Login
3. Create new secret key
4. Copy to `.env`

### Anthropic Claude
1. Go to: https://console.anthropic.com/
2. Sign up/Login
3. Settings → API Keys → Create Key
4. Copy to `.env`

## Gmail OAuth2 Setup (Optional)

For email sending with Gmail API:

1. **Create Google Cloud Project:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create/select project
   - Enable Gmail API

2. **Create OAuth2 Credentials:**
   - APIs & Services → Credentials
   - Create Credentials → OAuth client ID
   - Choose "Desktop app"
   - Download as `credentials.json` (save in project root)

3. **First-time authentication:**
   - Run the test script: `python test_gmail_oauth.py`
   - Browser will open for Gmail authorization
   - Sign in and grant permissions
   - `token.json` will be created automatically

> **Security:** Both `credentials.json` and `token.json` are excluded from git.

## Troubleshooting

**"API key not found"**
- Check `.env` file exists
- Verify key is correct
- No spaces around `=`

**"No module named..."**
- Run: `pip install -r requirements.txt`

**"Vector database error"**
- Delete `chroma_db` folder
- Restart agent

**"Gmail authentication failed"**
- Ensure Gmail API is enabled in Google Cloud Console
- Delete `token.json` and re-authenticate
- Check `credentials.json` is valid and in project root
- Run `python test_gmail_oauth.py` to test setup

## What Next?

- Read full documentation: [README.md](README.md)
- View architecture: [architecture.mmd](architecture.mmd)
- Check examples in the README

## Examples

### Generate and Email Newsletter
```
🤖 Task: Create a newsletter about neural networks and email it to student@example.com
```

### Create HTML Page
```
🤖 Task: Generate an HTML page about deep learning
```

### Knowledge Base Query
```
🤖 Task: What are the key concepts in the documents?
```

---

**Need help?** Check [README.md](README.md) for detailed documentation.
