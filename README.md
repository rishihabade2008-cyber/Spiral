# 🧠 Jarvis - Self-Learning AI Agent (Phase 1)

A production-ready framework for building self-learning AI agents with persistent memory, loop-based task execution, and real-time visual feedback.

## 🎯 What is Jarvis?

Jarvis is a **Jarvis-style AI assistant** that:
- ✅ **Thinks before acting** - Plans multi-step tasks
- ✅ **Learns from experience** - Saves learnings to Mem0
- ✅ **Handles failures** - Reflects, retries, and diagnoses errors
- ✅ **Shows its work** - Real-time loop visualization
- ✅ **Persistent memory** - Remembers user preferences and strategies

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER REQUEST                          │
└──────────────────────┬──────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │   LangGraph Loop Engine     │
        │   (FastAPI Backend)         │
        └──────────────┬──────────────┘
                       │
    ┌──────────────────┼──────────────────┐
    │                  │                  │
    ▼                  ▼                  ▼
  Analyzer      Memory Retriever      Planner
    │                  │                  │
    └──────────────────┼──────────────────┘
                       │
    ┌──────────────────┼──────────────────┐
    │                  │                  │
    ▼                  ▼                  ▼
  Executor         Observer          Reflection
    │                  │                  │
    └──────────────────┼──────────────────┘
                       │
                       ▼
                  Learning
                       │
        ┌──────────────┴──────────────┐
        │      Save to Mem0           │
        │   (Persistent Memory)        │
        └─────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- API Keys:
  - `ANTHROPIC_API_KEY` (Claude API)
  - `MEM0_API_KEY` (Mem0 API)

### Step 1: Setup Backend

```bash
cd backend

# Create .env file
cp .env.example .env

# Edit .env and add your API keys
# MEM0_API_KEY=your_key_here
# ANTHROPIC_API_KEY=your_key_here

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r ../requirements.txt

# Run backend
python main.py
```

Backend will start on: `http://localhost:8000`

### Step 2: Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will start on: `http://localhost:3000`

## 📖 How It Works

### The Loop Engine

1. **Analyzer** - Parse user intent and extract goal
2. **Memory Retriever** - Search Mem0 for relevant past experiences
3. **Planner** - Create step-by-step task plan
4. **Executor** - Run current step using appropriate tool
5. **Observer** - Record what happened (success/failure)
6. **Reflection** - Decide if we should retry, continue, or fail
7. **Learning** - Extract useful lessons and save to Mem0

### Example Flow

**User:** "Create a Python calculator project"

```
1. [Analyzer]
   ✓ Intent: coding
   ✓ Goal: Create a Python calculator project

2. [Memory Retriever]
   ✓ Found: User prefers clean folder structure
   ✓ Found: User wants tests included

3. [Planner]
   ✓ Step 1: Create project folder
   ✓ Step 2: Generate calculator.py
   ✓ Step 3: Create tests
   ✓ Step 4: Create README.md

4. [Executor]
   ✓ Created project/
   ✓ Wrote calculator.py
   ✓ Ran tests: PASSED

5. [Observer]
   ✓ All steps completed
   ✓ Files created successfully

6. [Reflection]
   ✓ Task succeeded
   ✓ No retry needed

7. [Learning]
   ✓ Saved: User wants project structure
   ✓ Saved: Python tests work well
   ✓ Saved: README is important
```

## 🛠️ Tools Available (Phase 1)

### File Manager
- Create folders
- Write files
- Read files
- List directory contents
- Delete files

### Python Executor
- Execute Python scripts
- Run arbitrary Python code
- Execute shell commands
- Capture output and errors

### Mem0 Integration
- Save learnings
- Search relevant memories
- Format context for prompts

## 📊 Real-Time Visualization

The React frontend shows:
- **Chat Interface** - Interact with Jarvis
- **Loop Status** - Watch the loop execute in real-time
- **Execution Log** - See what each node is doing
- **Plan Viewer** - Visual task breakdown
- **Error Handling** - Clear error messages

## 🔧 Configuration

Edit `backend/.env`:

```env
# APIs
MEM0_API_KEY=your_mem0_key
ANTHROPIC_API_KEY=your_claude_key

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Loop Engine
MAX_RETRIES=3
MAX_LOOP_ITERATIONS=20

# Tools
PYTHON_TIMEOUT=30
WORK_DIR=/tmp/jarvis-workspace
```

## 📚 Project Structure

```
jarvis-agent/
├── backend/
│   ├── core/
│   │   ├── config.py          # Configuration loading
│   │   ├── state.py           # JarvisState TypedDict
│   │   └── prompts.py         # LLM prompts
│   ├── loop_engine/
│   │   └── graph.py           # LangGraph loop engine
│   ├── agents/
│   │   ├── mem0_client.py     # Mem0 API client
│   │   └── tools.py           # File & Python tools
│   ├── main.py                # FastAPI app
│   └── .env                   # Configuration
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Main app component
│   │   ├── components/        # React components
│   │   ├── App.css            # Styles
│   │   └── main.jsx           # Entry point
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
└── requirements.txt
```

## 🔄 API Endpoints

### REST
- `GET /health` - Health check
- `POST /chat` - Send message (blocking)
- `GET /config` - Get configuration

### WebSocket
- `WS /ws/chat` - Real-time streaming chat

## 📝 Example Requests

### Blocking Chat
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Create a Python calculator",
    "user_id": "user123"
  }'
```

### WebSocket Chat
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chat');
ws.onopen = () => {
  ws.send(JSON.stringify({
    message: "Create a Python calculator",
    user_id: "user123"
  }));
};
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data.type, data.content);
};
```

## 🎓 Next Steps (Phase 2-5)

- **Phase 2**: Self-correction & error retry logic
- **Phase 3**: Project memory & task history
- **Phase 4**: Voice input/output, Web search
- **Phase 5**: Multi-agent systems, GitHub integration, Browser automation

## 🐛 Troubleshooting

**"Connection error" in frontend:**
- Make sure backend is running: `python backend/main.py`
- Check that backend is on `http://localhost:8000`

**"API key not set" error:**
- Copy `.env.example` to `.env`
- Add your actual API keys
- Restart the backend

**"LangGraph not found" error:**
```bash
pip install langgraph langchain anthropic
```

**Frontend won't connect:**
- Make sure CORS is enabled in `main.py` (it is)
- Clear browser cache
- Check browser console for errors

## 📖 Documentation

- [Loop Engine Design](./docs/loop-engine.md)
- [Mem0 Integration](./docs/mem0-integration.md)
- [Tool Development](./docs/tool-development.md)

## 🤝 Contributing

This is a hackathon-ready project. Feel free to extend it:
- Add more tools (web search, API calls, GitHub)
- Enhance reflection logic
- Build advanced UIs
- Deploy to production

## 📄 License

MIT - Use freely for any purpose

## 🎯 Design Philosophy

**Fast ➜ Real-time visibility ➜ Learn from execution ➜ Improve next time**

This is not a chatbot. This is an AI that **thinks, acts, observes, reflects, and learns**.

---

Built with ❤️ using FastAPI, LangGraph, Mem0, and React.
