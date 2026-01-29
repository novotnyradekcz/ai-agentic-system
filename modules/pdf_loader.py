"""
PDF Loader Module
Extracts text content from PDF files reliably.
"""

import PyPDF2
from pathlib import Path
from typing import List, Dict


class PDFLoader:
    """Loads and extracts text from PDF files."""
    
    def __init__(self, pdf_path: str):
        """
        Initialize PDF loader.
        
        Args:
            pdf_path: Path to the PDF file
        """
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    def extract_text(self) -> str:
        """
        Extract all text from the PDF.
        
        Returns:
            Extracted text as a single string
        """
        text = ""
        
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                print(f"Processing PDF: {self.pdf_path.name}")
                print(f"Total pages: {num_pages}")
                
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    text += page_text + "\n\n"
                
                print(f"Successfully extracted {len(text)} characters")
                
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            raise
        
        return text.strip()
    
    def extract_text_by_pages(self) -> List[Dict[str, any]]:
        """
        Extract text page by page with metadata.
        
        Returns:
            List of dictionaries containing page number and text
        """
        pages_data = []
        
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    
                    pages_data.append({
                        'page_number': page_num + 1,
                        'text': page_text.strip(),
                        'source': str(self.pdf_path)
                    })
                
        except Exception as e:
            print(f"Error extracting text by pages: {e}")
            raise
        
        return pages_data


if __name__ == "__main__":
    # Example usage
    pdf_path = "../data/sample.pdf"
    
    try:
        loader = PDFLoader(pdf_path)
        text = loader.extract_text()
        print(f"\nExtracted text preview (first 500 chars):\n{text[:500]}")
    except FileNotFoundError:
        print(f"Please place a PDF file at: {pdf_path}")
