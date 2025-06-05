# Quick Start Guide - Local LLM Novel Summarizer

This guide will help you quickly set up and use the novel summarizer with your local LMStudio setup.

## Prerequisites ✅

You already have:
- ✅ Conda environment (base)
- ✅ Novel file: `novels/我在诡秘世界封神.txt` (1.7M characters, 706 chapters)
- ✅ Project files ready

## Step 1: Install Dependencies

In your conda base environment:

```bash
pip install -r requirements.txt
```

**New dependencies added**: `tqdm>=4.64.0` for progress display

## Step 2: Set up LMStudio

1. **Download LMStudio**: https://lmstudio.ai/
2. **Install and open LMStudio**
3. **Download Qwen3-8B model**:
   - Go to "Discover" tab
   - Search for "Qwen3" 
   - Download "Qwen3-8B" (recommended for Chinese novels)
4. **Start the server**:
   - Go to "Local Server" tab
   - Select Qwen3-8B model
   - Click "Start Server"
   - Default URL: `http://localhost:1234`

## Step 3: Configure Settings (Optional)

### Option A: Environment Variables (.env file)

Create a `.env` file with your preferred settings:

```bash
# Copy template and edit
cp env_template.txt .env
```

Edit `.env`:
```
# LMStudio Server Configuration
LMSTUDIO_BASE_URL=http://localhost
LMSTUDIO_PORT=1234

# Model Configuration
MODEL_NAME=qwen3-8b
MAX_TOKENS=32786

# Processing Configuration
CHUNK_BUFFER=500
API_TIMEOUT=60
```

### Option B: Command Line Arguments

You can specify settings directly when running:

```bash
# Basic usage
python main.py novels/我在诡秘世界封神.txt

# Custom server and model
python main.py novels/我在诡秘世界封神.txt summaries/output.md http://localhost:1234 qwen3-8b
```

## Step 4: Test the Setup

```bash
python test_summarizer.py
```

This will verify all components are working correctly and test your configuration.

## Step 5: Start Summarizing

### Basic usage:
```bash
python main.py novels/我在诡秘世界封神.txt
```

### With custom settings:
```bash
# Custom output file
python main.py novels/我在诡秘世界封神.txt summaries/诡秘世界摘要.md

# Custom server URL
python main.py novels/我在诡秘世界封神.txt summaries/output.md http://localhost:8080

# Custom server and model
python main.py novels/我在诡秘世界封神.txt summaries/output.md http://localhost:1234 Qwen3-14b
```

## 🆕 New Features: Checkpoint & Progress

### 📊 Progress Display

The tool now shows a beautiful progress bar with real-time information:

```
处理第 3 章: 60%|████████████▌        | 3/5 [00:30<00:20] 已完成: 3/5 成功率: 100.0%
```

### 💾 Automatic Checkpoint Saving

Every chapter is automatically saved as it's processed:

- **Checkpoint file**: `checkpoints/我在诡秘世界封神_checkpoint.json`
- **Progress summary**: `checkpoints/我在诡秘世界封神_progress.md`

### 🔄 Interrupt & Resume

You can safely interrupt and resume processing:

```bash
# Start processing
python main.py novels/我在诡秘世界封神.txt

# Press Ctrl+C to interrupt...
# ⚠️ 用户中断处理，已保存到第 50 章的进度

# Resume from where you left off
python main.py novels/我在诡秘世界封神.txt
# 📂 发现断点文件，从第 50 章继续处理...

# Or start fresh (ignore checkpoint)
python main.py novels/我在诡秘世界封神.txt --no-resume
```

### 📁 Checkpoint Files

After interruption, you'll find:

```
checkpoints/
├── 我在诡秘世界封神_checkpoint.json    # Checkpoint data
└── 我在诡秘世界封神_progress.md        # Intermediate results
```

The progress file contains all completed chapter summaries so far!

## Configuration Options

### Environment Variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `LMSTUDIO_BASE_URL` | `http://localhost` | Server base URL |
| `LMSTUDIO_PORT` | `1234` | Server port |
| `MODEL_NAME` | `qwen3-8b` | Model name to use |
| `MAX_TOKENS` | `32786` | Maximum context tokens |
| `CHUNK_BUFFER` | `500` | Safety buffer for chunking |
| `API_TIMEOUT` | `60` | API request timeout (seconds) |

### Command Line Usage:

```bash
python main.py <novel_path> [output_path] [server_url] [model_name] [options]
```

**Options:**
- `--no-resume`: Don't use checkpoint, start fresh

Examples:
```bash
# Default settings
python main.py novels/我在诡秘世界封神.txt

# Custom output
python main.py novels/我在诡秘世界封神.txt summaries/my_summary.md

# Custom server (different port)
python main.py novels/我在诡秘世界封神.txt summaries/output.md http://localhost:8080

# Custom server and model
python main.py novels/我在诡秘世界封神.txt summaries/output.md http://localhost:1234 Qwen3-14b

# Start fresh (ignore checkpoint)
python main.py novels/我在诡秘世界封神.txt --no-resume
```

