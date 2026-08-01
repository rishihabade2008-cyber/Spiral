# 🏗️ Jarvis Phase 1 - Architecture & Design

Deep dive into how Jarvis works, why it's designed this way, and how to extend it.

## 🧠 The Core Concept

Jarvis is **not a chatbot**. It's an **agentic loop** that continuously:

```
THINK → PLAN → ACT → OBSERVE → REFLECT → LEARN → REPEAT
```

This loop is implemented as a **LangGraph state machine** with 7 nodes.

---

## 📊 The 7-Node Loop Engine

### Node 1: Analyzer 🔍

**Purpose**: Understand user intent

**Input**: User message
**Output**: 
```json
{
  "intent": "coding|research|automation|chat|...",
  "goal": "Clear statement of what to do",
  "subtasks": ["list of high-level subtasks"]
}
```

**Why this matters**: 
- Different intents → different strategies
- Clear goal → better planning
- Subtasks → recursive breakdown of complexity

**When it fails**: If intent is wrong, everything downstream fails

---

### Node 2: Memory Retriever 💾

**Purpose**: Find relevant past experiences

**Input**: Goal (semantic search query)
**Output**: List of relevant memories from Mem0

**What it searches for**:
- User preferences ("prefers Python")
- Project decisions ("uses FastAPI")
- Successful strategies ("run tests first")
- Failed approaches ("avoid this")

**Why this matters**:
- Learns from past
- Makes consistent decisions
- Avoids repeated mistakes
- Personalizes behavior

**Key insight**: Memory is a **vector database** (Mem0), not conversation history.

---

### Node 3: Planner 📋

**Purpose**: Break goal into actionable steps

**Input**: 
- Goal
- Retrieved memories (for context)

**Output**: 
```json
{
  "steps": [
    {
      "step": 1,
      "task": "specific action",
      "tool": "file_manager|python_executor|web_search|...",
      "description": "why this matters"
    }
  ]
}
```

**Why this matters**:
- Prevents hallucination (concrete plan)
- Makes progress visible
- Enables checkpoint recovery
- Tool routing is explicit

**Design principle**: One step = one tool call (atomic operations)

---

### Node 4: Executor ⚙️

**Purpose**: Do the actual work

**What it does**:
1. Takes current step from plan
2. Translates to tool input
3. Calls the tool (file ops, Python, web search, etc.)
4. Returns result (success or error)

**Key feature**: **Bounded execution** - one tool call per loop iteration
- Prevents infinite loops
- Enables recovery
- Makes debugging easier

**Tool routing**:
```python
if step.tool == "file_manager":
    # Create/read/delete files
elif step.tool == "python_executor":
    # Run Python code or scripts
elif step.tool == "web_search":
    # Search the web (phase 2+)
```

---

### Node 5: Observer 👁️

**Purpose**: Record what happened factually

**Input**: Tool result (success or error)
**Output**: Structured observations

**Example**:
```json
{
  "action_completed": true,
  "output_available": true,
  "error_occurred": false,
  "observations": [
    "File was created",
    "File size: 1024 bytes",
    "No errors"
  ]
}
```

**Why separate from Reflection?**
- Clear facts vs. interpretation
- Enables audit trail
- Reproducible for debugging

**Design principle**: Observation doesn't judge, it just records

---

### Node 6: Reflection 🧠

**Purpose**: Decide what to do next

**Questions it asks**:
1. Did the action work?
2. Is there an error?
3. Can we automatically fix it?
4. Should we retry?
5. Should we try a different tool?
6. Is user approval needed?

**Output**:
```json
{
  "success": true/false,
  "error_type": "if failed",
  "can_retry": true/false,
  "repair_suggestion": "how to fix",
  "next_action": "retry|try_different_tool|continue|ask_user"
}
```

**Retry logic**:
```
if not success and can_retry and retry_count < max_retries:
    → Retry same step
else if success or retry_count >= max_retries:
    → Move to next step
```

**Design principle**: Exponential backoff - each retry is more conservative

---

### Node 7: Learning 📚

**Purpose**: Extract and save learnings

**What it extracts**:
- **User memories**: Preferences, style, constraints
- **Project memories**: Architecture, decisions, patterns
- **Strategy memories**: What worked, what didn't
- **Failure learnings**: Common pitfalls

