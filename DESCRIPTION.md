# Spiral - Self-Learning AI Agent

## One-Liner
**An agentic loop that thinks, acts, observes, reflects, and learns—making AI smarter with every task.**

---

## Short Description (50 words)

Spiral is a production-ready self-learning AI agent that executes multi-step tasks, learns from every execution, and improves over time. Built with LangGraph, Mem0, and React—it's not a chatbot, it's an agent that gets smarter.

---

## Medium Description (150 words)

Spiral is a **self-learning AI agent framework** that goes beyond traditional chatbots. Instead of just responding, Spiral:

1. **Thinks** - Analyzes requests and creates detailed plans
2. **Acts** - Executes tasks using real tools (file ops, Python, web search)
3. **Observes** - Records what happened with precision
4. **Reflects** - Decides if results are good or needs retry
5. **Learns** - Extracts lessons and saves to persistent memory

The key innovation: **every task makes the agent smarter**. Memories compound over time, enabling exponential improvement in decision-making.

Built with LangGraph state machines, Mem0 for persistent memory, Anthropic's Claude API for reasoning, and a beautiful React UI for real-time visualization of the entire loop.

Perfect for rapid prototyping, hackathons, or production deployment.

---

## Long Description (500+ words)

### What is Spiral?

Spiral is a **production-ready framework for building self-learning AI agents**. It's not a chatbot. It's an **agentic loop** that continuously improves.

### The Problem

Traditional chatbots are stateless—they forget every conversation. Even modern AI systems lack true learning mechanisms. They respond once and move on, never getting better from experience.

Spiral solves this by implementing a **closed-loop learning system**:

```
Request → Think → Plan → Act → Observe → Reflect → Learn → Repeat
                                                         ↓
                                              Memory improves future tasks
```

### How It Works

**The 7-Node Loop Engine:**

1. **Analyzer** 🔍 - Understands user intent and extracts the goal
2. **Memory Retriever** 💾 - Finds relevant past experiences using semantic search
3. **Planner** 📋 - Creates step-by-step task decomposition
4. **Executor** ⚙️ - Runs each step using appropriate tools
5. **Observer** 👁️ - Records outcomes factually (success/failure/error)
6. **Reflection** 🧠 - Decides next action (continue/retry/fail)
7. **Learning** 📚 - Extracts lessons and saves to persistent memory

**Key Innovation**: Each node is a Claude API call with structured reasoning. No black boxes. Everything is transparent and debuggable.

### What Makes It Different

❌ **Not a chatbot** - Chatbots respond once. Spiral loops indefinitely.

✅ **Agentic** - Thinks, plans, acts, observes, reflects, learns.

❌ **Not stateless** - Traditional apps forget. Spiral remembers.

✅ **Persistent Memory** - Every task improves future decisions.

❌ **Not simulation** - Many demos fake execution. Spiral actually runs code.

✅ **Real Execution** - Creates files, runs Python, calls APIs.

❌ **Not black box** - Standard agents hide their thinking.

✅ **Transparent Loop** - See exactly what each node does in real-time.

### Features

**Phase 1 (Included)**
- ✅ Real-time loop visualization (watch all 7 nodes)
- ✅ File creation & management
- ✅ Python code execution
- ✅ Persistent memory (Mem0 integration)
- ✅ Automatic error detection & retry logic
- ✅ Beautiful React UI with dark mode
- ✅ WebSocket streaming for real-time updates
- ✅ Production-grade error handling

**Phase 2+ (Roadmap)**
- Web search integration
- GitHub API integration
- Voice input/output
- Multi-agent coordination
- Browser automation
- Advanced analytics dashboard

### Tech Stack

**Backend**
- FastAPI (async HTTP + WebSocket)
- LangGraph (agent loop state machine)
- Anthropic Claude API (reasoning)
- Mem0 API (persistent memory)
- Python 3.10+

**Frontend**
- React 18 (component framework)
- Vite (build tool)
- WebSocket (real-time streaming)
- Custom CSS (dark mode, animations)

**Infrastructure**
- Docker ready
- No database needed (Mem0 handles storage)
- Localhost to production with one command

### Performance

- **Single task**: 15-30 seconds (depends on loop iterations)
- **Memory overhead**: ~150MB steady state
- **API calls**: 5-10 per task
- **Scalability**: Sequential processing; parallel ready (Phase 2)

