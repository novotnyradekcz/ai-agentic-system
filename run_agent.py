#!/usr/bin/env python3
"""
Run the AI Agentic System
Main entry point for the agentic educational assistant.
"""

import os
import sys
import argparse
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent))

from agent import AgenticSystem
from modules.vector_database import VectorDatabase
from modules.text_chunker import TextChunker
from modules.pdf_loader import PDFLoader


def setup_knowledge_base(data_dir: str, collection_name: str = "agent_kb"):
    """
    Setup the knowledge base from data directory.
    
    Args:
        data_dir: Directory containing PDF files
        collection_name: Name for the vector database collection
        
    Returns:
        VectorDatabase instance
    """
    print("\n" + "="*80)
    print("SETTING UP KNOWLEDGE BASE")
    print("="*80)
    
    data_path = Path(data_dir)
    if not data_path.exists():
        print(f"⚠️  Warning: Data directory not found: {data_dir}")
        print("Creating empty knowledge base...")
        return VectorDatabase(collection_name=collection_name)
    
    # Initialize components
    vector_db = VectorDatabase(collection_name=collection_name)
    text_chunker = TextChunker(chunk_size=1000, chunk_overlap=200)
    
    # Process all PDFs
    pdf_files = list(data_path.glob("*.pdf"))
    
    if not pdf_files:
        print(f"⚠️  No PDF files found in {data_dir}")
        print("Agent will work without knowledge base context.")
        return vector_db
    
    print(f"\nFound {len(pdf_files)} PDF files")
    
    all_chunks = []
    for pdf_file in pdf_files:
        print(f"  Processing: {pdf_file.name}")
        try:
            loader = PDFLoader(str(pdf_file))
            text = loader.extract_text()
            
            chunks = text_chunker.chunk_text(
                text,
                metadata={'source': pdf_file.name, 'type': 'pdf'}
            )
            all_chunks.extend(chunks)
            print(f"    ✓ Created {len(chunks)} chunks")
        except Exception as e:
            print(f"    ✗ Error: {e}")
    
    if all_chunks:
        print(f"\nAdding {len(all_chunks)} chunks to knowledge base...")
        vector_db.add_documents(all_chunks)
        stats = vector_db.get_collection_stats()
        print(f"✓ Knowledge base ready with {stats['total_documents']} documents")
    
    print("="*80 + "\n")
    return vector_db


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="AI Agentic Educational Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default settings (Gemini)
  python run_agent.py
  
  # Use OpenAI
  python run_agent.py --llm openai --model gpt-4
  
  # Use Anthropic
  python run_agent.py --llm anthropic --model claude-3-opus-20240229
  
  # Custom data directory
  python run_agent.py --data-dir ./my_documents
        """
    )
    
    parser.add_argument(
        '--llm',
        type=str,
        default='gemini',
        choices=['openai', 'anthropic', 'gemini'],
        help='LLM provider (default: gemini)'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        default=None,
        help='Specific model name (optional)'
    )
    
    parser.add_argument(
        '--data-dir',
        type=str,
        default='data',
        help='Directory containing knowledge base documents (default: data)'
    )
    
    parser.add_argument(
        '--collection',
        type=str,
        default='agent_kb',
        help='Vector database collection name (default: agent_kb)'
    )
    
    parser.add_argument(
        '--temperature',
        type=float,
        default=0.7,
        help='LLM temperature (default: 0.7)'
    )
    
    args = parser.parse_args()
    
    # Check for API keys
    llm_key_map = {
        'openai': 'OPENAI_API_KEY',
        'anthropic': 'ANTHROPIC_API_KEY',
        'gemini': 'GOOGLE_API_KEY'
    }
    
    required_key = llm_key_map[args.llm]
    if not os.getenv(required_key):
        print(f"❌ Error: {required_key} not found in environment variables")
        print(f"Please set it in your .env file")
        sys.exit(1)
    
    try:
        # Setup knowledge base
        vector_db = setup_knowledge_base(args.data_dir, args.collection)
        
        # Initialize agent
        agent = AgenticSystem(
            vector_db=vector_db,
            llm_provider=args.llm,
            model_name=args.model,
            temperature=args.temperature
        )
        
        # Start interactive mode
        agent.interactive_mode()
    
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
