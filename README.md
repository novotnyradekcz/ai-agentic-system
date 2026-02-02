# 🤖 AI Agentic Educational Assistant

An intelligent AI agent system that combines **Retrieval-Augmented Generation (RAG)**, **autonomous reasoning**, **tool-based actions**, **self-reflection**, and **performance evaluation** to create an educational assistant capable of answering questions, generating content, and taking meaningful actions.

## 🌟 Features

### Core Agentic Capabilities

1. **🧠 Reasoning & Planning**
   - Autonomous task understanding and breakdown
   - Step-by-step planning before execution
   - Intelligent tool selection based on task requirements

2. **🔧 Tool-Based Actions**
   - RAG query for knowledge base retrieval
   - Content generation (blog posts, newsletters, HTML pages)
   - Email sending capabilities
   - Knowledge search without generation

3. **🔍 Reflection & Self-Correction**
   - Automatic evaluation of actions and outcomes
   - Identification of strengths and weaknesses
   - Alternative approach suggestions for failures

4. **📊 Evaluation & Metrics**
   - Real-time performance tracking
   - Success rate monitoring
   - Quality scoring (efficiency, tool usage, reflection quality)
   - Comprehensive evaluation reports

5. **📚 RAG Pipeline**
   - PDF document processing
   - Semantic chunking and embedding
   - Vector database storage (ChromaDB)
   - Context-aware answer generation

## 🏗️ Architecture

The system follows a modular architecture with clear separation of concerns:

```
User Input → Reasoning → Tool Selection → Execution → Reflection → Evaluation → Output
```

See [architecture.mmd](architecture.mmd) for detailed component diagram.

### Key Components

- **Agent Orchestrator** (`agent.py`): Main coordination logic
- **Reasoning Module** (`modules/agent_reasoning.py`): Think, plan, reflect
- **Tool Registry** (`modules/agent_tools.py`): Tool management and execution
- **Content Tools** (`modules/content_tools.py`): Content generation capabilities
- **Email Tool** (`modules/email_tool.py`): Secure email via Gmail API with OAuth2
- **Evaluator** (`modules/agent_evaluator.py`): Performance measurement
- **RAG System** (`modules/rag_system.py`): Retrieval and generation

## 🔒 Security

This system implements secure practices:

- **OAuth2 Authentication**: Email sending uses Gmail API with OAuth2 (no passwords stored)
- **Credential Protection**: Sensitive files (`credentials.json`, `token.json`, `.env`) are automatically excluded from version control via `.gitignore`
- **API Key Management**: LLM API keys stored in `.env` file (not in code)
- **Token Refresh**: OAuth2 tokens automatically refresh without re-authentication

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- API key for at least one LLM provider:
  - Google Gemini (recommended, default)
  - OpenAI
  - Anthropic Claude

### Installation

1. **Clone or navigate to the project:**
```bash
cd ai_agentic_system
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**

Create a `.env` file in the project root:

```bash
# LLM API Keys (at least one required)
GOOGLE_API_KEY=your_google_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

4. **Set up Gmail API for email sending (optional):**

If you want to use the email sending feature, you need to set up OAuth2 authentication with Gmail API:

**a. Create a Google Cloud Project:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Gmail API:
     - Navigate to "APIs & Services" → "Library"
     - Search for "Gmail API" and enable it

**b. Create OAuth2 Credentials:**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Choose "Desktop app" as the application type
   - Download the credentials JSON file
   - Save it as `credentials.json` in the project root directory
   - (See `credentials.json.example` for expected structure)

**c. First-time authentication:**
   - Run the test script: `python test_gmail_oauth.py`
   - Or wait for first email task - a browser window will open automatically
   - Sign in with your Gmail account
   - Grant the necessary permissions
   - A `token.json` file will be created automatically for future use

> **Note:** Both `credentials.json` and `token.json` are automatically excluded from git via `.gitignore` for security.

5. **Add your documents to the data folder:**
```bash
# Place PDF files in the data/ directory
cp your_documents.pdf data/
```

### Running the Agent

**Basic usage with Google Gemini (default):**
```bash
python run_agent.py
```

**Use OpenAI:**
```bash
python run_agent.py --llm openai --model gpt-4
```

**Use Anthropic Claude:**
```bash
python run_agent.py --llm anthropic --model claude-3-opus-20240229
```

**Custom data directory:**
```bash
python run_agent.py --data-dir ./my_documents
```

## 💡 Usage Examples

Once the agent is running in interactive mode, you can give it various tasks:

### Knowledge Base Queries
```
🤖 Task: What is machine learning?
🤖 Task: Explain neural networks in simple terms
```

### Content Generation
```
🤖 Task: Create a professional blog post about artificial intelligence
🤖 Task: Generate a social media post about deep learning
🤖 Task: Write a newsletter about the latest AI trends
🤖 Task: Create an HTML page about natural language processing
```

### Combined Actions
```
🤖 Task: Create a newsletter about machine learning and email it to student@example.com
🤖 Task: Generate a technical blog post about transformers
```

### System Commands
```
🤖 Task: tools          # List all available tools
🤖 Task: stats          # Show performance statistics
🤖 Task: save           # Save evaluation report
🤖 Task: quit           # Exit the agent
```