## Expected Output

The tool will:
1. Load the novel (1.7M characters)
2. Split into 706 chapters
3. **Show progress bar** with real-time updates
4. **Save each chapter** as it's processed
5. Generate summaries using your local Qwen3-8B model
6. Save results to `summaries/我在诡秘世界封神_summary.md`

## Performance Estimates

For your novel:
- **File size**: 1.7MB (706 chapters)
- **Estimated tokens**: ~1.9M tokens  
- **Processing time**: ~60-120 minutes (depending on hardware)
- **Context size**: 32,786 tokens per chunk (increased!)
- **Recommended**: Use GPU acceleration in LMStudio

## Testing Checkpoint Features

Test the new features with a small sample:

```bash
# Create test novel and run checkpoint test
python test_checkpoint.py

# Run test (only 5 chapters)
python main.py novels/test_checkpoint.txt

# Test interruption - Press Ctrl+C after a few chapters process
# Then resume:
python main.py novels/test_checkpoint.txt
```

## Advanced Configuration

### Multiple LMStudio Instances

If you have multiple LMStudio servers:

```bash
# Server 1 (port 1234) with Qwen3-8B
LMSTUDIO_BASE_URL=http://localhost
LMSTUDIO_PORT=1234
MODEL_NAME=qwen3-8b

# Server 2 (port 8080) with Qwen3-14B  
python main.py novels/我在诡秘世界封神.txt summaries/output.md http://localhost:8080 Qwen3-14b
```

### Remote LMStudio Server

```bash
# Connect to remote server
LMSTUDIO_BASE_URL=http://192.168.1.100
LMSTUDIO_PORT=1234

# Or via command line
python main.py novels/我在诡秘世界封神.txt summaries/output.md http://192.168.1.100:1234
```

### Different Context Sizes

```bash
# For models with different context limits
MAX_TOKENS=16000  # For smaller models
MAX_TOKENS=32786  # For larger models (default)
MAX_TOKENS=8000   # For memory-constrained setups
```

## Troubleshooting

### Common Issues:

1. **LMStudio connection failed**:
   ```bash
   ❌ Failed to connect to LMStudio server
   ```
   - Check `LMSTUDIO_BASE_URL` and `LMSTUDIO_PORT`
   - Make sure LMStudio is running
   - Verify model is loaded

2. **Wrong port**:
   - Check LMStudio's "Local Server" tab for the actual port
   - Update `.env` file or use command line argument

3. **Model not found**:
   - The tool will automatically use the first available model
   - Specify exact model name in configuration

4. **Checkpoint issues**:
   - Check `checkpoints/` directory exists
   - Use `--no-resume` to ignore corrupted checkpoints
   - Delete checkpoint files manually if needed

### Debug Commands:

```bash
# Test configuration
python test_summarizer.py

# Test checkpoint features
python test_checkpoint.py

# Check help
python main.py

# Clean checkpoints
rm -rf checkpoints/
```

## File Structure After Setup

```
rolling_summerizer/
├── novels/
│   └── 我在诡秘世界封神.txt    # Your input novel
├── summaries/
│   └── 我在诡秘世界封神_summary.md  # Generated summary
├── checkpoints/                   # 🆕 Checkpoint files
│   ├── 我在诡秘世界封神_checkpoint.json
│   └── 我在诡秘世界封神_progress.md
├── .env                       # Your configuration
├── env_template.txt           # Configuration template
├── main.py                    # Main application
├── test_summarizer.py         # Test script
├── test_checkpoint.py         # 🆕 Checkpoint test
└── README.md                  # Full documentation
```

## Expected Summary Format

```markdown
# 小说章节摘要 (Generated by qwen3-8b)

**原文件**: novels/我在诡秘世界封神.txt
**使用模型**: qwen3-8b
**服务器**: http://localhost:1234
**生成时间**: 2024-01-01 12:00:00
**总章节数**: 706
**最大Token数**: 32786

---

## 第1章 01：神秘雕像

**摘要**: 白茶在宿舍时，室友于贞贞请求帮忙处理一个神秘的雕像...

## 第2章 02：归纳信息

**摘要**: 白茶开始调查雕像的来源，发现了一些不寻常的线索...
```

## Ready to Start!

Once LMStudio is running with Qwen3-8B loaded, simply run:

```bash
python main.py novels/我在诡秘世界封神.txt
```

The tool will:
- 🎯 **Automatically detect** your LMStudio server
- 📊 **Show progress** with beautiful progress bars  
- 💾 **Save each chapter** as it's processed
- 🔄 **Resume seamlessly** if interrupted
- 🚀 **Handle the rolling window** processing for your novel! 