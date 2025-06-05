#!/usr/bin/env python3
"""
Setup script for the Novel Summarizer project.
This script helps users quickly set up the environment and dependencies.
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


def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is too old. Requires Python 3.9+")
        return False


def install_dependencies():
    """Install required Python packages."""
    packages = ["openai>=1.3.0", "python-dotenv>=1.0.0", "tiktoken>=0.5.1", "regex>=2023.10.3"]
    
    for package in packages:
        if not run_command(f"pip install {package}", f"Installing {package}"):
            return False
    return True


def create_env_file():
    """Create .env file from template if it doesn't exist."""
    if not os.path.exists(".env"):
        if os.path.exists("env_template.txt"):
            print("📄 Creating .env file from template...")
            shutil.copy("env_template.txt", ".env")
            print("✅ .env file created. Please edit it and add your OPENAI_API_KEY")
        else:
            print("📄 Creating basic .env file...")
            with open(".env", "w") as f:
                f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
            print("✅ .env file created. Please edit it and add your OPENAI_API_KEY")
    else:
        print("📄 .env file already exists")


def run_tests():
    """Run the test script to verify installation."""
    print("🧪 Running tests to verify installation...")
    return run_command("python test_summarizer.py", "Running functionality tests")


def main():
    """Main setup function."""
    print("=" * 60)
    print("🚀 NOVEL SUMMARIZER SETUP")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
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
    
    # Create .env file
    create_env_file()
    
    # Run tests
    if not run_tests():
        print("❌ Tests failed")
        return 1
    
    # Final instructions
    print("\n" + "=" * 60)
    print("🎉 SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\n📋 Next steps:")
    print("1. Edit the .env file and add your OpenAI API key")
    print("2. Test with the example novel: python main.py example_novel.txt")
    print("3. Check the generated summary in the summaries/ folder")
    print("\n📚 Usage examples:")
    print("  python main.py your_novel.txt")
    print("  python main.py your_novel.txt output_summary.md")
    print("  python main.py your_novel.txt output_summary.md gpt-4")
    print("\n📖 Read README.md for more detailed instructions")
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 