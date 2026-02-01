# 📚 AI Agentic System - Documentation Index

Welcome to the AI Agentic Educational Assistant! This index will help you navigate the documentation.

## 🚀 Getting Started

**New to the project? Start here:**

1. **[QUICKSTART.md](QUICKSTART.md)** ⚡
   - 5-minute setup guide for the agentic system
   - First tasks to try
   - API key setup instructions
   - Quick troubleshooting

2. **[README.md](README.md)** 📖
   - Complete agentic system documentation
   - Feature overview
   - Detailed usage examples
   - Configuration options

**Interested in the underlying RAG pipeline?**

- **[RAG_PIPELINE.md](RAG_PIPELINE.md)** 📚
  - Original RAG pipeline documentation
  - Foundation for the agentic system
  - Data processing and retrieval details
  - Pipeline-specific usage

## 🏗️ Understanding the System

3. **[architecture.mmd](architecture.mmd)** 🏛️
   - Visual system architecture
   - Component relationships
   - Data flow diagram
   - (View with Mermaid viewer)

4. **[WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md)** 🔄
   - Task execution flow
   - Decision-making process
   - Component interactions
   - Visual diagrams

5. **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** ✅
   - What was implemented
   - Technical details
   - Design decisions
   - Statistics and metrics

6. **[WHATS_NEW.md](WHATS_NEW.md)** 🎉
   - New features added to create agentic system
   - Comparison with RAG pipeline
   - Enhancement details

## 💻 Code & Examples

7. **[run_agent.py](run_agent.py)** 🎮
   - Main entry point for agentic system
   - Command-line interface
   - How to run the agent

8. **[run_pipeline.py](run_pipeline.py)** 🔧
   - Original RAG pipeline entry point
   - Pipeline-specific commands

9. **[examples_agent.py](examples_agent.py)** 💡
   - Agentic system examples
   - Working code examples
   - Usage demonstrations
   - Best practices
   - Run with: `python examples_agent.py`

8. **[agent.py](agent.py)** 🤖
   - Main agent orchestrator
   - Core agentic logic
   - Task execution pipeline

## 📁 Module Documentation

### Core Agent Modules

9. **modules/agent_reasoning.py** 🧠
   - Reasoning and planning
   - Reflection capabilities
   - Self-evaluation
   - Output critique

10. **modules/agent_tools.py** 🔧
    - Tool framework
    - Base tool class
    - Tool registry
    - RAG and search tools

11. **modules/agent_evaluator.py** 📊
    - Performance metrics
    - Quality scoring
    - Evaluation reports
    - Statistics tracking

12. **modules/content_tools.py** ✍️
    - Blog post generation
    - Newsletter creation
    - HTML page generation
    - Content formatting

13. **modules/email_tool.py** ✉️
    - Email sending
    - SMTP configuration
    - Email validation

### RAG Pipeline Modules (Pre-existing)

14. **modules/rag_system.py** 📚
    - RAG implementation
    - Context retrieval
    - Answer generation
    - LLM integration

15. **modules/vector_database.py** 💾
    - ChromaDB integration
    - Embedding storage
    - Similarity search

16. **modules/text_chunker.py** ✂️
    - Semantic chunking
    - Overlap management
    - Statistics

17. **modules/pdf_loader.py** 📄
    - PDF text extraction
    - Document processing

## 🎯 Quick Reference

### For Users

- **How do I start?** → [QUICKSTART.md](QUICKSTART.md)
- **What can it do?** → [README.md](README.md) (Features section)
- **How do I use it?** → [README.md](README.md) (Usage Examples)
- **How does it work?** → [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md)

### For Developers

- **System architecture?** → [architecture.mmd](architecture.mmd)
- **How to add tools?** → [modules/agent_tools.py](modules/agent_tools.py)
- **How reasoning works?** → [modules/agent_reasoning.py](modules/agent_reasoning.py)
- **Evaluation system?** → [modules/agent_evaluator.py](modules/agent_evaluator.py)

### For Reviewers

