# 🚀 Jarvis Phase 1 - Quick Start Guide

You now have a complete, production-ready self-learning AI agent. Here's how to run it in 5 minutes.

## ⚡ TL;DR - Get Running Now

```bash
# Terminal 1: Backend
cd jarvis-agent/backend
python -m venv venv
source venv/bin/activate
pip install -r ../requirements.txt
# Edit .env with your API keys
python main.py

# Terminal 2: Frontend (while backend is running)
cd jarvis-agent/frontend
npm install
npm run dev
```

Then open `http://localhost:3000` in your browser.

---

## 📋 Prerequisites

Before you start, you need:

1. **Python 3.10+**
   ```bash
   python --version
   ```

2. **Node.js 18+**
   ```bash
   node --version
   npm --version
   ```

3. **API Keys** (Get them free):
   - Claude API: https://console.anthropic.com
   - Mem0 API: https://mem0.ai (sign up for free tier)

---

## Step-by-Step Setup

### Step 1: Get Your API Keys

1. Go to https://console.anthropic.com and get your Claude API key
2. Go to https://mem0.ai and get your Mem0 API key
3. Copy them somewhere safe

### Step 2: Setup Backend

```bash
cd jarvis-agent/backend

# Create environment file
cp .env.example .env

# Edit .env and add your keys
nano .env  # or use your editor
# Add:
# MEM0_API_KEY=your_key_here
# ANTHROPIC_API_KEY=your_key_here
```

```bash
# Create Python environment
python -m venv venv

# Activate it
# On Mac/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r ../requirements.txt

# Start backend
python main.py
```

✅ You should see: `Uvicorn running on http://0.0.0.0:8000`

### Step 3: Setup Frontend

**In a new terminal** (keep backend running):

```bash
cd jarvis-agent/frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

✅ You should see: `VITE v5.0.0 ready in ... ms`

### Step 4: Open in Browser

Go to: `http://localhost:3000`

You'll see:
- **Left side**: Chat interface with Jarvis
- **Right side**: Real-time loop visualization

---

## 🧪 Test It Out

Try these prompts to test the agent:

```
"Create a Python hello world script"
"Build a simple calculator in Python"
"Create a project folder structure"
```

Watch the loop execute in real-time on the right panel:
1. 🔍 Analyzer - Understands your request
2. 💾 Memory - Retrieves past learnings
3. 📋 Planner - Creates a task plan
4. ⚙️ Execute - Runs the steps
5. 👁️ Observe - Records what happened
6. 🧠 Reflect - Decides what's next
7. 📚 Learn - Saves learnings to memory

---

## 🎯 What You Can Do Right Now

### In Phase 1:
- ✅ Chat with Jarvis
- ✅ Watch real-time loop execution
- ✅ See memory retrieval
- ✅ File creation and Python execution
- ✅ Error handling and retry logic
- ✅ Learning extraction

### To Add (Phase 2-5):
- Web search integration
- GitHub integration
- Voice input/output
- Multi-agent coordination
- Browser automation
- Dashboard with metrics

---

## 🐛 Troubleshooting

### Backend won't start
```
Error: MEM0_API_KEY not set

→ Solution: Edit backend/.env and add your actual API key
```

### Frontend won't connect
```
Connection error. Make sure backend is running

→ Solution: Make sure backend is running on port 8000
→ Check: http://localhost:8000/health
```

### "Module not found" error
```
ModuleNotFoundError: No module named 'langgraph'

→ Solution: Reinstall dependencies
→ pip install -r requirements.txt
```

### Port already in use
```
Address already in use (:8000 or :3000)

→ Solution: Kill existing process or use different port
→ Change PORT in backend/.env
```

---

## 📁 Project Structure

What you got:

```
jarvis-agent/
├── backend/              ← Python FastAPI server
│   ├── core/
│   │   ├── config.py     ← Settings & env vars
│   │   ├── state.py      ← State object definition
│   │   └── prompts.py    ← LLM prompts
│   ├── loop_engine/
│   │   └── graph.py      ← LangGraph loop (the magic)
│   ├── agents/
│   │   ├── mem0_client.py ← Memory integration
│   │   └── tools.py      ← File & Python tools
│   ├── main.py           ← FastAPI app
│   └── .env              ← Your API keys (create this)
│
├── frontend/             ← React UI
│   ├── src/
│   │   ├── App.jsx       ← Main app
│   │   ├── components/   ← Chat, Loop, Plan components
│   │   └── index.css     ← Styles
│   ├── package.json
│   └── vite.config.js
│
└── README.md            ← Full documentation
```

---

## 🔧 Configuration Tips

### Make it faster
```env
# In backend/.env
MAX_RETRIES=2        # Fewer retries
MAX_LOOP_ITERATIONS=10  # Shorter loops
PYTHON_TIMEOUT=15    # Quicker timeout
```

### Make it smarter
Edit `backend/core/prompts.py` - each prompt controls behavior:
- `ANALYZER_PROMPT` - How it understands requests
- `PLANNER_PROMPT` - How it plans tasks
- `REFLECTION_PROMPT` - How it decides next steps
- `LEARNING_PROMPT` - What it learns

### Save to different directory
```env
# In backend/.env
WORK_DIR=/path/to/workspace
```

---

## 📊 Real Features

This isn't a demo. You have:

✅ **Real LangGraph loop engine** - Not a simple chatbot
✅ **Real Mem0 integration** - Actual persistent memory
✅ **Real error handling** - Retries, diagnosis, fallbacks
✅ **Real tool execution** - File ops + Python code
✅ **Real streaming UI** - Real-time loop visualization
✅ **Production-ready code** - Error handling, logging, validation

---

## 🚀 Next Steps After Setup

1. **Try different prompts** - See how it plans and executes
2. **Watch the loop** - Learn how self-learning works
3. **Check Mem0** - See what it's remembering
4. **Extend the tools** - Add web search, GitHub, etc.
5. **Deploy it** - Docker compose is ready (phase later)

---

## 💡 Pro Tips

1. **Look at the logs** - Terminal shows detailed execution
2. **Check browser console** - Debug frontend issues
3. **Test endpoints** - `http://localhost:8000/health` 
4. **Save good prompts** - They train the agent
5. **Clear old workspace** - `/tmp/jarvis-workspace` can grow

---

## 📞 Need Help?

1. Check `README.md` - Full docs
2. Check backend logs - `python main.py` shows errors
3. Check browser console - F12 in browser
4. Check `.env.example` - Reference for config

---

## 🎓 Learning Path

1. **Start**: Run it, play with prompts
2. **Understand**: Read loop_engine/graph.py (the 7 nodes)
3. **Extend**: Add new tools to agents/tools.py
4. **Deploy**: Use docker-compose.yml
5. **Scale**: Phase 2-5 features

---

## 🎉 You're Ready!

You now have a real self-learning AI agent that:
- Plans multi-step tasks
- Executes them
- Learns from results
- Remembers for next time

The loop engine is the core. Each time the agent runs, it gets smarter.

**Go build something cool.** 🚀

---

Questions? Check:
- Backend logs: `python backend/main.py`
- Frontend console: F12
- Full README: `README.md`
- Code comments: Well-documented Python/React
