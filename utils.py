import os
import regex as re
import tiktoken
from typing import List, Tuple


def load_novel(path: str) -> str:
    """
    Load novel text from file and return as string.
    
    Args:
        path: Path to the novel text file
        
    Returns:
        The complete text content of the novel
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        return text
    except UnicodeDecodeError:
        # Try different encodings if UTF-8 fails
        for encoding in ['gbk', 'gb2312', 'big5']:
            try:
                with open(path, 'r', encoding=encoding) as f:
                    text = f.read()
                print(f"Successfully loaded file with {encoding} encoding")
                return text
            except UnicodeDecodeError:
                continue
        raise ValueError(f"Unable to decode file {path} with any common encoding")


def split_into_chapters(text: str) -> List[Tuple[str, str]]:
    """
    Split novel text into chapters using regex patterns.
    
    Args:
        text: The complete novel text
        
    Returns:
        List of tuples (chapter_title, chapter_content)
    """
    # Support multiple chapter title patterns
    patterns = [
        r'第\d+章[^\n]*',           # 第1章 标题
        r'Chapter\s+\d+[:\s][^\n]*', # Chapter 1: Title
        r'第[一二三四五六七八九十百千万]+章[^\n]*',  # 第一章 标题
        r'章节\s*\d+[^\n]*',        # 章节 1
        r'卷\d+[^\n]*',             # 卷1
    ]
    
    # Try each pattern and use the one that finds the most matches
    best_pattern = None
    best_matches = []
    
    for pattern in patterns:
        matches = [(m.group(), m.start()) for m in re.finditer(pattern, text)]
        if len(matches) > len(best_matches):
            best_pattern = pattern
            best_matches = matches
    
    if not best_matches:
        # If no pattern matches, treat the entire text as one chapter
        return [("全文", text)]
    
    chapters = []
    for idx, (title, start_pos) in enumerate(best_matches):
        end_pos = best_matches[idx + 1][1] if idx + 1 < len(best_matches) else len(text)
        content = text[start_pos:end_pos]
        
        # Extract title and body
        lines = content.split('\n', 1)
        chap_title = lines[0].strip()
        chap_body = lines[1] if len(lines) > 1 else ''
        
        # Remove extra whitespace and empty lines
        chap_body = '\n'.join(line.strip() for line in chap_body.split('\n') if line.strip())
        
        if chap_body:  # Only add chapters with content
            chapters.append((chap_title, chap_body))
    
    return chapters


def estimate_tokens(text: str, model_name: str = 'gpt-3.5-turbo') -> int:
    """
    Estimate the number of tokens in text using tiktoken.
    
    Args:
        text: Text to estimate tokens for
        model_name: Model name for token encoding
        
    Returns:
        Estimated number of tokens
    """
    try:
        encoding = tiktoken.encoding_for_model(model_name)
        tokens = encoding.encode(text)
        return len(tokens)
    except Exception:
        # Fallback estimation: roughly 4 characters per token for Chinese text
        return len(text) // 4


def split_into_chunks(text: str, chunk_size: int = 3800, stride: int = 1900, 
                     model_name: str = 'gpt-3.5-turbo') -> List[str]:
    """
    Split text into overlapping chunks based on token limits.
    
    Args:
        text: Text to split
        chunk_size: Maximum tokens per chunk
        stride: Step size for sliding window
        model_name: Model name for token encoding
        
    Returns:
        List of text chunks
    """
    try:
        encoding = tiktoken.encoding_for_model(model_name)
        token_ids = encoding.encode(text)
        
        chunks = []
        start = 0
        n = len(token_ids)
        
        while start < n:
            end = min(start + chunk_size, n)
            chunk_ids = token_ids[start:end]
            chunk_text = encoding.decode(chunk_ids)
            chunks.append(chunk_text)
            
            # If we've reached the end, break
            if end == n:
                break
                
            # Move to next starting position
            start += stride
            
        return chunks
    
    except Exception:
        # Fallback: split by characters (approximation)
        char_chunk_size = chunk_size * 4  # 4 chars per token approximation
        char_stride = stride * 4
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = min(start + char_chunk_size, len(text))
            chunk = text[start:end]
            chunks.append(chunk)
            
            if end == len(text):
                break
                
            start += char_stride
            
        return chunks


def create_directories():
    """Create necessary directories for the project."""
    directories = ['chapters', 'summaries']
    for directory in directories:
        os.makedirs(directory, exist_ok=True) 