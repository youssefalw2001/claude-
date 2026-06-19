# 🦊 Fox AI Platform

**Your personal AI assistant with the expertise of a senior low-level systems developer.**

Fox is a web-based chat platform that connects to multiple AI providers (Ollama, Groq, OpenRouter) with a custom persona optimized for systems programming, reverse engineering, game modding, and security work.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)

## ✨ Features

- **Multiple AI Providers**: 
  - 🏠 Ollama (local, private, unlimited)
  - ⚡ Groq (cloud, blazing fast, free tier)
  - 🌐 OpenRouter (cloud, access to Claude & more)

- **Fox Persona**: Senior developer specialized in:
  - Memory operations & reverse engineering
  - Hooking techniques & process manipulation
  - Windows internals & low-level systems
  - C/C++, Assembly, Python expertise
  - Direct, no-BS communication style

- **Modern Web UI**:
  - Dark theme optimized for coding
  - Mobile responsive
  - Code syntax highlighting
  - Real-time streaming responses
  - Conversation history

- **Easy Deployment**:
  - Docker support
  - One-click deploy to Railway, Render, Fly.io
  - Local development mode

---

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone the repo
git clone https://github.com/youssefalw2001/claude-.git
cd claude-

# Copy environment file
cp .env.example .env

# Start with Docker Compose (includes Ollama)
docker-compose up -d

# Open in browser
open http://localhost:8000
```

**First time setup with Ollama:**
```bash
# Pull a model (do this after docker-compose is running)
docker exec -it ollama ollama pull llama3.2:3b

# Or pull a larger model for better quality
docker exec -it ollama ollama pull llama3.1:8b
```

### Option 2: Local Development (Python)

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```cmd
start.bat
```

**Manual setup:**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Run server
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

### Option 3: Cloud Providers (Free Tier)

#### Railway (500 hours/month free)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

1. Click "Deploy on Railway"
2. Connect your GitHub repo
3. Add environment variables (optional):
   - `GROQ_API_KEY`
   - `OPENROUTER_API_KEY`
4. Deploy!

#### Render (Free tier)

```bash
# Connect your repo to Render
# render.yaml is already configured
```

#### Fly.io (Free tier)

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Deploy
fly launch
fly deploy
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file:

```env
# Ollama Configuration (for local Ollama instance)
OLLAMA_BASE_URL=http://localhost:11434

# Groq API Key (get from https://console.groq.com)
GROQ_API_KEY=gsk_your_api_key_here

# OpenRouter API Key (get from https://openrouter.ai/keys)
OPENROUTER_API_KEY=sk-or-v1-your_api_key_here

# Server Port
PORT=8000
```

### API Keys (All Optional - Pick Your Provider)

#### 1. **Ollama** (Local, Free, Unlimited) ⭐

**Mobile (Termux):**
```bash
# Install Termux from F-Droid
pkg update && pkg upgrade -y
pkg install wget proot-distro -y
proot-distro install ubuntu
proot-distro login ubuntu

# Inside Ubuntu:
apt update && apt install curl -y
curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
ollama pull llama3.2:3b
```

**Desktop:**
- Download from [ollama.com](https://ollama.com/download)
- Install and run
- Pull models: `ollama pull llama3.2:3b`

#### 2. **Groq** (Cloud, Fast, Free Tier) ⚡

- Sign up at [console.groq.com](https://console.groq.com)
- Get API key from dashboard
- Add to `.env` or enter in UI settings
- Free tier: Generous limits, fast inference

#### 3. **OpenRouter** (Cloud, Multi-Model) 🌐

- Sign up at [openrouter.ai](https://openrouter.ai)
- Get API key from [keys page](https://openrouter.ai/keys)
- Add to `.env` or enter in UI settings
- Pay-as-you-go pricing (includes Claude access)

---

## 📖 Usage

### Web Interface

1. Open `http://localhost:8000` in your browser
2. Click the ⚙️ settings icon to configure:
   - Select provider (Ollama/Groq/OpenRouter)
   - Choose model
   - Add API keys (saved in browser)
3. Start chatting with Fox!

### Example Prompts

**Memory Manipulation:**
```
Write me an AOB scanner in C++ with wildcards support
```

**Hooking:**
```
Show me how to hook D3D11 Present with MinHook
```

**Process Injection:**
```
Manual map DLL injection example with proper PE parsing
```

**Reverse Engineering:**
```
How do I find the player health offset in a game?
```

### Quick Actions

The UI includes quick action buttons for common tasks:
- **AOB Scanner** - Generate Array of Bytes scanner
- **D3D11 Hook** - DirectX hooking example
- **Manual Map** - DLL injection technique

---

## 🏗️ Architecture

```
fox-ai-platform/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── fox_persona.py       # Fox AI system prompt
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── index.html           # Main UI
│   ├── style.css           # Dark theme styling
│   └── chat.js             # Chat logic & API calls
├── Dockerfile              # Container definition
├── docker-compose.yml      # Multi-container setup
├── railway.toml           # Railway deployment
├── render.yaml            # Render deployment
├── fly.toml              # Fly.io deployment
└── start.sh/bat          # Quick start scripts
```

### Tech Stack