**What NOT to learn**:
- Temporary file names
- Timestamps
- Specific tool outputs
- One-off fixes

**Saving to Mem0**:
```python
mem0_client.add_memory(
    messages=[
        {"role": "user", "content": original_request},
        {"role": "assistant", "content": json.dumps(learnings)}
    ],
    user_id=user_id,
    memory_type="learning"
)
```

**Why this matters**: 
- Exponential learning (memory compounds)
- Future tasks are smarter
- Agent gets personalized to each user
- Solves cold-start problem

---

## 🔄 Loop Flow Diagram

```
START
  ↓
[1. ANALYZER]
  ↓
[2. MEMORY RETRIEVER]
  ↓
[3. PLANNER]
  ↓
┌─────────────────────────┐
│  EXECUTION LOOP         │
│                         │
│ [4. EXECUTOR]           │
│  ↓                      │
│ [5. OBSERVER]           │
│  ↓                      │
│ [6. REFLECTION]         │
│  ↓                      │
│  Success? ────────┐     │
│   ├─ Yes  →  Next Step  │
│   └─ No   →  Retry?     │
│             ├─ Yes  → Loop
│             └─ No   → Learn
└─────────────────────────┘
  ↓
[7. LEARNING]
  ↓
END
```

---

## 💾 State Management

The entire loop state flows through as a single object: **JarvisState**

```python
class JarvisState:
    # User & Session
    user_id: str
    session_id: str
    
    # Current task
    goal: str
    plan: List[Dict]
    current_step: int
    
    # Current execution
    tool_name: str
    tool_input: Dict
    tool_result: Any
    
    # Reflection
    reflection: str
    success: bool
    can_retry: bool
    retry_count: int
    
    # Learning
    learning: str
    relevant_memories: List
    
    # Metadata
    messages: List  # Loop history
    loop_iteration: int
```

**Why a single state?**
- LangGraph requirement
- Clear data flow
- Easy to serialize/restore
- Enables checkpoint/recovery

---

## 🔌 Tool Architecture

### Adding a New Tool

```python
# In agents/tools.py

class MyTool:
    def execute(self, params: Dict) -> Dict[str, Any]:
        # Do work
        return {
            "success": bool,
            "result": output,
            "error": error_message
        }

# In execute_tool():
elif tool_name == "my_tool":
    return my_tool.execute(tool_input)
```

### Tool Contract

Every tool must:
1. Accept a Dict input
2. Return a Dict with `success` (bool)
3. Never raise exceptions (catch and return error)
4. Complete within `PYTHON_TIMEOUT`

### Built-in Tools

#### File Manager
```python
{
  "action": "write_file|read_file|create_folder|list_files|delete",
  "path": "relative/path",
  "content": "file content (for write_file)"
}
```

#### Python Executor
```python
{
  "action": "execute_code|execute_script|run_command",
  "code": "python code",
  "script_path": "path/to/script.py",
  "command": "shell command"
}
```

---

## 🧠 Memory Architecture

### Memory Types

```
┌─────────────────────────────────────┐
│        MEMORY SYSTEM (Mem0)         │
├─────────────────────────────────────┤
│ 1. EPISODIC MEMORY (Conversations)  │
│    - What happened                  │
│    - When it happened               │
│    - Outcome                        │
│                                     │
│ 2. SEMANTIC MEMORY (Facts)          │
│    - User prefers X                 │
│    - Project uses Y                 │
│    - Learned pattern Z              │
│                                     │
│ 3. PROCEDURAL MEMORY (Skills)       │
│    - How to do X                    │
│    - When to use Y                  │
│    - Successful strategies          │
└─────────────────────────────────────┘
```

### Memory Search

```python
# Semantic search by query
memories = mem0_client.search_memories(
    query="How to build a Python project?",
    user_id=user_id,
    limit=5
)

# Returns top 5 most relevant memories using vector similarity
```

### Memory Saving

```python
# After task completes
learnings = ["User likes Python", "Projects need README"]
mem0_client.add_memory(
    messages=[
        {"role": "user", "content": original_request},
        {"role": "assistant", "content": json.dumps(learnings)}
    ],
    user_id=user_id
)
```

---

## 🌐 Frontend Architecture

### Real-time Communication

