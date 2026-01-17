# helper_functions.py
# Utility functions for processing Harry Potter PDF and text data

import re
from typing import List
from langchain.docstore.document import Document
from langchain.document_loaders import PyPDFLoader


def split_into_chapters(pdf_path: str) -> List[Document]:
    """
    Split Harry Potter PDF into chapters based on chapter headings.
    Expects format: "CHAPTER ONE" or "CHAPTER 1" etc.
    """
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    full_text = "\n".join([doc.page_content for doc in documents])
    
    # Find all chapter headings
    chapter_pattern = r'(CHAPTER\s+(?:ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN|ELEVEN|TWELVE|THIRTEEN|FOURTEEN|FIFTEEN|SIXTEEN|SEVENTEEN|EIGHTEEN|NINETEEN|TWENTY|\d+)\b)'
    chapter_matches = list(re.finditer(chapter_pattern, full_text, re.IGNORECASE))
    
    chapters = []
    for i, match in enumerate(chapter_matches):
        start_pos = match.start()
        end_pos = chapter_matches[i+1].start() if i+1 < len(chapter_matches) else len(full_text)
        
        chapter_text = full_text[start_pos:end_pos].strip()
        chapter_num = i + 1
        
        chapters.append(Document(
            page_content=chapter_text,
            metadata={"chapter": chapter_num, "source": f"Chapter {chapter_num}"}
        ))
    
    return chapters


def replace_t_with_space(documents):
    """
    Clean text by replacing tabs with spaces and normalizing whitespace.
    Handles both single Document and lists of Documents.
    """
    if isinstance(documents, list):
        for doc in documents:
            doc.page_content = doc.page_content.replace('\t', ' ')
            doc.page_content = re.sub(r'\s+', ' ', doc.page_content)
        return documents
    else:
        # Single document case
        documents.page_content = documents.page_content.replace('\t', ' ')
        documents.page_content = re.sub(r'\s+', ' ', documents.page_content)
        return documents


def replace_double_lines_with_one_line(text: str) -> str:
    """Normalize line breaks: replace multiple newlines with double newlines."""
    return re.sub(r'\n{3,}', '\n\n', text).strip()


def escape_quotes(text: str) -> str:
    """Escape quotes for safe use in prompts."""
    return text.replace('"', '\\"').replace("'", "\\'")


def extract_book_quotes_as_documents(documents) -> List[Document]:
    """
    Extract quoted text passages from documents.
    Looks for text within double quotes or dialogue patterns.
    """
    full_text = " ".join([doc.page_content for doc in documents])
    
    # Extract quoted passages
    quote_pattern = r'"([^"]{50,300})"'  # Quotes containing 50-300 chars
    matches = re.findall(quote_pattern, full_text)
    
    quotes = []
    for i, quote in enumerate(matches):
        cleaned_quote = quote.strip()
        if len(cleaned_quote) > 50:  # Only keep substantial quotes
            quotes.append(Document(
                page_content=cleaned_quote,
                metadata={"quote_id": i, "type": "quote", "source": "book_quotes"}
            ))
    
    # If no quotes found, create chunks from paragraphs
    if not quotes:
        paragraphs = [p.strip() for p in full_text.split('\n\n') if len(p.strip()) > 100]
        for i, para in enumerate(paragraphs[:20]):  # Top 20 paragraphs
            quotes.append(Document(
                page_content=para,
                metadata={"quote_id": i, "type": "paragraph", "source": "book_paragraphs"}
            ))
    
    return quotes


def extract_text_from_pdf(pdf_path: str) -> str:
    """Simple PDF text extraction without chunking."""
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    return "\n".join([doc.page_content for doc in documents])
