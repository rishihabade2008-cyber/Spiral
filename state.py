from typing import TypedDict, List, Dict, Any, Optional

class JarvisState(TypedDict, total=False):
    """Central state object for the Jarvis loop engine."""
    
    # User & Session
    user_id: str
    session_id: str
    
    # Input
    user_message: str
    intent: str
    
    # Memory
    relevant_memories: List[Dict[str, Any]]
    
    # Planning
    goal: str
    plan: List[Dict[str, Any]]
    plan_summary: str
    
    # Execution
    current_step: int
    current_action: str
    
    # Tool execution
    tool_name: str
    tool_input: Dict[str, Any]
    tool_result: Any
    tool_error: Optional[str]
    
    # Observation
    observations: List[str]
    
    # Reflection
    reflection: str
    success: bool
    error_type: str
    can_retry: bool
    
    # Retry logic
    retry_count: int
    max_retries: int
    
    # Learning
    learning: str
    
    # Output
    final_answer: str
    
    # Metadata
    messages: List[Dict[str, str]]
    loop_history: List[Dict[str, Any]]
    current_node: str
    loop_iteration: int


def create_initial_state(user_id: str, user_message: str) -> JarvisState:
    """Create a fresh state for a new task."""
    return {
        "user_id": user_id,
        "session_id": f"session_{int(__import__('time').time())}",
        "user_message": user_message,
        "intent": "",
        "relevant_memories": [],
        "goal": "",
        "plan": [],
        "plan_summary": "",
        "current_step": 0,
        "current_action": "",
        "tool_name": "",
        "tool_input": {},
        "tool_result": None,
        "tool_error": None,
        "observations": [],
        "reflection": "",
        "success": False,
        "error_type": "",
        "can_retry": True,
        "retry_count": 0,
        "max_retries": 3,
        "learning": "",
        "final_answer": "",
        "messages": [],
        "loop_history": [],
        "current_node": "start",
        "loop_iteration": 0,
    }
