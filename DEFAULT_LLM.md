# Default LLM Configuration

> **Note**: This document describes LLM configuration for the **RAG Pipeline**. For the AI Agentic System, see [README.md](README.md).

## 🎯 Google Gemini is the Default LLM

As of this configuration, **Google Gemini** is set as the default LLM provider for both the RAG pipeline and the agentic system.

### Why Gemini as Default?

- ✅ **Fast Performance**: Gemini-2.5-flash offers excellent speed
- ✅ **Cost-Effective**: Competitive pricing for API usage
- ✅ **Good Quality**: Strong performance on RAG tasks

### Current Default Settings

```python
LLM Provider: gemini
Default Model: gemini-2.5-flash
```

## 🔄 Switching LLM Providers

You can easily switch to a different provider:

### RAG Pipeline

```bash
# Use default (Gemini)
python run_pipeline.py --interactive

# Switch to OpenAI
python run_pipeline.py --llm openai --interactive

# Switch to Anthropic Claude
python run_pipeline.py --llm anthropic --interactive
```

### Agentic System

```bash
# Use default (Gemini)
python run_agent.py

# Switch to OpenAI
python run_agent.py --llm openai

# Switch to Anthropic Claude
python run_agent.py --llm anthropic
```

### In Python Code

```python
from modules import RAGPipeline

# Use Gemini (default)
pipeline = RAGPipeline()

# Use OpenAI
pipeline = RAGPipeline(llm_provider="openai")

# Use Anthropic
pipeline = RAGPipeline(llm_provider="anthropic")
```

## 🔑 Required API Keys

Make sure your `.env` file has the appropriate key:

```bash
# For Gemini (default)
GOOGLE_API_KEY=your_google_api_key_here

# For OpenAI (optional)
OPENAI_API_KEY=your_openai_key_here

# For Anthropic (optional)
ANTHROPIC_API_KEY=your_anthropic_key_here
```

## 📊 Provider Comparison

| Provider | Default Model | Speed | Cost | Best For |
|----------|--------------|-------|------|----------|
| **Gemini** ⭐ | gemini-2.5-flash | ⚡⚡⚡ | 💰💰 | Fast, general-purpose RAG |
| OpenAI | gpt-3.5-turbo | ⚡⚡ | 💰💰 | Balanced performance |
| Anthropic | claude-3-sonnet | ⚡⚡ | 💰💰💰 | Long context, detailed answers |

## 🎓 Getting Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and add it to your `.env` file

## 💡 Tips

- **Free tier available**: Gemini offers generous free usage
- **No credit card required**: Start testing immediately
- **Fast setup**: Get your key in seconds
- **Great for learning**: Perfect for educational projects like this one

## 🔄 Changing the Default

To change the default LLM provider, edit [main.py](main.py) line 249:

```python
parser.add_argument(
    '--llm',
    type=str,
    default='gemini',  # Change this to 'openai' or 'anthropic'
    choices=['openai', 'anthropic', 'gemini'],
    help='LLM provider to use (default: gemini)'
)
```
