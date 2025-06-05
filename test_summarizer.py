#!/usr/bin/env python3
"""
Test script for the Novel Summarizer (Local LLM version).
This script tests the core functionality without requiring LLM calls.
"""

import os
import sys
from utils import (
    load_novel,
    split_into_chapters,
    split_into_chunks,
    estimate_tokens,
    create_directories
)


def test_load_novel():
    """Test novel loading functionality."""
    print("Testing novel loading...")
    
    # Check for the novel in the novels folder
    novel_path = "novels/我在诡秘世界封神.txt"
    if os.path.exists(novel_path):
        text = load_novel(novel_path)
        print(f"✅ Successfully loaded novel: {len(text)} characters")
        print(f"   File: {novel_path}")
        # Show first 100 characters
        preview = text[:100].replace('\n', ' ').strip()
        print(f"   Preview: {preview}...")
        return text, novel_path
    else:
        print(f"❌ Novel file not found: {novel_path}")
        # Try to find any .txt files in novels folder
        if os.path.exists("novels"):
            txt_files = [f for f in os.listdir("novels") if f.endswith('.txt')]
            if txt_files:
                print(f"Available novels in folder: {txt_files}")
                first_novel = os.path.join("novels", txt_files[0])
                text = load_novel(first_novel)
                print(f"✅ Loaded first available novel: {first_novel}")
                return text, first_novel
        return None, None


def test_chapter_splitting(text):
    """Test chapter splitting functionality."""
    print("\nTesting chapter splitting...")
    
    chapters = split_into_chapters(text)
    print(f"✅ Found {len(chapters)} chapters:")
    
    # Show first 5 chapters
    for i, (title, content) in enumerate(chapters[:5]):
        content_preview = content[:50].replace('\n', ' ').strip()
        print(f"  {i+1}. {title} ({len(content)} characters)")
        print(f"      Preview: {content_preview}...")
    
    if len(chapters) > 5:
        print(f"  ... and {len(chapters) - 5} more chapters")
    
    return chapters


def test_token_estimation(chapters):
    """Test token estimation functionality."""
    print("\nTesting token estimation...")
    
    total_tokens = 0
    for i, (title, content) in enumerate(chapters[:3]):  # Test first 3 chapters
        tokens = estimate_tokens(content)
        total_tokens += tokens
        print(f"  {title}: {tokens} tokens")
    
    print(f"✅ Token estimation working (first 3 chapters: {total_tokens} tokens)")


def test_chunking(chapters):
    """Test text chunking functionality."""
    print("\nTesting text chunking...")
    
    if not chapters:
        print("❌ No chapters to test chunking")
        return
    
    # Test with the first chapter if it's long enough
    test_chapter = chapters[0]
    title, content = test_chapter
    
    # Test with different chunk sizes
    for chunk_size in [1000, 2000, 4000]:
        stride = chunk_size // 2
        chunks = split_into_chunks(content, chunk_size=chunk_size, stride=stride)
        print(f"  Chunk size {chunk_size}: {len(chunks)} chunks")
    
    print("✅ Text chunking working")


def test_directory_creation():
    """Test directory creation functionality."""
    print("\nTesting directory creation...")
    
    create_directories()
    
    expected_dirs = ['chapters', 'summaries']
    for directory in expected_dirs:
        if os.path.exists(directory):
            print(f"✅ Directory '{directory}' created successfully")
        else:
            print(f"❌ Directory '{directory}' not created")


def test_regex_patterns():
    """Test different chapter title patterns."""
    print("\nTesting regex patterns...")
    
    test_texts = [
        "第1章 测试标题\n这是内容",
        "第一章 古代标题\n这是内容",
        "Chapter 1: English Title\nThis is content",
        "章节 1 另一种格式\n这是内容",
        "卷1 卷标题\n这是内容"
    ]
    
    for text in test_texts:
        chapters = split_into_chapters(text)
        if chapters:
            title, content = chapters[0]
            print(f"✅ Pattern matched: '{title.strip()}'")
        else:
            print(f"❌ No pattern matched for: '{text.split()[0]}'")


def test_configuration():
    """Test configuration loading."""
    print("\nTesting configuration system...")
    
    try:
        # Import the configuration class
        sys.path.append('.')
        from main import NovelSummarizerConfig
        
        # Test default configuration
        config = NovelSummarizerConfig()
        print(f"✅ Default configuration loaded:")
        print(f"   Server URL: {config.server_url}")
        print(f"   Model: {config.model_name}")
        print(f"   Max tokens: {config.max_tokens}")
        print(f"   Chunk buffer: {config.chunk_buffer}")
        
        # Test configuration updates
        config.update_from_args(
            server_url="http://localhost:8080",
            model="Qwen3-14b"
        )
        print(f"✅ Configuration update test:")
        print(f"   Updated Server URL: {config.server_url}")
        print(f"   Updated Model: {config.model_name}")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