Uses **WebSocket** for streaming responses:

```javascript
ws = new WebSocket('ws://localhost:8000/ws/chat');
ws.send(JSON.stringify({message: "...", user_id: "..."}));
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === "thinking") updateLoopStatus(data);
  if (data.type === "result") displayFinalResult(data);
};
```

### Three Main Components

1. **ChatInterface** - User input/output
2. **LoopStatus** - Real-time node visualization
3. **PlanViewer** - Task breakdown

Each subscribes to different message types from WebSocket.

---

## 🔌 API Design

### WebSocket Messages

**From Backend**:
```json
{
  "type": "status|thinking|result|error",
  "content": {
    "current_node": "analyzer",
    "message": "Processing...",
    "data": {}
  }
}
```

**To Backend**:
```json
{
  "message": "user input",
  "user_id": "unique_id"
}
```

### Response Types

- `status` - Node changed
- `thinking` - Intermediate update
- `result` - Final answer
- `error` - Error occurred

---

## 🚀 Performance Characteristics

### Timing

- **Single step execution**: ~2-5 seconds (API calls)
- **Full task (3-5 steps)**: ~10-25 seconds
- **With retries**: ~30-60 seconds max (3 max retries)

### Scaling

- **Concurrency**: Single user per connection (WebSocket)
- **Memory**: ~100MB base + ~10MB per active session
- **API calls**: ~2-3 Claude calls per loop + 1-2 Mem0 calls

### Optimization Opportunities

1. Parallel step execution (phase 2)
2. Memory caching (frequently used)
3. Prompt optimization (fewer tokens)
4. Tool batching (multiple files at once)

---

## 🐛 Error Handling Strategy

### Three-tier approach:

1. **Tool Level**: Catch all exceptions, return error
2. **Reflection Level**: Decide if recoverable
3. **Loop Level**: Max retries = bail out

### Recovery Types

```
Tool Error
  → Can auto-fix? → Repair → Retry
  → Can't fix? → Reflect → Retry or Ask User
  → Max retries? → Learning → Next Task
```

### Logging

Every step is logged:
```python
logger.info(f"Node: {node_name}, Step: {step}, Success: {success}")
```

Check backend console for full execution trace.

---

## 🎯 Design Decisions & Why

### Why LangGraph?

- State machine semantics
- Built for agent loops
- Checkpointing support
- Streaming built-in
- Production-grade

### Why Mem0 API?

- Managed vector database
- Semantic search built-in
- No infrastructure needed
- Easy for hackathon
- Scalable

### Why FastAPI + React?

- FastAPI: Async, WebSocket, type hints
- React: Real-time updates, component reuse
- Together: Efficient for rapid prototyping

### Why WebSocket?

- Streaming responses
- Real-time UI updates
- Lower latency than polling
- Natural for agent loops

---

## 🔮 Extension Points

### Phase 2: Add Tools
```python
# New tool in agents/tools.py
class WebSearchTool:
    def search(self, query: str):
        # Implement search
        pass
```

### Phase 3: Add Memory Types
```python
# Add "project_state" memory type
# Track evolving project architecture
```

### Phase 4: Multi-Agent
```python
# Executor routes to different agents
# Coder Agent, Researcher Agent, etc.
```

### Phase 5: Browser Automation
```python
# New tool using Playwright
# Click, type, extract from web
```

---

## 📈 Metrics to Track

For production:

1. **Success rate**: % of tasks completed
2. **Retry rate**: % that needed retries
3. **Learning quality**: How well memories help future tasks
4. **User satisfaction**: Feedback on results
5. **Cost**: API calls per task

---

## 🎓 Learning Resources

1. **LangGraph Docs**: https://python.langchain.com/docs/langgraph
2. **Mem0 API**: https://docs.mem0.ai
3. **Claude API**: https://docs.anthropic.com
4. **Agent Papers**:
   - "ReAct: Synergizing Reasoning and Acting" (Yao et al.)
   - "Self-Refine: Iterative Refinement with Self-Feedback" (Madaan et al.)

---

This is a **production-ready foundation** for self-learning agents. Extend it for your use case.

**Key principle**: The loop is the learning mechanism. Every iteration makes the agent smarter for next time.

---

Build, measure, learn. 🚀
