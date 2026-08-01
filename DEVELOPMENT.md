# 🛠️ Jarvis - Developer Guide

How to extend and customize Jarvis for your use case.

---

## Adding New Tools

### Step 1: Create Tool Class

In `backend/agents/tools.py`:

```python
class WebSearchTool:
    """Search the web using a search API."""
    
    def __init__(self):
        self.api_key = os.getenv("SEARCH_API_KEY")
    
    def search(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """Execute search."""
        try:
            # Your search implementation
            results = []  # Call API
            return {
                "success": True,
                "results": results,
                "count": len(results)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
```

### Step 2: Register in Dispatcher

In `execute_tool()` function:

```python
elif tool_name == "web_search":
    action = tool_input.get("action")
    if action == "search":
        return web_search_tool.search(
            tool_input.get("query", ""),
            tool_input.get("limit", 5)
        )
```

### Step 3: Update Prompts

In `backend/core/prompts.py`, add tool to `PLANNER_PROMPT`:

```python
PLANNER_PROMPT = """
...
Available tools:
- file_manager: Create/read/write files
- python_executor: Run Python code
- web_search: Search the web
...
"""
```

### Step 4: Test

```python
# In Python console
from agents.tools import execute_tool

result = execute_tool("web_search", {
    "action": "search",
    "query": "AI latest news",
    "limit": 5
})
print(result)
```

---

## Customizing Node Behavior

### Edit System Prompts

In `backend/core/prompts.py`:

```python
# Current prompt
ANALYZER_PROMPT = "Analyze user intent..."

# Customize for your domain
ANALYZER_PROMPT = """
You are an AI assistant specialized in DOMAIN.
Understand user requests in the context of DOMAIN.
Detect intents specific to DOMAIN.
...
"""
```

### Modify Node Logic

In `backend/loop_engine/graph.py`:

```python
def node_analyzer(self, state: JarvisState) -> Dict[str, Any]:
    # Current implementation
    
    # Customize here
    # Add domain-specific logic
    # Validate intent for your domain
    
    return state
```

---

## Adding Memory Types

### Store Specialized Memory

In `node_learning()`:

```python
# Store different memory types
mem0_client.add_memory(
    messages=[
        {"role": "user", "content": "User request"},
        {"role": "assistant", "content": "Learned pattern"}
    ],
    user_id=user_id,
    memory_type="domain_pattern"  # Custom type
)
```

### Retrieve Specialized Memory

In `node_memory_retriever()`:

```python
# Search specific memory type
domain_memories = mem0_client.search_memories(
    query=state["goal"],
    user_id=state["user_id"],
    limit=3,
    memory_type="domain_pattern"  # Custom type
)
```

---

## Creating Custom LLM Nodes

### Add New Node to Loop

In `backend/loop_engine/graph.py`:

```python
def node_researcher(self, state: JarvisState) -> Dict[str, Any]:
    """New node to research complex questions."""
    state["current_node"] = "researcher"
    
    prompt = "Research this question: " + state["goal"]
    response = self._llm_call(prompt)
    
    state["research"] = response
    state["messages"].append({
        "node": "researcher",
        "result": response[:100]
    })
    
    return state

# Add to graph
graph.add_node("researcher", self.node_researcher)
```

### Add Node to Graph Flow

```python
# Add edge
graph.add_edge("planner", "researcher")
graph.add_edge("researcher", "executor")
```

---

## Integrating External APIs

### Example: GitHub Integration

```python
# In agents/tools.py

class GitHubTool:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"
    
    def create_repo(self, name: str) -> Dict[str, Any]:
        """Create GitHub repository."""
        headers = {"Authorization": f"token {self.token}"}
        response = requests.post(
            f"{self.base_url}/user/repos",
            json={"name": name},
            headers=headers
        )
        return {
            "success": response.status_code == 201,
            "repo_url": response.json().get("html_url")
        }
```

### Add to Tool Dispatcher

```python
elif tool_name == "github":
    action = tool_input.get("action")
    if action == "create_repo":
        return github_tool.create_repo(tool_input.get("name", ""))
```

