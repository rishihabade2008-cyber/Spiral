"""LangGraph-based loop engine for Jarvis."""

import json
from typing import Any, Dict, Optional
from langgraph.graph import StateGraph, START, END
from anthropic import Anthropic
from core.state import JarvisState, create_initial_state
from core.prompts import (
    ANALYZER_PROMPT,
    PLANNER_PROMPT,
    REFLECTION_PROMPT,
    LEARNING_PROMPT,
    OBSERVATION_PROMPT,
)
from agents.mem0_client import mem0_client
from agents.tools import execute_tool
from core.config import config
import logging

logger = logging.getLogger(__name__)
client = Anthropic()


class LoopEngine:
    """Main loop engine orchestrating the Jarvis agent."""
    
    def __init__(self):
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph state machine."""
        graph = StateGraph(JarvisState)
        
        # Add nodes
        graph.add_node("analyzer", self.node_analyzer)
        graph.add_node("memory_retriever", self.node_memory_retriever)
        graph.add_node("planner", self.node_planner)
        graph.add_node("executor", self.node_executor)
        graph.add_node("observer", self.node_observer)
        graph.add_node("reflection", self.node_reflection)
        graph.add_node("learning", self.node_learning)
        
        # Define edges
        graph.add_edge(START, "analyzer")
        graph.add_edge("analyzer", "memory_retriever")
        graph.add_edge("memory_retriever", "planner")
        graph.add_edge("planner", "executor")
        graph.add_edge("executor", "observer")
        graph.add_edge("observer", "reflection")
        
        # Reflection routing
        graph.add_conditional_edges(
            "reflection",
            self._reflection_router,
            {
                "continue": "executor",
                "next_step": "executor",
                "finish": "learning",
                "failed": "learning",
            }
        )
        
        graph.add_edge("learning", END)
        
        return graph.compile()
    
    def _llm_call(self, prompt: str, json_mode: bool = True) -> str:
        """Call Claude API."""
        try:
            response = client.messages.create(
                model="claude-opus-4-6",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ],
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            return json.dumps({"error": str(e)})
    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """Safely parse JSON from LLM response."""
        try:
            # Try to extract JSON from response if it contains markdown
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]
            
            return json.loads(response.strip())
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse JSON: {response}")
            return {"error": "Failed to parse response", "raw": response}
    
    def node_analyzer(self, state: JarvisState) -> Dict[str, Any]:
        """Node 1: Analyze user intent and goal."""
        state["current_node"] = "analyzer"
        
        response = self._llm_call(
            ANALYZER_PROMPT + f"\n\nUser message: {state['user_message']}"
        )
        result = self._parse_json_response(response)
        
        state["intent"] = result.get("intent", "chat")
        state["goal"] = result.get("goal", state["user_message"])
        state["messages"].append({
            "node": "analyzer",
            "intent": state["intent"],
            "goal": state["goal"],
        })
        
        logger.info(f"Analyzed intent: {state['intent']}, goal: {state['goal']}")
        return state
    
    def node_memory_retriever(self, state: JarvisState) -> Dict[str, Any]:
        """Node 2: Retrieve relevant memories from Mem0."""
        state["current_node"] = "memory_retriever"
        
        # Search for relevant memories
        memories = mem0_client.search_memories(
            query=state["goal"],
            user_id=state["user_id"],
            limit=5,
        )
        
        state["relevant_memories"] = memories
        formatted_memories = mem0_client.format_memories_for_context(memories)
        
        state["messages"].append({
            "node": "memory_retriever",
            "memories_found": len(memories),
            "formatted": formatted_memories,
        })
        
        logger.info(f"Retrieved {len(memories)} relevant memories")
        return state
    
    def node_planner(self, state: JarvisState) -> Dict[str, Any]:
        """Node 3: Create step-by-step plan."""
        state["current_node"] = "planner"
        
        memories_context = mem0_client.format_memories_for_context(state["relevant_memories"])
        
        prompt = PLANNER_PROMPT.format(
            goal=state["goal"],
            memories=memories_context,
        )
        
        response = self._llm_call(prompt)
        result = self._parse_json_response(response)
        
        state["plan"] = result.get("steps", [])
        state["plan_summary"] = result.get("summary", "")
        
        state["messages"].append({
            "node": "planner",
            "steps_count": len(state["plan"]),
            "plan": state["plan"],
        })
        
        logger.info(f"Created plan with {len(state['plan'])} steps")
        return state
    
    def node_executor(self, state: JarvisState) -> Dict[str, Any]:
        """Node 4: Execute current step."""
        state["current_node"] = "executor"
        state["loop_iteration"] += 1
        
        if state["loop_iteration"] > config.MAX_LOOP_ITERATIONS:
            state["tool_error"] = "Max loop iterations reached"
            return state
        
        # Get current step
        if state["current_step"] >= len(state["plan"]):
            state["success"] = True
            return state
        
        current_step = state["plan"][state["current_step"]]
        state["current_action"] = current_step.get("task", "")
        state["tool_name"] = current_step.get("tool", "file_manager")
        
        # For this demo, convert task description to tool input
        state["tool_input"] = self._generate_tool_input(current_step, state)
        
        # Execute the tool
        try:
            state["tool_result"] = execute_tool(state["tool_name"], state["tool_input"])
            state["tool_error"] = None
        except Exception as e:
            state["tool_error"] = str(e)
            state["tool_result"] = None
        
        state["messages"].append({
            "node": "executor",
            "step": state["current_step"],
            "action": state["current_action"],
            "tool": state["tool_name"],
        })
        
        logger.info(f"Executed step {state['current_step']}: {state['current_action']}")
        return state
    
    def node_observer(self, state: JarvisState) -> Dict[str, Any]:
        """Node 5: Observe and record results."""
        state["current_node"] = "observer"
        
        observations = []
        if state["tool_result"]:
            if state["tool_result"].get("success"):
                observations.append("✓ Action completed successfully")
                if "message" in state["tool_result"]:
                    observations.append(f"  {state['tool_result']['message']}")
            else:
                observations.append("✗ Action failed")
                if "error" in state["tool_result"]:
                    observations.append(f"  Error: {state['tool_result']['error']}")
        
        if state["tool_error"]:
            observations.append(f"✗ Tool error: {state['tool_error']}")
        
        state["observations"] = observations
        state["success"] = (
            state["tool_result"] and state["tool_result"].get("success", False)
        )
        
        state["messages"].append({
            "node": "observer",
            "observations": observations,
            "success": state["success"],
        })
        
        logger.info(f"Observations: {observations}")
        return state
    
    def node_reflection(self, state: JarvisState) -> Dict[str, Any]:
        """Node 6: Reflect on results and decide next action."""
        state["current_node"] = "reflection"
        
        prompt = REFLECTION_PROMPT.format(
            current_step=state["current_step"],
            action=state["current_action"],
            result=str(state["tool_result"]),
            error=state["tool_error"] or "None",
        )
        
        response = self._llm_call(prompt)
        result = self._parse_json_response(response)
        
        state["reflection"] = result.get("analysis", "")
        state["success"] = result.get("success", False)
        state["error_type"] = result.get("error_type", "")
        state["can_retry"] = result.get("can_retry", False)
        
        # Determine next action
        next_action = result.get("next_action", "continue_to_next_step")
        
        if not state["success"] and state["can_retry"] and state["retry_count"] < state["max_retries"]:
            state["retry_count"] += 1
            next_action = "continue"  # Retry same step
        elif state["success"] or state["retry_count"] >= state["max_retries"]:
            state["current_step"] += 1
            state["retry_count"] = 0
            next_action = "next_step"
        
        state["messages"].append({
            "node": "reflection",
            "reflection": state["reflection"],
            "next_action": next_action,
            "success": state["success"],
        })
        
        logger.info(f"Reflection: {state['reflection']}, Next: {next_action}")
        return state
    
    def _reflection_router(self, state: JarvisState) -> str:
        """Route based on reflection results."""
        if state["current_step"] >= len(state["plan"]):
            return "finish"
        
        if state["success"]:
            return "next_step"
        
        if state["can_retry"] and state["retry_count"] < state["max_retries"]:
            return "continue"
        
        return "finish"
    
    def node_learning(self, state: JarvisState) -> Dict[str, Any]:
        """Node 7: Extract learnings and save to memory."""
        state["current_node"] = "learning"
        
        # Generate learning from the execution
        prompt = LEARNING_PROMPT.format(
            goal=state["goal"],
            plan=json.dumps(state["plan"], indent=2),
            outcome=state["final_answer"] or "Task attempted",
            feedback="",
        )
        
        response = self._llm_call(prompt)
        result = self._parse_json_response(response)
        
        # Save learnings to Mem0
        learnings = []
        for memory_type in ["user_memories", "project_memories", "strategy_memories"]:
            learnings.extend(result.get(memory_type, []))
        
        if learnings:
            mem0_client.add_memory(
                messages=[
                    {"role": "user", "content": state["user_message"]},
                    {"role": "assistant", "content": json.dumps(learnings)},
                ],
                user_id=state["user_id"],
                memory_type="learning",
            )
        
        state["learning"] = "; ".join(learnings[:3]) if learnings else "No new learnings"
        state["messages"].append({
            "node": "learning",
            "learnings": learnings,
            "saved_to_memory": len(learnings) > 0,
        })
        
        state["final_answer"] = f"Task completed. Learnings: {state['learning']}"
        
        logger.info(f"Saved {len(learnings)} learnings to memory")
        return state
    
    def _generate_tool_input(self, step: Dict[str, Any], state: JarvisState) -> Dict[str, Any]:
        """Generate tool input from step description."""
        # This is simplified - in production, you'd use LLM to parse step into tool calls
        tool = step.get("tool", "file_manager")
        task = step.get("task", "")
        
        if tool == "file_manager":
            return {
                "action": "create_folder",
                "path": "project",
            }
        elif tool == "python_executor":
            return {
                "action": "run_command",
                "command": "python --version",
            }
        
        return {"action": "list_files"}
    
    def run(self, user_message: str, user_id: str = "default") -> Dict[str, Any]:
        """Run the full loop engine."""
        state = create_initial_state(user_id, user_message)
        state["messages"] = []
        
        try:
            final_state = self.graph.invoke(state)
            return {
                "success": True,
                "final_answer": final_state.get("final_answer", ""),
                "learning": final_state.get("learning", ""),
                "messages": final_state.get("messages", []),
                "goal": final_state.get("goal", ""),
                "plan": final_state.get("plan", []),
            }
        except Exception as e:
            logger.error(f"Loop execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "final_answer": f"Error: {str(e)}",
            }


# Create global engine instance
loop_engine = LoopEngine()
