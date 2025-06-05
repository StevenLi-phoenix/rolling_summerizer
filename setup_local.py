#!/usr/bin/env python3
"""
Setup script for the Novel Summarizer (Local LLM version).
This script helps users quickly set up the environment for local LLM usage.
"""

import os
import sys
import subprocess
import shutil


def run_command(command, description):
    """Run a command and display the result."""
    print(f"📋 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False


def check_conda_environment():
    """Check if conda is available and we're in the right environment."""
    print("🐍 Checking conda environment...")
    try:
        # Check if conda is available
        result = subprocess.run("conda info --envs", shell=True, check=True, capture_output=True, text=True)
        print("✅ Conda is available")
        
        # Check if we're in base environment
        result = subprocess.run("conda info", shell=True, check=True, capture_output=True, text=True)
        if "active environment : base" in result.stdout:
            print("✅ Currently in conda base environment")
            return True
        else:
            print("⚠️ Not in conda base environment. Activating base...")
            return True
    except subprocess.CalledProcessError:
        print("❌ Conda not found. Please install Anaconda or Miniconda first.")
        return False


def install_dependencies():
    """Install required Python packages."""
    packages = ["openai>=1.3.0", "requests>=2.28.0", "python-dotenv>=1.0.0", "tiktoken>=0.5.1", "regex>=2023.10.3"]
    
    for package in packages:
        if not run_command(f"pip install {package}", f"Installing {package}"):
            return False
    return True


def check_lmstudio():
    """Check if LMStudio is available and provide guidance."""
    print("🤖 Checking LMStudio setup...")
    
    # Check if LMStudio server is running
    try:
        import requests
        response = requests.get("http://localhost:1234/v1/models", timeout=3)
        if response.status_code == 200:
            models = response.json()
            model_names = [m.get('id', 'unknown') for m in models.get('data', [])]
            print(f"✅ LMStudio server is running")
            print(f"Available models: {model_names}")
            return True
        else:
            print(f"⚠️ LMStudio server responded with status {response.status_code}")
    except Exception:
        pass
    
    print("⚠️ LMStudio server not detected")
    print("📖 Please follow these steps:")
    print("   1. Download LMStudio from https://lmstudio.ai/")
    print("   2. Install and open LMStudio")
    print("   3. Go to 'Discover' tab and download a model (recommended: Qwen3-8B)")
    print("   4. Go to 'Local Server' tab, select your model, and click 'Start Server'")
    print("   5. Server should start on http://localhost:1234")
    return False


def check_novel_files():
    """Check for novel files and provide guidance."""
    print("📚 Checking for novel files...")
    
    if not os.path.exists("novels"):
        print("📁 Creating novels directory...")
        os.makedirs("novels", exist_ok=True)
    
    txt_files = []
    if os.path.exists("novels"):
        txt_files = [f for f in os.listdir("novels") if f.endswith('.txt')]
    
    if txt_files:
        print(f"✅ Found {len(txt_files)} novel file(s):")
        for file in txt_files[:3]:  # Show first 3 files
            file_path = os.path.join("novels", file)
            size = os.path.getsize(file_path) / 1024 / 1024  # Size in MB
            print(f"   - {file} ({size:.1f} MB)")
        if len(txt_files) > 3:
            print(f"   ... and {len(txt_files) - 3} more")
        return True
    else:
        print("⚠️ No novel files found in 'novels' folder")
        print("📖 Please add your novel .txt files to the 'novels' folder")
        print("   Supported formats: UTF-8, GBK, GB2312, Big5")
        return False


def run_tests():
    """Run the test script to verify installation."""
    print("🧪 Running tests to verify installation...")
    return run_command("python test_summarizer.py", "Running functionality tests")


def main():
    """Main setup function."""
    print("=" * 60)
    print("🚀 NOVEL SUMMARIZER SETUP (LOCAL LLM)")
    print("=" * 60)
    
    # Check conda environment
    if not check_conda_environment():
        return 1
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        return 1
    
    # Create directories
    print("📁 Creating project directories...")
    os.makedirs("chapters", exist_ok=True)
    os.makedirs("summaries", exist_ok=True)
    print("✅ Project directories created")
    
    # Check LMStudio
    lmstudio_ready = check_lmstudio()
    
    # Check novel files
    novels_ready = check_novel_files()
    
    # Run tests
    if not run_tests():
        print("❌ Tests failed")
        return 1
    
    # Final instructions
    print("\n" + "=" * 60)
    print("🎉 SETUP COMPLETED!")
    print("=" * 60)
    
    if lmstudio_ready and novels_ready:
        print("\n✅ Everything is ready! You can start summarizing:")
        print("📚 Example usage:")
        print("  python main.py novels/我在诡秘世界封神.txt")
    else:
        print("\n📋 Next steps:")
        if not lmstudio_ready:
            print("🤖 1. Set up LMStudio (see instructions above)")
        if not novels_ready:
            print("📚 2. Add novel .txt files to the 'novels' folder")
        print("📝 3. Then run: python main.py novels/your_novel.txt")
    
    print("\n🔧 Additional commands:")
    print("  python test_summarizer.py  # Test functionality")
    print("  python main.py --help      # See usage instructions")
    
    print("\n📊 Performance tips:")
    print("  - Use GPU acceleration in LMStudio for faster processing")
    print("  - Start with smaller novels to test the setup")
    print("  - Monitor memory usage - large novels may require chunking")
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 