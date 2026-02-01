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

## Email Setup (Optional)

For Gmail:
1. Enable 2-factor authentication
2. Go to: https://myaccount.google.com/apppasswords
3. Create app password
4. Add to `.env`:
```
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
```

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
