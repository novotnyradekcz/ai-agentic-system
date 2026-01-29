# RAG Pipeline - Quick Reference

## 🚀 Quick Start

**Prerequisites:** Python 3.8+, ffmpeg

```bash
# Install ffmpeg first (if not installed)
brew install ffmpeg  # macOS
# sudo apt-get install ffmpeg  # Linux

# 1. Navigate to project
cd "/Users/rano/Documents/AI Academy/HW4/rag_pipeline"

# 2. Run setup script
./setup.sh

# 3. Add your API keys to .env
cp .env.example .env
nano .env  # or use any text editor

# 4. Add your data files
cp your_file.pdf data/
cp your_audio.mp3 data/
cp your_video.mp4 data/

# 5. Run the pipeline
python main.py --interactive
```

## 📋 Common Commands

### Process all files in data/
```bash
python main.py
```

### Ask a single question
```bash
python main.py --query "What is the main topic?"
```

### Interactive Q&A mode
```bash
python main.py --interactive
```

### Process specific files
```bash
python main.py --pdf data/document.pdf --query "Summarize this"
python main.py --audio data/recording.mp3 --interactive
```

### Use different LLM provider
```bash
# Default is Gemini
python main.py --interactive

# Use OpenAI or Anthropic instead
python main.py --llm openai --interactive
python main.py --llm anthropic --interactive
```

### Reset database and start fresh
```bash
python main.py --reset
```

## 🔧 Configuration

### API Keys (in .env file)
```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
```

### Model Options

**Whisper Models** (audio transcription):
- `tiny` - Fastest, least accurate
- `base` - Default, good balance
- `small` - Better accuracy
- `medium` - High accuracy
- `large` - Best accuracy, slowest

**Embedding Models**:
- `all-MiniLM-L6-v2` - Default, fast
- `all-mpnet-base-v2` - Better quality
- `multi-qa-MiniLM-L6-cos-v1` - Optimized for Q&A

**LLM Providers**:
- `gemini` - Gemini models (default: gemini-2.5-flash) ⭐ **DEFAULT**
- `openai` - GPT models (default: gpt-3.5-turbo)
- `anthropic` - Claude models (default: claude-3-sonnet)

## 📁 Project Structure

```
rag_pipeline/
├── main.py              # Main entry point
├── examples.py          # Usage examples
├── setup.sh             # Quick setup script
├── requirements.txt     # Dependencies
├── .env                 # Your API keys
├── data/                # Your PDF/audio files
├── chroma_db/           # Vector database (auto-created)
└── modules/             # Core components
    ├── pdf_loader.py
    ├── audio_transcriber.py
    ├── text_chunker.py
    ├── vector_database.py
    └── rag_system.py
```

## 🐍 Python API Usage

```python
from modules import RAGPipeline

# Initialize
pipeline = RAGPipeline()

# Process data
chunks = pipeline.load_pdf("data/document.pdf")
pipeline.build_knowledge_base(chunks)

# Query
result = pipeline.query("Your question?")
print(result['answer'])
```

## ⚡ Performance Tips

1. **For faster audio transcription**: Use `whisper_model="tiny"`
2. **For better quality**: Use `embedding_model="all-mpnet-base-v2"`
3. **For less context**: Reduce chunk_size to 500-800
4. **For more precise answers**: Retrieve 3-5 chunks
5. **GPU acceleration**: Install CUDA-enabled PyTorch

## 🔍 Troubleshooting

### "Module not found"
```bash
pip install -r requirements.txt
```

### "API key not found"
```bash
# Make sure .env exists and has your keys
cat .env
```

### "File not found"
```bash
# Check your files are in data/
ls -la data/
```

### Reset everything
```bash
rm -rf chroma_db/ venv/
./setup.sh
```

## 📊 Example Queries

- "What is the main topic discussed?"
- "Summarize the key points"
- "Who are the main people mentioned?"
- "What conclusions were reached?"
- "Explain the methodology used"
- "What are the practical applications?"

## 🎯 Assignment Requirements Check

✅ **1. Load and Process Data**
   - PDF: `modules/pdf_loader.py`
   - Audio: `modules/audio_transcriber.py` (Whisper)

✅ **2. Chunk the Text**
   - `modules/text_chunker.py` (semantic chunking)

✅ **3. Embed and Store**
   - Embeddings: Sentence Transformers
   - Database: ChromaDB (`modules/vector_database.py`)

✅ **4. Retrieve and Generate**
   - `modules/rag_system.py` (complete RAG)

## 📝 Next Steps

1. Add your PDF and audio files to `data/`
2. Configure your API keys in `.env`
3. Run: `python main.py --interactive`
4. Start asking questions!

## 📚 Documentation

Full documentation: See [README.md](README.md)
Code examples: See [examples.py](examples.py)