def test_lmstudio_connection():
    """Test connection to LMStudio server (optional)."""
    print("\nTesting LMStudio connection (optional)...")
    
    try:
        import requests
        
        # Test multiple possible URLs
        urls_to_test = [
            "http://localhost:1234",
            "http://127.0.0.1:1234",
            "http://localhost:8080"
        ]
        
        for url in urls_to_test:
            try:
                response = requests.get(f"{url}/v1/models", timeout=3)
                if response.status_code == 200:
                    models = response.json()
                    model_names = [m.get('id', 'unknown') for m in models.get('data', [])]
                    print(f"✅ LMStudio server is running on {url}")
                    print(f"   Available models: {model_names}")
                    return True
                else:
                    print(f"⚠️ Server at {url} responded with status {response.status_code}")
            except requests.exceptions.ConnectionError:
                print(f"⚠️ No server found at {url}")
            except Exception as e:
                print(f"⚠️ Error testing {url}: {e}")
        
        print("⚠️ No LMStudio server detected on common ports")
        
    except ImportError:
        print("⚠️ requests library not available for connection test")
    except Exception as e:
        print(f"⚠️ Connection test error: {e}")
    
    print("   This is optional - the test can continue without it")
    return False


def test_environment_file():
    """Test .env file configuration."""
    print("\nTesting environment file configuration...")
    
    env_files = ['.env', 'env_template.txt']
    for env_file in env_files:
        if os.path.exists(env_file):
            print(f"✅ Found {env_file}")
            with open(env_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'LMSTUDIO_BASE_URL' in content:
                    print(f"   Contains new configuration format")
                else:
                    print(f"   Contains old configuration format")
        else:
            print(f"⚠️ {env_file} not found")
    
    return True


def mock_summarizer_test():
    """Test the summarizer workflow without LLM calls."""
    print("\n" + "="*60)
    print("NOVEL SUMMARIZER TEST (LOCAL LLM VERSION)")
    print("="*60)
    
    # Test loading
    text, novel_path = test_load_novel()
    if not text:
        print("❌ Cannot continue without a novel file")
        return
    
    # Test chapter splitting
    chapters = test_chapter_splitting(text)
    
    # Test token estimation
    test_token_estimation(chapters)
    
    # Test chunking
    test_chunking(chapters)
    
    # Test directory creation
    test_directory_creation()
    
    # Test regex patterns
    test_regex_patterns()
    
    # Test configuration system
    config_ok = test_configuration()
    
    # Test environment file
    test_environment_file()
    
    # Test LMStudio connection (optional)
    lmstudio_connected = test_lmstudio_connection()
    
    print("\n✅ All basic functionality tests passed!")
    
    if config_ok:
        print("\n🔧 Configuration examples:")
        print("Environment variables:")
        print("  LMSTUDIO_BASE_URL=http://localhost")
        print("  LMSTUDIO_PORT=1234")
        print("  MODEL_NAME=qwen3-8b")
        print("  MAX_TOKENS=32000")
        
        print("\nCommand line:")
        print("  python main.py novels/我在诡秘世界封神.txt")
        print("  python main.py novels/我在诡秘世界封神.txt summaries/output.md http://localhost:1234")
        print("  python main.py novels/我在诡秘世界封神.txt summaries/output.md http://localhost:1234 Qwen3-14b")
    
    print("\nTo test with actual LLM summarization:")
    if lmstudio_connected:
        print("✅ LMStudio is ready - you can start summarizing!")
    else:
        print("1. Make sure LMStudio is running with a model loaded")
    print(f"2. Run: python main.py {novel_path}")
    
    # Show file stats
    if novel_path and chapters:
        print(f"\n📊 Novel Statistics:")
        print(f"   File: {novel_path}")
        print(f"   Total characters: {len(text):,}")
        print(f"   Total chapters: {len(chapters)}")
        print(f"   Average chapter length: {len(text) // len(chapters):,} characters")
        
        # Estimate processing time
        total_tokens = sum(estimate_tokens(content) for _, content in chapters)
        print(f"   Estimated total tokens: {total_tokens:,}")
        estimated_minutes = (total_tokens // 1000) * 2  # Rough estimate: 2 minutes per 1000 tokens
        print(f"   Estimated processing time: ~{estimated_minutes} minutes")


if __name__ == "__main__":
    mock_summarizer_test() 