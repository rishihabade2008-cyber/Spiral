# 📡 Jarvis API Reference

Complete documentation of all HTTP and WebSocket endpoints.

---

## Base URL

```
http://localhost:8000
```

---

## REST Endpoints

### Health Check

**Endpoint**: `GET /health`

**Response**: 
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

**Use case**: Verify backend is running

**cURL**:
```bash
curl http://localhost:8000/health
```

**JavaScript**:
```javascript
const response = await fetch('http://localhost:8000/health');
const data = await response.json();
console.log(data.status);  // "healthy"
```

---

### Send Chat Message (Blocking)

**Endpoint**: `POST /chat`

**Request**:
```json
{
  "message": "Create a Python calculator",
  "user_id": "user123"
}
```

**Response**:
```json
{
  "success": true,
  "final_answer": "Created calculator.py with...",
  "learning": "User prefers clean code",
  "goal": "Create a Python calculator",
  "plan": [
    {
      "step": 1,
      "task": "Create project folder",
      "tool": "file_manager",
      "description": "..."
    }
  ],
  "messages": [
    {
      "node": "analyzer",
      "intent": "coding",
      "goal": "..."
    }
  ]
}
```

**Use case**: Simple synchronous API call

**cURL**:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Create a Python calculator",
    "user_id": "user123"
  }'
```

**JavaScript**:
```javascript
const response = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'Create a Python calculator',
    user_id: 'user123'
  })
});
const data = await response.json();
console.log(data.final_answer);
```

**Python**:
```python
import requests

response = requests.post('http://localhost:8000/chat', json={
    'message': 'Create a Python calculator',
    'user_id': 'user123'
})
print(response.json()['final_answer'])
```

---

### Get Configuration

**Endpoint**: `GET /config`

**Response**:
```json
{
  "max_retries": 3,
  "max_loop_iterations": 20,
  "python_timeout": 30
}
```

**Use case**: Client-side configuration

**cURL**:
```bash
curl http://localhost:8000/config
```

---

## WebSocket Endpoint

### Real-time Chat

**Endpoint**: `WS /ws/chat`

**Connect**:
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chat');
```

**Send Message**:
```javascript
ws.send(JSON.stringify({
  message: "Create a Python calculator",
  user_id: "user123"
}));
```

**Message Types Received**:

#### Status Update
```json
{
  "type": "status",
  "content": {
    "current_node": "analyzer",
    "message": "Analyzing your request..."
  }
}
```

#### Thinking/Progress
```json
{
  "type": "thinking",
  "content": {
    "node": "planner",
    "steps_count": 5,
    "plan": [...]
  }
}
```

#### Final Result
```json
{
  "type": "result",
  "content": {
    "final_answer": "Created calculator.py...",
    "learning": "User prefers clean code",
    "goal": "Create a Python calculator",
    "plan": [...],
    "success": true
  }
}
```

#### Error
```json
{
  "type": "error",
  "content": {
    "error": "API key not configured"
  }
}
```

**Full Example**:
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chat');