---

## Custom Prompting Strategy

### Domain-Specific System Prompt

```python
# Override analyzer for your domain

DOMAIN_ANALYZER = """
You are an AI assistant for [DOMAIN].

Your role:
1. Understand [DOMAIN] terminology
2. Recognize [DOMAIN] patterns
3. Make [DOMAIN]-specific decisions

When analyzing requests:
- Consider [DOMAIN] constraints
- Apply [DOMAIN] best practices
- Suggest [DOMAIN] solutions

Available intents:
- [DOMAIN]-specific intent 1
- [DOMAIN]-specific intent 2
"""
```

---

## Frontend Customization

### Add Custom Component

```jsx
// frontend/src/components/CustomPanel.jsx

import React from 'react';
import './CustomPanel.css';

function CustomPanel({ data }) {
  return (
    <div className="custom-panel">
      {/* Your custom UI */}
    </div>
  );
}

export default CustomPanel;
```

### Integrate into App

```jsx
// frontend/src/App.jsx

import CustomPanel from './components/CustomPanel';

function App() {
  return (
    <div className="app-container">
      <ChatInterface />
      <LoopStatus />
      <CustomPanel data={data} />
    </div>
  );
}
```

---

## Testing Extensions

### Unit Test Example

```python
# backend/tests/test_tools.py

import pytest
from agents.tools import execute_tool

def test_file_creation():
    result = execute_tool("file_manager", {
        "action": "write_file",
        "path": "test.txt",
        "content": "test"
    })
    assert result["success"] == True
    assert result["path"]

def test_python_execution():
    result = execute_tool("python_executor", {
        "action": "execute_code",
        "code": "print('hello')"
    })
    assert result["success"] == True
    assert "hello" in result["stdout"]
```

### Run Tests

```bash
cd backend
pytest tests/ -v
```

---

## Performance Optimization

### Caching Memories

```python
# Cache frequently accessed memories

class MemoryCache:
    def __init__(self, ttl=300):
        self.cache = {}
        self.ttl = ttl
    
    def get(self, key):
        # Check if cached and not expired
        if key in self.cache:
            return self.cache[key]
        return None
    
    def set(self, key, value):
        self.cache[key] = {
            "value": value,
            "time": time.time()
        }
```

### Parallel Tool Execution

```python
# Execute multiple tools in parallel (Phase 2+)

import asyncio

async def execute_tools_parallel(tools_list):
    tasks = [
        execute_tool(tool["name"], tool["input"])
        for tool in tools_list
    ]
    return await asyncio.gather(*tasks)
```

---

## Monitoring & Logging

### Add Custom Logging

```python
import logging

logger = logging.getLogger(__name__)

logger.info(f"Task started: {goal}")
logger.debug(f"Retrieved {len(memories)} memories")
logger.warning(f"Retry attempt {retry_count}")
logger.error(f"Tool failed: {error}")
```

### Structured Logging

```python
import json

log_entry = {
    "timestamp": datetime.now().isoformat(),
    "user_id": state["user_id"],
    "node": state["current_node"],
    "success": state["success"],
    "duration": execution_time
}
logger.info(json.dumps(log_entry))
```

---

## Error Handling Strategy

### Custom Error Handler

```python
def handle_tool_error(tool_name: str, error: str) -> str:
    """Custom error handling strategy."""
    
    if "timeout" in error.lower():
        return "Tool took too long. Retrying with smaller input..."
    
    elif "memory" in error.lower():
        return "Out of memory. Simplifying task..."
    
    elif "api" in error.lower():
        return "API error. Checking authentication..."
    
    return "Unknown error. Check logs for details."
```

---

## State Augmentation

### Add Custom State Fields

```python
# In core/state.py

class JarvisState(TypedDict, total=False):
    # ... existing fields ...
    
    # Your custom fields
    domain_context: str
    custom_metadata: Dict[str, Any]
    custom_result: str
```

### Use in Nodes

```python
def node_custom(self, state: JarvisState) -> Dict[str, Any]:
    # Access custom fields
    context = state.get("domain_context", "")
    
    # Set custom fields
    state["custom_result"] = "..."
    
    return state
```

