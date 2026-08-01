"""FastAPI application for Jarvis self-learning agent."""

import asyncio
import json
import logging
from typing import Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from core.config import config, Config
from loop_engine.graph import loop_engine

# Configure logging
logging.basicConfig(
    level=config.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Validate config
try:
    config.validate()
except ValueError as e:
    logger.error(f"Configuration error: {e}")
    raise

# Create FastAPI app
app = FastAPI(title="Jarvis Self-Learning Agent", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class MessageRequest(BaseModel):
    """User message request."""
    message: str
    user_id: str = "default"


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str


class ResponseMessage(BaseModel):
    """Response message structure."""
    type: str  # "status", "thinking", "tool_use", "result", "error"
    content: Dict[str, Any]


# Routes
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0",
    }


@app.post("/chat")
async def chat(request: MessageRequest) -> JSONResponse:
    """Send a message to Jarvis (simple blocking endpoint)."""
    try:
        logger.info(f"Received message from {request.user_id}: {request.message}")
        
        result = loop_engine.run(request.message, request.user_id)
        
        return JSONResponse({
            "success": result.get("success", False),
            "final_answer": result.get("final_answer", ""),
            "learning": result.get("learning", ""),
            "goal": result.get("goal", ""),
            "plan": result.get("plan", []),
            "messages": result.get("messages", []),
        })
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)},
        )


@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket endpoint for real-time streaming responses."""
    await websocket.accept()
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            message_data = json.loads(data)
            user_message = message_data.get("message", "")
            user_id = message_data.get("user_id", "default")
            
            if not user_message:
                await websocket.send_json({
                    "type": "error",
                    "content": {"error": "Empty message"},
                })
                continue
            
            logger.info(f"WebSocket message from {user_id}: {user_message}")
            
            # Send "thinking" status
            await websocket.send_json({
                "type": "status",
                "content": {
                    "current_node": "starting",
                    "message": "Analyzing your request...",
                },
            })
            
            # Run the loop engine in a thread to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                loop_engine.run,
                user_message,
                user_id,
            )
            
            # Send intermediate messages as they come from the loop
            if "messages" in result:
                for msg in result.get("messages", []):
                    await websocket.send_json({
                        "type": "thinking",
                        "content": msg,
                    })
                    await asyncio.sleep(0.1)  # Small delay for visual effect
            
            # Send final result
            await websocket.send_json({
                "type": "result",
                "content": {
                    "final_answer": result.get("final_answer", ""),
                    "learning": result.get("learning", ""),
                    "goal": result.get("goal", ""),
                    "plan": result.get("plan", []),
                    "success": result.get("success", False),
                },
            })
    
    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        try:
            await websocket.send_json({
                "type": "error",
                "content": {"error": str(e)},
            })
        except:
            pass


@app.get("/config")
async def get_config():
    """Get configuration info (public only)."""
    return {
        "max_retries": config.MAX_RETRIES,
        "max_loop_iterations": config.MAX_LOOP_ITERATIONS,
        "python_timeout": config.PYTHON_TIMEOUT,
    }


# Startup/shutdown events
@app.on_event("startup")
async def startup():
    """Initialize on startup."""
    logger.info("Jarvis agent starting up...")
    logger.info(f"Work directory: {config.WORK_DIR}")
    logger.info(f"Max retries: {config.MAX_RETRIES}")
    logger.info(f"Max loop iterations: {config.MAX_LOOP_ITERATIONS}")


@app.on_event("shutdown")
async def shutdown():
    """Cleanup on shutdown."""
    logger.info("Jarvis agent shutting down...")


# Run with: uvicorn main:app --reload --host 0.0.0.0 --port 8000
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host=config.HOST,
        port=config.PORT,
        log_level=config.LOG_LEVEL.lower(),
    )