## 🛠️ Available Tools

The agent has access to the following tools:

1. **rag_query**: Query the knowledge base with RAG
2. **knowledge_search**: Search knowledge base (retrieval only)
3. **generate_blog_post**: Create blog posts and social media content
4. **generate_newsletter**: Generate newsletter-style content
5. **generate_html**: Create HTML web pages
6. **send_email**: Send emails with generated content

## 📊 How It Works

### Task Execution Flow

1. **Reasoning Phase**
   - Agent analyzes the task
   - Breaks it into steps
   - Identifies required tools
   - Creates execution plan

2. **Tool Selection**
   - Evaluates available tools
   - Selects most appropriate ones
   - Determines execution sequence

3. **Execution Phase**
   - Runs selected tools with extracted parameters
   - Handles errors gracefully
   - Collects results

4. **Reflection Phase**
   - Analyzes outcomes
   - Identifies successes and failures
   - Suggests improvements
   - Determines if retry is needed

5. **Evaluation Phase**
   - Measures task success
   - Calculates quality scores
   - Updates performance metrics
   - Tracks tool usage

## 🧪 Evaluation Metrics

The system tracks the following metrics:

- **Success Rate**: Percentage of successful task completions
- **Efficiency Score**: How economically the agent uses reasoning steps
- **Tool Usage Score**: Appropriateness of tool selection
- **Reflection Quality**: Depth and usefulness of self-reflection
- **Overall Performance**: Weighted combination of all metrics

View metrics anytime with the `stats` command, or save a detailed report with `save`.

## 📁 Project Structure

```
ai_agentic_system/
├── run_agent.py              # Main entry point
├── agent.py                  # Agentic system orchestrator
├── run_pipeline.py           # Original RAG pipeline
├── requirements.txt          # Dependencies
├── architecture.mmd          # System architecture diagram
├── README.md                 # This file
├── .env                      # Environment variables (create this)
│
├── modules/
│   ├── agent_reasoning.py    # Reasoning & reflection
│   ├── agent_tools.py        # Tool framework & base tools
│   ├── agent_evaluator.py    # Performance evaluation
│   ├── content_tools.py      # Content generation tools
│   ├── email_tool.py         # Email sending tool
│   ├── rag_system.py         # RAG implementation
│   ├── vector_database.py    # Vector DB (ChromaDB)
│   ├── text_chunker.py       # Text chunking
│   ├── pdf_loader.py         # PDF processing
│   └── audio_transcriber.py  # Audio transcription
│
├── data/                     # Place your PDF documents here
├── outputs/                  # Generated content (auto-created)
└── logs/                     # Evaluation reports (auto-created)
```

## 🔧 Configuration

### LLM Providers

The system supports three LLM providers with easy switching:

**Google Gemini (Default)**
- Fast and cost-effective
- Model: `gemini-2.5-flash` (default) or `gemini-2.5-pro`
- Requires: `GOOGLE_API_KEY`

**OpenAI**
- Industry standard
- Models: `gpt-3.5-turbo`, `gpt-4`, `gpt-4-turbo`
- Requires: `OPENAI_API_KEY`

**Anthropic Claude**
- Strong reasoning capabilities
- Models: `claude-3-sonnet-20240229`, `claude-3-opus-20240229`
- Requires: `ANTHROPIC_API_KEY`

### Email Configuration

For the email sending feature:

1. Use an app-specific password (not your main password)
2. For Gmail:
   - Enable 2-factor authentication
   - Generate app password at: https://myaccount.google.com/apppasswords
3. Add credentials to `.env` file

## 🎯 Use Cases

### Educational Assistant
- Answer student questions from course materials
- Generate study guides and summaries
- Create practice questions

### Content Creator
- Generate blog posts from research papers
- Create social media content
- Produce newsletters

### Knowledge Management
- Search through documentation
- Synthesize information from multiple sources
- Create reference materials

## 🔐 Security Notes

- Never commit your `.env` file
- Use app-specific passwords for email
- Keep API keys secure
- Review generated content before publishing

## 📈 Future Enhancements

Potential improvements:

- [ ] PDF generation for reports and slides
- [ ] Web browsing capability for real-time information
- [ ] Multi-turn conversations with memory
- [ ] Fine-tuning on specific educational domains
- [ ] Web-based UI interface
- [ ] Advanced scheduling and automation
- [ ] Integration with more tools (databases, APIs)
- [ ] Multi-modal support (images, audio)

## 🤝 Contributing

This is an educational project. Feel free to:
- Add new tools
- Improve reasoning algorithms
- Enhance evaluation metrics
- Add new content generation formats

## 📝 License

Educational project for AI Academy Capstone.

## 🙏 Acknowledgments

Built on top of:
- LangChain for text processing
- ChromaDB for vector storage
- Sentence Transformers for embeddings
- OpenAI, Anthropic, and Google for LLM APIs

## 📞 Support

For issues or questions:
1. Check the architecture diagram
2. Review the evaluation logs
3. Use the `tools` command to see available capabilities
4. Check performance with `stats` command

---

**Happy Learning! 🚀**