---

## Deployment Customization

### Docker Build

```dockerfile
# Dockerfile.backend

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ ./backend/

ENV PYTHONUNBUFFERED=1
CMD ["python", "backend/main.py"]
```

### Environment-Specific Config

```python
# In core/config.py

import os

ENV = os.getenv("ENV", "development")

if ENV == "production":
    DEBUG = False
    LOG_LEVEL = "WARNING"
    MAX_RETRIES = 2
elif ENV == "staging":
    DEBUG = True
    LOG_LEVEL = "INFO"
    MAX_RETRIES = 3
else:  # development
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    MAX_RETRIES = 3
```

---

## Versioning Strategy

### API Versioning

```python
# backend/main.py

@app.post("/v1/chat")
async def chat_v1(request: MessageRequest):
    # Version 1 implementation
    pass

@app.post("/v2/chat")
async def chat_v2(request: MessageRequestV2):
    # Version 2 with new features
    pass
```

---

## Documentation

### Code Documentation

```python
def node_custom(self, state: JarvisState) -> Dict[str, Any]:
    """
    Custom node that does X.
    
    Args:
        state: Current JarvisState
    
    Returns:
        Updated JarvisState
    
    Raises:
        ValueError: If X condition
    
    Example:
        >>> state = create_initial_state("user", "test")
        >>> result = engine.node_custom(state)
    """
    pass
```

### API Documentation

```python
@app.post("/custom")
async def custom_endpoint(request: CustomRequest):
    """
    Create or update something.
    
    Parameters:
    - param1: Description
    - param2: Description
    
    Returns:
    - success: bool
    - data: CustomResponse
    """
    pass
```

---

## Best Practices

1. **Error Handling**: Always catch exceptions in tools
2. **Logging**: Log important decisions and errors
3. **Testing**: Write tests for custom code
4. **Documentation**: Document your extensions
5. **Performance**: Measure and optimize
6. **Security**: Validate all inputs
7. **Modularity**: Keep code organized
8. **Backwards Compatibility**: Don't break existing APIs

---

## Common Patterns

### Conditional Node Execution

```python
def should_run_research(state: JarvisState) -> bool:
    return "research" in state["intent"]

graph.add_conditional_edges(
    "planner",
    should_run_research,
    {
        True: "researcher",
        False: "executor"
    }
)
```

### Memory-Based Routing

```python
# Choose tool based on memory

def select_tool(state: JarvisState) -> str:
    memories = state["relevant_memories"]
    
    for mem in memories:
        if "tool_X_works_well" in mem.get("content", ""):
            return "tool_X"
    
    return "default_tool"
```

---

## Troubleshooting Customizations

### Debug Custom Node

```python
def node_custom(self, state: JarvisState) -> Dict[str, Any]:
    logger.debug(f"Input state: {state}")
    
    try:
        # Your code
        result = process(state)
    except Exception as e:
        logger.error(f"Error in custom node: {e}", exc_info=True)
        raise
    
    logger.debug(f"Output state: {state}")
    return state
```

### Test in Isolation

```python
# Test custom code without full loop

from loop_engine.graph import LoopEngine

engine = LoopEngine()
state = create_initial_state("user", "test")
result = engine.node_custom(state)
print(result)
```

---

## Extension Checklist

- [ ] Created new component/tool/node
- [ ] Added to dispatcher/graph
- [ ] Updated prompts if needed
- [ ] Added error handling
- [ ] Added logging
- [ ] Wrote tests
- [ ] Updated documentation
- [ ] Verified it works end-to-end
- [ ] Checked for performance impact
- [ ] Got code review (if team)

---

## Resources

- LangGraph Docs: https://python.langchain.com/docs/langgraph
- FastAPI Docs: https://fastapi.tiangolo.com
- React Docs: https://react.dev
- Anthropic API: https://docs.anthropic.com
- Mem0 Docs: https://docs.mem0.ai

---

**You now have a fully extensible framework. Build anything on top of it!** 🚀