- **What was built?** → [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
- **Technical stack?** → [README.md](README.md) (Architecture section)
- **Design decisions?** → [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) (Design Decisions)

## 📋 File Organization

```
ai_agentic_system/
│
├── 📘 Documentation
│   ├── README.md                    # Main agentic system docs
│   ├── RAG_PIPELINE.md              # RAG pipeline docs (foundation)
│   ├── QUICKSTART.md                # Quick start guide
│   ├── WORKFLOW_GUIDE.md            # Visual workflows
│   ├── IMPLEMENTATION_SUMMARY.md    # Implementation details
│   ├── WHATS_NEW.md                 # New features list
│   ├── DEFAULT_LLM.md               # LLM configuration
│   ├── INDEX.md                     # This file
│   └── architecture.mmd             # Architecture diagram
│
├── 🚀 Executable Files
│   ├── run_agent.py                 # Agentic system entry point
│   ├── run_pipeline.py              # RAG pipeline entry point
│   ├── agent.py                     # Agent orchestrator
│   ├── examples_agent.py            # Agent usage examples
│   ├── examples_pipeline.py         # Pipeline usage examples
│   └── setup_pipeline.sh            # Pipeline setup script
│
├── 🧩 Core Modules
│   └── modules/
│       ├── agent_reasoning.py       # Reasoning & reflection
│       ├── agent_tools.py           # Tool framework
│       ├── agent_evaluator.py       # Evaluation & metrics
│       ├── content_tools.py         # Content generation
│       ├── email_tool.py            # Email sending
│       ├── rag_system.py            # RAG implementation
│       ├── vector_database.py       # Vector DB
│       ├── text_chunker.py          # Text chunking
│       └── pdf_loader.py            # PDF processing
│
├── 📂 Data & Output
│   ├── data/                        # Input documents
│   ├── outputs/                     # Generated content
│   └── logs/                        # Evaluation reports
│
└── ⚙️ Configuration
    ├── requirements.txt             # Dependencies
    ├── .env.example                 # Environment template
    └── .gitignore                   # Git ignore rules
```

## 🎓 Learning Path

### Beginner Path
1. Start with [QUICKSTART.md](QUICKSTART.md)
2. Run the agent and try simple tasks
3. Read [README.md](README.md) Features section
4. Experiment with different tasks

### Intermediate Path
1. Read [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md)
2. Run [examples_agent.py](examples_agent.py)
3. View [architecture.mmd](architecture.mmd)
4. Understand component interactions

### Advanced Path
1. Study [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
2. Review module source code
3. Understand evaluation metrics
4. Extend with new tools

## 🔗 External Resources

### API Documentation
- **Google Gemini**: https://ai.google.dev/docs
- **OpenAI**: https://platform.openai.com/docs
- **Anthropic**: https://docs.anthropic.com/

### Libraries Used
- **LangChain**: https://python.langchain.com/
- **ChromaDB**: https://docs.trychroma.com/
- **Sentence Transformers**: https://www.sbert.net/

## 📞 Support & Help

### Common Issues
- **API Key Problems** → [QUICKSTART.md](QUICKSTART.md) (Troubleshooting)
- **Installation Issues** → Check [requirements.txt](requirements.txt)
- **Usage Questions** → [README.md](README.md) (Usage Examples)
- **Understanding Flow** → [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md)

### Getting Help
1. Check documentation in this index
2. Review [README.md](README.md)
3. Look at [examples_agent.py](examples_agent.py)
4. Use `tools` and `stats` commands in CLI

## 📝 Notes

- All `.md` files are in Markdown format
- `.mmd` file requires Mermaid viewer
- Python files are well-commented
- Examples are runnable as-is

## 🎯 Quick Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the agent (default: Gemini)
python run_agent.py

# Run with different LLM
python run_agent.py --llm openai

# Run examples
python examples_agent.py

# See all options
python run_agent.py --help
```

## ✨ What's Unique

This system combines:
- ✅ **RAG** for knowledge retrieval
- ✅ **Reasoning** for task planning
- ✅ **Tools** for actions
- ✅ **Reflection** for self-improvement
- ✅ **Evaluation** for performance tracking

## 🎓 Educational Value

Perfect for learning:
- Agentic AI systems
- RAG architectures
- LLM integration
- Tool-based design
- Performance evaluation

---

**Ready to start?** → [QUICKSTART.md](QUICKSTART.md) ⚡

**Questions?** → [README.md](README.md) 📖

**Want to understand deeply?** → [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md) 🔄
