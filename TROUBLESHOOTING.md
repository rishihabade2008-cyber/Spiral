# 🐛 Jarvis - Troubleshooting Guide

Common issues and solutions.

---

## ⚡ Quick Fixes

**First, always try:**
1. Stop both backend and frontend
2. Clear browser cache (Ctrl+Shift+Delete)
3. Restart both servers
4. Refresh browser (Ctrl+F5)

If that doesn't work, continue below.

---

## 🔧 Backend Issues

### Error: "ModuleNotFoundError: No module named 'anthropic'"

**Cause**: Dependencies not installed

**Fix**:
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r ../requirements.txt
```

---

### Error: "MEM0_API_KEY not set"

**Cause**: Environment variables not configured

**Fix**:
```bash
cd backend
cp .env.example .env
# Edit .env with your text editor
# Add: MEM0_API_KEY=your_actual_key_here
# Add: ANTHROPIC_API_KEY=your_actual_key_here
```

**Verify**:
```bash
python -c "from core.config import config; config.validate()"
```

---

### Error: "ANTHROPIC_API_KEY not set"

**Fix**: Same as above - edit backend/.env

**Test your key**:
```bash
curl https://api.anthropic.com/v1/models \
  -H "x-api-key: $ANTHROPIC_API_KEY"
```

---

### Error: "Port 8000 already in use"

**Cause**: Another process on port 8000

**Fix - Find and kill**:
```bash
# Mac/Linux
lsof -i :8000
kill -9 <PID>

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Or change port**:
```bash
# In backend/.env
PORT=8001

# Then run
python main.py
```

---

### Error: "Connection refused" when testing API

**Cause**: Backend not running

**Fix**:
1. Check backend is running: `python backend/main.py`
2. Should see: `Uvicorn running on http://0.0.0.0:8000`
3. Test: `curl http://localhost:8000/health`

---

### Error: "Timeout" or very slow responses

**Cause**: 
- Mem0 API is slow
- Claude API is slow
- Tool execution is slow

**Fix**:
```bash
# Check Mem0 API status
curl https://api.mem0.ai/v1/memories/ \
  -H "Authorization: Token $MEM0_API_KEY"

# Check Claude API
python -c "from anthropic import Anthropic; c = Anthropic(); print(c.messages.create(model='claude-opus-4-6', max_tokens=10, messages=[{'role': 'user', 'content': 'hi'}]))"

# Increase timeout in backend/.env
PYTHON_TIMEOUT=60
```

---

### Backend crashes with error

**Check logs**:
```bash
# Run in foreground to see full traceback
cd backend
source venv/bin/activate
python main.py  # Ctrl+C to stop
```

**Common errors**:
- `ImportError` - Missing dependency (pip install)
- `ValueError` - Missing config (check .env)
- `ConnectionError` - API unreachable (check network)

---

## 🎨 Frontend Issues

### Error: "Port 3000 already in use"

**Fix**:
```bash
# Find process on port 3000
lsof -i :3000  # Mac/Linux
netstat -ano | findstr :3000  # Windows

# Kill it
kill -9 <PID>  # Mac/Linux
taskkill /PID <PID> /F  # Windows
```

---

### Frontend shows "Connection error"

**Cause**: Frontend can't reach backend

**Fix**:
1. Make sure backend is running on port 8000
2. Test: `curl http://localhost:8000/health`
3. Should return: `{"status":"healthy","version":"1.0.0"}`

**If backend is running but frontend can't connect:**
```bash
# Check CORS
# In backend/main.py, should see:
# allow_origins=["http://localhost:3000", "http://localhost:5173"]

# Restart both servers
# Clear browser cache
# Try incognito mode
```

---

### Error: "Cannot find node_modules"

**Fix**:
```bash
cd frontend
npm install
npm run dev
```

---

### Error: "Vite not found"

**Fix**:
```bash
cd frontend
npm install --save-dev vite @vitejs/plugin-react
npm run dev
```

---

### Styles not loading / UI looks broken

**Fix**:
1. Clear browser cache (Ctrl+Shift+Delete)
2. Hard refresh (Ctrl+Shift+F5)
3. Close all browser tabs and reopen
4. Restart Vite dev server

---

### WebSocket connection fails

**Cause**: Frontend can't connect to WebSocket

**Fix**:
1. Backend must be running
2. Frontend must connect to `ws://localhost:8000/ws/chat`
3. Check browser console (F12) for errors
4. Try in different browser (Safari, Firefox)

**Debug**:
```javascript
// In browser console
ws = new WebSocket('ws://localhost:8000/ws/chat');
ws.onopen = () => console.log('Connected!');
ws.onerror = (e) => console.log('Error:', e);
ws.onclose = () => console.log('Closed');
```

---

## 📊 Full Stack Issues

### "Nothing happens when I send a message"

**Checklist**:
- [ ] Backend running? (terminal shows `Uvicorn running`)
- [ ] Frontend running? (terminal shows `VITE ready`)
- [ ] Browser shows no errors? (F12 console)
- [ ] API keys set? (backend/.env)
- [ ] Network connection? (can you browse internet)

