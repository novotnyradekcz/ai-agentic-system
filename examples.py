"""
Example Usage Script
Demonstrates various ways to use the RAG pipeline.
"""

import sys
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent))

from modules import (
    PDFLoader,
    AudioTranscriber,
    TextChunker,
    VectorDatabase,
    RAGSystem
)


def example_1_simple_pipeline():
    """Example 1: Simple end-to-end pipeline."""
    print("\n" + "="*80)
    print("Example 1: Simple Pipeline")
    print("="*80)
    
    # Initialize components
    chunker = TextChunker(chunk_size=500, chunk_overlap=50)
    db = VectorDatabase(collection_name="example_1")
    
    # Sample text
    sample_text = """
    Machine learning is a subset of artificial intelligence that focuses on 
    enabling computers to learn from data. Deep learning, a specialized form 
    of machine learning, uses neural networks with multiple layers.
    
    Natural language processing (NLP) is another AI field that deals with 
    understanding and generating human language. Modern NLP systems use 
    transformer architectures like BERT and GPT.
    """
    
    # Process
    chunks = chunker.chunk_text(sample_text, metadata={'source': 'example'})
    db.add_documents(chunks)
    
    # Query
    rag = RAGSystem(vector_db=db)
    result = rag.answer_question("What is deep learning?")
    
    print(f"\nAnswer: {result['answer']}")


def example_2_pdf_processing():
    """Example 2: Process a PDF file."""
    print("\n" + "="*80)
    print("Example 2: PDF Processing")
    print("="*80)
    
    pdf_path = "data/sample.pdf"
    
    if not Path(pdf_path).exists():
        print(f"⚠️  PDF not found at: {pdf_path}")
        print("Please add a PDF file to test this example.")
        return
    
    # Load PDF
    loader = PDFLoader(pdf_path)
    text = loader.extract_text()
    print(f"Extracted {len(text)} characters from PDF")
    
    # Chunk and store
    chunker = TextChunker()
    chunks = chunker.chunk_text(text, metadata={'source': 'sample.pdf'})
    
    db = VectorDatabase(collection_name="example_2")
    db.add_documents(chunks)
    
    # Query
    rag = RAGSystem(vector_db=db)
    result = rag.answer_question("What is this document about?")
    
    print(f"\nAnswer: {result['answer']}")


def example_3_audio_transcription():
    """Example 3: Transcribe audio file."""
    print("\n" + "="*80)
    print("Example 3: Audio Transcription")
    print("="*80)
    
    audio_path = "data/sample_audio.mp3"
    
    if not Path(audio_path).exists():
        print(f"⚠️  Audio not found at: {audio_path}")
        print("Please add an audio file to test this example.")
        return
    
    # Transcribe
    transcriber = AudioTranscriber(model_size="tiny")  # Use tiny for speed
    result = transcriber.transcribe_audio(audio_path)
    
    print(f"Transcribed {len(result['text'])} characters")
    print(f"Language: {result['language']}")
    
    # Chunk and store
    chunker = TextChunker()
    chunks = chunker.chunk_text(result['text'], metadata={'source': 'audio'})
    
    db = VectorDatabase(collection_name="example_3")
    db.add_documents(chunks)
    
    print(f"Created {len(chunks)} chunks from audio")


def example_4_custom_configuration():
    """Example 4: Custom configuration."""
    print("\n" + "="*80)
    print("Example 4: Custom Configuration")
    print("="*80)
    
    # Custom chunker settings
    chunker = TextChunker(
        chunk_size=300,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". "]
    )
    
    # Custom vector DB settings
    db = VectorDatabase(
        collection_name="custom_collection",
        embedding_model="all-mpnet-base-v2",  # Better quality embeddings
        persist_directory="./custom_db"
    )
    
    # Custom RAG settings
    rag = RAGSystem(
        vector_db=db,
        llm_provider="anthropic",  # Use Claude instead of GPT
        temperature=0.3,           # More deterministic
        max_tokens=500             # Shorter responses
    )
    
    print("✓ Custom configuration loaded")


def example_5_batch_processing():
    """Example 5: Process multiple documents."""
    print("\n" + "="*80)
    print("Example 5: Batch Processing")
    print("="*80)
    
    documents = [
        {
            'text': 'Python is a high-level programming language.',
            'source': 'doc1.txt',
            'author': 'Alice'
        },
        {
            'text': 'JavaScript is used for web development.',
            'source': 'doc2.txt',
            'author': 'Bob'
        },
        {
            'text': 'SQL is a language for database queries.',
            'source': 'doc3.txt',
            'author': 'Charlie'
        }
    ]
    
    # Process all documents
    chunker = TextChunker()
    all_chunks = chunker.chunk_documents(documents)
    
    print(f"Processed {len(documents)} documents into {len(all_chunks)} chunks")
    
    # Store in database
    db = VectorDatabase(collection_name="example_5")
    db.add_documents(all_chunks)
    
    # Query across all documents
    rag = RAGSystem(vector_db=db)
    result = rag.answer_question("What programming languages are mentioned?")
    
    print(f"\nAnswer: {result['answer']}")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("RAG Pipeline - Usage Examples")
    print("="*80)
    
    try:
        example_1_simple_pipeline()
        # example_2_pdf_processing()
        # example_3_audio_transcription()
        # example_4_custom_configuration()
        example_5_batch_processing()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have:")
        print("1. Installed all dependencies: pip install -r requirements.txt")
        print("2. Set up your .env file with API keys")
        print("3. Added sample data files if testing examples 2 or 3")