ws.onopen = () => {
  console.log('Connected');
  ws.send(JSON.stringify({
    message: 'Create a Python calculator',
    user_id: 'user123'
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.type === 'status') {
    console.log(`Node: ${data.content.current_node}`);
  } else if (data.type === 'thinking') {
    console.log(`Progress: ${data.content.message}`);
  } else if (data.type === 'result') {
    console.log(`Done: ${data.content.final_answer}`);
  } else if (data.type === 'error') {
    console.error(data.content.error);
  }
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('Disconnected');
};
```

---

## Data Types

### JarvisState

The core state object flowing through the loop:

```typescript
interface JarvisState {
  // User & Session
  user_id: string;
  session_id: string;
  
  // Input
  user_message: string;
  intent: string;
  
  // Memory
  relevant_memories: Array<{memory: string, [key: string]: any}>;
  
  // Planning
  goal: string;
  plan: Array<{
    step: number;
    task: string;
    tool: string;
    description: string;
  }>;
  plan_summary: string;
  
  // Execution
  current_step: number;
  current_action: string;
  
  // Tool execution
  tool_name: string;
  tool_input: Record<string, any>;
  tool_result: any;
  tool_error: string | null;
  
  // Observation
  observations: string[];
  
  // Reflection
  reflection: string;
  success: boolean;
  error_type: string;
  can_retry: boolean;
  
  // Retry
  retry_count: number;
  max_retries: number;
  
  // Learning
  learning: string;
  
  // Output
  final_answer: string;
  
  // Metadata
  messages: Array<{node: string, [key: string]: any}>;
  loop_history: Array<any>;
  current_node: string;
  loop_iteration: number;
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Empty message"
}
```

### 500 Internal Server Error
```json
{
  "error": "Error description"
}
```

### WebSocket Errors
```json
{
  "type": "error",
  "content": {
    "error": "Error message"
  }
}
```

---

## Rate Limiting

**Not implemented in Phase 1**

Phase 2+ will add:
- Per-user rate limiting
- Per-IP rate limiting
- Token bucket algorithm

---

## Authentication

**Not implemented in Phase 1**

Phase 2+ will add:
- API key authentication
- JWT tokens
- User sessions

---

## CORS Headers

Current CORS configuration:
```python
allow_origins=[
  "http://localhost:3000",
  "http://localhost:5173"
]
```

To allow other origins, edit `backend/main.py`:
```python
allow_origins=["*"]  # WARNING: Not secure for production
```

---

## Request/Response Examples

### Example 1: Simple Text-to-File Task

**Request**:
```json
{
  "message": "Create a file named test.txt with 'Hello World'",
  "user_id": "demo"
}
```

**Response Flow** (WebSocket):
1. `status`: "analyzer" - Understanding request
2. `thinking`: "planner" - Creating plan
3. `thinking`: "executor" - Creating file
4. `thinking`: "reflection" - Checking success
5. `result`: Success with file path

---

### Example 2: Python Code Generation

**Request**:
```json
{
  "message": "Write a Python script that calculates factorial",
  "user_id": "demo"
}
```

**Response Flow**:
1. `status`: "Analyzing coding task"
2. `thinking`: Plan includes code generation + execution
3. `thinking`: Code created and executed
4. `result`: Success with output

---

### Example 3: Multi-Step Project

**Request**:
```json
{
  "message": "Create a Python project with structure, code, and README",
  "user_id": "demo"
}
```

**Response Flow**:
1. `status`: "analyzer"
2. `thinking`: Plan has 5+ steps
3. `thinking`: Each step executes and reports
4. `result`: Complete project created

---

## Integration Examples

### Python Client

```python
import requests
import json

class JarvisClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def chat(self, message, user_id="default"):
        """Send blocking request"""
        response = requests.post(
            f"{self.base_url}/chat",
            json={"message": message, "user_id": user_id}
        )
        return response.json()
    
    def health(self):
        """Check if backend is running"""
        response = requests.get(f"{self.base_url}/health")
        return response.json()

# Usage
client = JarvisClient()
result = client.chat("Create a Python calculator")
print(result['final_answer'])
```

### JavaScript Client

```javascript
class JarvisClient {
  constructor(baseUrl = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
  }
  
  async chat(message, userId = 'default') {
    const response = await fetch(`${this.baseUrl}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, user_id: userId })
    });
    return response.json();
  }
  
  async health() {
    const response = await fetch(`${this.baseUrl}/health`);
    return response.json();
  }
}

// Usage
const client = new JarvisClient();
client.chat('Create a Python calculator').then(result => {
  console.log(result.final_answer);
});
```

---

## Webhooks (Phase 2+)

Planned webhook support:

```python
# Register webhook
POST /webhooks
{
  "url": "https://myapp.com/jarvis-callback",
  "events": ["task_complete", "error"]
}

# Jarvis will POST to your webhook when:
# - Task completes
# - Error occurs
# - Learning saved
```

---

## Batch Requests (Phase 2+)

Planned batch API:

```json
POST /batch
{
  "requests": [
    {"message": "Task 1", "user_id": "user1"},
    {"message": "Task 2", "user_id": "user2"},
    {"message": "Task 3", "user_id": "user3"}
  ]
}
```

---

## Testing Endpoints

### cURL Examples

```bash
# Health check
curl http://localhost:8000/health

# Get config
curl http://localhost:8000/config

# Send message
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "test",
    "user_id": "debug"
  }'

# WebSocket (using websocat)
echo '{"message":"test","user_id":"debug"}' | \
  websocat ws://localhost:8000/ws/chat
```

### Postman

1. Create collection "Jarvis"
2. Add requests:
   - GET http://localhost:8000/health
   - POST http://localhost:8000/chat (body: JSON)
   - WebSocket ws://localhost:8000/ws/chat

---

## Performance Metrics

API response times (typical):

| Endpoint | Time | Notes |
|----------|------|-------|
| `/health` | <10ms | No API calls |
| `/config` | <10ms | Static config |
| `/chat` | 10-30s | Depends on loop iterations |
| `/ws/chat` | Streaming | Updates as loop progresses |

---

## Limitations

- **Sequential**: Only one request at a time per user
- **Stateless**: Each request is independent
- **No persistence**: Sessions don't persist across restarts
- **No auth**: Anyone can send requests

---

## Roadmap

**Phase 1** ✅: Core REST + WebSocket
**Phase 2**: Authentication + Rate limiting
**Phase 3**: Batch requests + Webhooks
**Phase 4**: Streaming responses + Server-sent events
**Phase 5**: GraphQL endpoint

---

## Support

For API issues:
1. Check `/health` endpoint
2. Verify backend is running
3. Check browser console for errors
4. Read TROUBLESHOOTING.md
5. Check logs: `backend/main.py` output

---

**API is production-ready for Phase 1. Ready to integrate!** 🚀