**Debug**:
1. Open browser console (F12)
2. Open backend terminal
3. Send message and watch both
4. Screenshot error messages
5. Post on GitHub issues

---

### Slow responses (10+ seconds)

**Normal**: 2-3 seconds per loop iteration
**Slow**: >5 seconds per iteration

**Causes**:
1. Mem0 API is slow
2. Claude API is overloaded
3. Network connection is slow
4. Tool execution is slow

**Fix**:
1. Try during off-peak hours
2. Reduce MAX_LOOP_ITERATIONS in .env
3. Use simpler prompts
4. Check your internet speed

---

### Memory not working

**Cause**: Mem0 API key invalid or API unreachable

**Fix**:
```bash
# Test Mem0 API
curl https://api.mem0.ai/v1/memories/ \
  -H "Authorization: Token YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "query": "test"}'

# If error: Check API key at https://mem0.ai
# If connection error: Check firewall/VPN
```

---

### Agent keeps making same mistakes

**Cause**: Learning not working properly

**Fix**:
1. Check Mem0 API connection
2. Verify API key works
3. Wait between tasks (memories need time to index)
4. Try `mem0_client.search_memories()` in Python console

---

## 🔍 Debugging Techniques

### Enable detailed logging

**In backend/.env**:
```
LOG_LEVEL=DEBUG
DEBUG=True
```

Restart backend - will show more details.

---

### Check backend API directly

```bash
# Health check
curl http://localhost:8000/health

# Config check
curl http://localhost:8000/config

# Send message (blocking)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "test", "user_id": "debug"}'
```

---

### Monitor browser network

1. Open DevTools (F12)
2. Go to Network tab
3. Send message
4. Watch requests/responses
5. Look for failed requests (red)

---

### Check file system

```bash
# Backend creates workspace here
ls -la /tmp/jarvis-workspace/

# Should see your created files
# If empty: Tool execution isn't working
# If full: Storage is working
```

---

## 🆘 Emergency Fixes

### Everything broken, start fresh

```bash
# Backend
cd backend
rm -rf venv
rm .env
python -m venv venv
source venv/bin/activate
pip install -r ../requirements.txt
cp .env.example .env
# Edit .env

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install

# Clean workspace
rm -rf /tmp/jarvis-workspace
```

---

### Browser completely broken

```bash
# Clear everything
# Mac/Chrome: Settings → Privacy → Clear browsing data → ALL TIME
# Windows: Ctrl+Shift+Delete → Clear all

# Or use incognito mode
Ctrl+Shift+N
```

---

### Virtual environment corrupted

```bash
cd backend

# Delete venv
rm -rf venv

# Recreate
python3 -m venv venv
source venv/bin/activate
pip install -r ../requirements.txt
```

---

## 📞 Getting Help

### Before asking for help, provide:

1. **Full error message** (copy-paste)
2. **What you were doing** (the prompt)
3. **System info**: `python --version`, `node --version`
4. **Terminal output** (screenshot)
5. **Browser console** (F12 → Console tab)

### Where to ask:

- GitHub Issues (if hosting on GitHub)
- Stack Overflow (tag: python, fastapi, react)
- Discord/Reddit communities

---

## ✅ Verification Checklist

After setup, verify everything:

```bash
# 1. Python works
python3 --version
# Should show 3.10+

# 2. Node works
node --version
npm --version
# Should show current versions

# 3. Backend starts
cd backend
source venv/bin/activate
python main.py
# Should show: Uvicorn running on http://0.0.0.0:8000
# Ctrl+C to stop

# 4. API responds
curl http://localhost:8000/health
# Should return: {"status":"healthy","version":"1.0.0"}

# 5. Frontend builds
cd frontend
npm install
npm run dev
# Should show: VITE v5.x.x ready in XXXms

# 6. Browser connects
# Open http://localhost:3000
# Should show Jarvis UI
```

---

## 🎯 Common Solutions Summary

| Problem | Solution |
|---------|----------|
| Module not found | `pip install -r requirements.txt` |
| API key error | Edit `.env` with actual keys |
| Port in use | `kill -9 <PID>` or change port |
| Backend won't start | Check logs, validate config |
| Frontend won't load | Clear cache, restart Vite |
| No WebSocket connection | Check backend running, check CORS |
| Slow responses | Check API status, reduce complexity |
| Memory not working | Test Mem0 API key, check connection |
| Files not created | Check `/tmp/jarvis-workspace` permissions |
| Everything broken | Start fresh (delete venv, node_modules) |

---

## 🚀 Still Stuck?

1. **Read the logs** - Full error is usually in terminal
2. **Check documentation** - README.md and ARCHITECTURE.md
3. **Try examples** - Use EXAMPLE_PROMPTS.md
4. **Search online** - Google the error message
5. **Ask community** - Discord/Reddit/Stack Overflow

---

**Most issues are solved by:**
1. Restarting both servers
2. Clearing cache
3. Checking API keys
4. Reading the error message

Good luck! 🚀