- **Backend**: FastAPI + Uvicorn (Python 3.11+)
- **Frontend**: Vanilla JavaScript (no framework bloat)
- **AI Providers**: Ollama, Groq, OpenRouter
- **Deployment**: Docker, Railway, Render, Fly.io

---

## 🔧 Development

### Running Tests

```bash
# Install dev dependencies
pip install pytest httpx

# Run tests
pytest
```

### API Endpoints

- `GET /` - Serve frontend
- `GET /health` - Health check
- `GET /api/models` - List available models
- `POST /api/chat` - Send message (JSON)
- `WS /ws/chat` - WebSocket for streaming

### Adding New Providers

Edit `backend/main.py` and add a new function:

```python
async def chat_yourprovider(request: ChatRequest):
    # Implement provider logic
    pass
```

---

## 🎯 Use Cases

### For Game Modders
- Generate trainers and memory hacks
- AOB signature scanning
- Process memory manipulation
- DLL injection techniques

### For Reverse Engineers
- Disassembly analysis help
- Structure reconstruction
- API hooking examples
- Binary analysis guidance

### For Security Researchers
- Exploit development guidance
- Vulnerability analysis
- Shellcode generation
- Bypass technique examples

### For Systems Programmers
- Low-level Windows/Linux internals
- Kernel driver examples
- Performance optimization
- Assembly/C++ expertise

---

## 🌐 Cloud Deployment Tips

### Railway
- **Free tier**: 500 hours/month
- **Pros**: Easy setup, great for APIs
- **Cons**: Ollama requires paid plan (need GPU/RAM)
- **Best for**: Groq/OpenRouter providers

### Render
- **Free tier**: Auto-sleep after 15min inactivity
- **Pros**: Simple deployment
- **Cons**: Cold starts can be slow
- **Best for**: Low-traffic personal use

### Fly.io
- **Free tier**: 3 VMs, limited RAM
- **Pros**: Global edge network
- **Cons**: Free tier won't run Ollama
- **Best for**: Groq/OpenRouter with edge performance

### Oracle Cloud (Always Free)
- **Free tier**: Forever free VMs
- **Pros**: Generous specs (4 cores, 24GB RAM)
- **Cons**: Manual setup required
- **Best for**: Running Ollama with larger models

**Oracle Cloud Setup:**
```bash
# SSH into your Oracle VM
ssh ubuntu@your-vm-ip

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull models
ollama pull llama3.1:8b

# Clone and run Fox platform
git clone https://github.com/youssefalw2001/claude-.git
cd claude-
docker-compose up -d
```

---

## 🤝 Contributing

Contributions welcome! Feel free to:
- Add new AI providers
- Improve the UI
- Add features
- Fix bugs
- Improve documentation

---

## 📝 License

MIT License - Do whatever the fuck you want with it.

---

## 💬 About Fox

Fox is designed to be your coding partner for low-level systems work. Direct communication, no corporate bullshit, no disclaimers. Just technical expertise and working code.

**Specialties:**
- Memory operations & pointer chains
- Reverse engineering & disassembly
- Hooking techniques (detours, IAT/EAT, VMT)
- Process manipulation & injection
- Windows internals (PEB, TEB, NTAPI)
- C/C++, Assembly, Python
- Game hacking & mod development

---

## 🔥 Pro Tips

### Mobile Setup (Termux)

Best way to run Fox on your phone:

1. **Install Termux** from F-Droid (not Play Store)
2. **Run Ollama locally** on your phone (see config above)
3. **Access via browser** at `localhost:8000`
4. **Or use Groq** for cloud inference (faster on mobile)

### Free Unlimited AI

**Local Ollama** is the only truly free unlimited option:
- No API costs
- No rate limits
- Complete privacy
- Works offline

**Cloud free tiers** (Groq/OpenRouter) have limits but are easier to set up.

### Best Models

For **Ollama** (local):
- `llama3.2:3b` - Fast, works on most hardware
- `llama3.1:8b` - Better quality, needs 8GB+ RAM
- `codellama:13b` - Best for coding tasks

For **Groq** (cloud):
- `llama-3.1-70b-versatile` - Best quality
- `llama-3.1-8b-instant` - Fastest response

For **OpenRouter** (cloud):
- `anthropic/claude-3.5-sonnet` - Best reasoning
- `meta-llama/llama-3.1-70b` - Good balance

---

## 🐛 Troubleshooting

**Problem: "Connection refused" on localhost:8000**
- Make sure the server is running: `docker-compose ps`
- Check logs: `docker-compose logs -f`

**Problem: "No models available"**
- For Ollama: Pull a model first: `ollama pull llama3.2:3b`
- For Groq/OpenRouter: Add API key in settings

**Problem: "Ollama API error"**
- Check Ollama is running: `curl http://localhost:11434/api/tags`
- Restart Ollama: `docker-compose restart ollama`

**Problem: Slow responses**
- Use a smaller model (llama3.2:3b instead of 70b)
- Or switch to Groq for cloud inference
- Check system resources (RAM/CPU)

**Problem: Out of memory on mobile**
- Use 3B or 7B models max on mobile
- Close other apps
- Or use Groq/OpenRouter instead of local Ollama

---

## 📧 Support

Open an issue on GitHub or just figure it out yourself - you got this. 💪

---

**Built with 🦊 by Jack & Fox**