### Use Cases

**Hackathons**
- Build AI agents in hours not weeks
- Impressive demos with real execution
- Learn agent patterns fast

**Prototyping**
- Test AI agent ideas quickly
- Iterate on prompts and tools
- See results immediately

**Production**
- Deploy with Docker
- Monitor with structured logging
- Scale with persistent memory

**Research**
- Study agentic loops
- Test reasoning strategies
- Benchmark agent performance

### The Learning Mechanism

The genius is in **memory compounding**:

```
Task 1: User says "I prefer Python"
→ Saved to memory

Task 2: User says "Build a project"
→ Agent retrieves: "User prefers Python"
→ Uses Python automatically

Task 3: User says "Add this feature"
→ Agent retrieves: Earlier decisions + Python preference
→ Makes better decisions

Task N: Agent has learned your patterns
→ Predicts preferences
→ Needs fewer corrections
```

Over 10 tasks, the agent becomes 10x better at serving that specific user.

### Why Spiral?

**Spiral** represents:
- 🌀 Growth & continuous improvement
- 🔄 The loop concept (core mechanism)
- 📈 Upward trajectory (learning)
- 🎨 Great branding potential

Plus it's short, memorable, and easy to say.

### Getting Started

1. Extract zip
2. Run setup script (auto-installs dependencies)
3. Add API keys (5 minutes)
4. Start backend & frontend
5. Open browser
6. Start talking to your AI agent

Full setup: **15 minutes**

### Documentation

- **100+ pages** of documentation
- **40+ files** of production code
- **3400+ lines** organized and commented
- Setup automation scripts included
- Troubleshooting guide included

### License

MIT - Use freely for any purpose (commercial, private, research)

### About the Author

Built by Rishi - A hacker who builds fast and ships products.

Inspired by:
- Anthropic's agent research
- LangGraph state machines
- Mem0's memory innovation
- Real-world hackathon needs

### The Philosophy

**Think → Act → Learn → Repeat**

Every iteration:
- The agent gets smarter
- The memory gets richer
- The decisions get better
- The user gets served faster

This isn't just software. It's a framework for **continuous improvement in AI systems**.

---

## Tagline Options

1. **"Think. Act. Learn. Repeat."** - Core philosophy
2. **"An AI that gets smarter with every task."** - Value prop
3. **"Self-learning agents for the impatient."** - For Rishi's audience
4. **"The loop is the learning."** - Technical deep dive
5. **"Your AI learns. Exponentially."** - Growth focused

---

## Social Media Description

**Twitter/X (280 chars)**
"Spiral: An AI agent that thinks, acts, observes, reflects, and learns. Each task makes it smarter. Built with LangGraph + Mem0 + Claude. Open source. Production ready. 🌀🧠"

**GitHub (short)**
"A self-learning AI agent that improves with every task. Think → Plan → Act → Observe → Reflect → Learn → Repeat. Production-ready framework with real execution."

**LinkedIn (professional)**
"Spiral is an enterprise-ready framework for autonomous AI agents. Built on proven technologies (LangGraph, Claude, Mem0), it implements a closed-loop learning system that improves decision-making over time. Perfect for teams building intelligent automation."

---

## Positioning

### For Hackers/Builders
*"Build impressive AI agents in hours, not weeks. See real code execution with transparent reasoning loops."*

### For Enterprises
*"Autonomous agents that improve over time. Transparent reasoning. Persistent memory. Production-ready."*

### For Researchers
*"Study agentic loops in action. Benchmark reasoning strategies. Test learning mechanisms."*

### For Startups
*"MVP your AI product idea fast. Scale when it works. Pay only for APIs."*

---

## Competitive Advantages

✅ **Full Stack** - Backend + Frontend included
✅ **Transparent** - See every decision in real-time
✅ **Learning** - Persistent memory compounds
✅ **Practical** - Actual execution, not simulation
✅ **Open** - MIT license, open source
✅ **Fast** - 15 min setup to working agent
✅ **Extensible** - Add tools, customize prompts, build on top

---

This is **not** another chatbot wrapper. This is a **learning framework** for building better AI systems.

**Spiral: Where AI gets smarter.** 🌀
