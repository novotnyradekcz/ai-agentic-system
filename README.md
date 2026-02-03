# 🤖 AI Agentic Educational Assistant

An intelligent AI agent system created as part of the **Ciklum AI Academy** capstone project. This system combines **Retrieval-Augmented Generation (RAG)**, **autonomous reasoning**, **tool-based actions**, and **self-reflection** to create a powerful educational assistant.

## 🌟 Core Capabilities

This system focuses on 4 essential capabilities:

### 📚 1. Question Answering (RAG)
- Answer questions using documents from the `data/` folder
- Semantic search with ChromaDB vector database
- Context-aware responses with source citations
- Supports both knowledge base and general knowledge questions

**Example:** *"What is retrieval-augmented generation?"*

### 📧 2. Email Communication
- Draft and send emails via Gmail API with OAuth2
- Intelligent content generation based on topic
- Automatic subject line inference
- Secure authentication (no passwords stored)

**Example:** *"Send an email about RAG to user@example.com"*

### 📄 3. PDF Document Creation
- Generate professional PDF documents automatically saved to `outputs/` folder
- 4 styles: report, guide, tutorial, whitepaper
- Content from your data or general knowledge
- Proper markdown formatting (headings, bold, italic, lists)

**Example:** *"Create a PDF guide about machine learning"*

### 🌐 4. HTML Page Generation
- Build complete, styled HTML pages automatically saved to `outputs/` folder
- Responsive design with gradient backgrounds
- Content from your data or general knowledge
- Proper markdown formatting (bold, italic, lists, links, code)

**Example:** *"Create an HTML page about neural networks"*

## 🏗️ Architecture

The system uses a 5-phase agentic process:

```
User Input → 🧠 Reasoning → 🔧 Tool Selection → ⚡ Execution → 🔍 Reflection → 📊 Evaluation → Output
```

### Advanced Features

1. **🧠 Autonomous Reasoning**
   - Task understanding and breakdown
   - Step-by-step planning before execution
   - Intelligent tool selection

2. **🔍 Self-Reflection**
   - Automatic evaluation of outcomes
   - Identification of strengths and weaknesses
   - Learning from results

3. **📊 Performance Tracking**
   - Real-time success rate monitoring
   - Quality scoring and metrics
   - Comprehensive evaluation reports

## 🔒 Security

This system implements secure practices:

- **OAuth2 Authentication**: Email sending uses Gmail API with OAuth2 (no passwords stored)
- **Credential Protection**: Sensitive files (`credentials.json`, `token.json`, `.env`) are automatically excluded from version control via `.gitignore`
- **API Key Management**: LLM API keys stored in `.env` file (not in code)
- **Token Refresh**: OAuth2 tokens automatically refresh without re-authentication

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- **FFmpeg** (required for audio/video transcription)
  - macOS: `brew install ffmpeg`
  - Ubuntu/Debian: `sudo apt-get install ffmpeg`
  - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)
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

### 📚 Question Answering
```
🤖 Task: What is retrieval-augmented generation?
🤖 Task: Explain machine learning in simple terms
🤖 Task: What are the benefits of RAG systems?
```

### 📧 Email Communication
```
🤖 Task: Send an email about RAG to user@example.com
🤖 Task: Email colleague@company.com introducing yourself
🤖 Task: Send a short email about machine learning to student@university.edu
```

### 📄 PDF Creation (automatically saves to outputs/)
```
🤖 Task: Create a PDF guide about neural networks
🤖 Task: Generate a PDF report on transformers
🤖 Task: Make a PDF tutorial about RAG
```

### 🌐 HTML Page Generation (automatically saves to outputs/)
```
🤖 Task: Create an HTML page about artificial intelligence
🤖 Task: Build an HTML page explaining deep learning
🤖 Task: Generate an HTML page about vector databases
```

### System Commands
```
🤖 Task: Who are you?    # Learn about the agent
🤖 Task: tools           # List all available tools
🤖 Task: stats           # Show performance statistics
🤖 Task: quit            # Exit the agent
```

## 🛠️ Available Tools

The agent has access to 5 specialized tools:

1. **rag_query**: Answer questions using knowledge base with RAG
2. **knowledge_search**: Retrieve information from knowledge base
3. **generate_html**: Create HTML pages (saved to outputs/)
4. **generate_pdf**: Generate PDF documents (saved to outputs/)
5. **send_email**: Send emails via Gmail API with OAuth2

**Note:** HTML and PDF tools automatically save files to the `outputs/` folder with timestamps.

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
- Generate study guides and summaries (as PDF or HTML)
- Create practice questions

### Content Creator
- Generate HTML pages from research papers
- Create PDF documents for distribution
- Produce professional reports and guides

### Knowledge Management
- Search through documentation
- Synthesize information from multiple sources
- Create reference materials (PDF or HTML)

## 🔐 Security Notes

- Never commit your `.env` file
- Use app-specific passwords for email
- Keep API keys secure
- Review generated content before publishing

## 📈 Future Enhancements

Potential improvements:

- [ ] Web browsing capability for real-time information
- [ ] Multi-turn conversations with memory
- [ ] Image generation and analysis
- [ ] Code execution and testing
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
