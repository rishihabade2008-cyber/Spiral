import requests
import json
from typing import List, Dict, Any, Optional
from core.config import config
import logging

logger = logging.getLogger(__name__)


class Mem0Client:
    """Client for Mem0 API - handles memory operations."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = config.MEM0_API_BASE
        self.headers = {
            "Authorization": f"Token {api_key}",
            "Content-Type": "application/json",
        }
    
    def add_memory(
        self,
        messages: List[Dict[str, str]],
        user_id: str,
        agent_id: str = "jarvis",
        memory_type: str = "general"
    ) -> Dict[str, Any]:
        """Add memory to Mem0."""
        try:
            payload = {
                "messages": messages,
                "user_id": user_id,
                "agent_id": agent_id,
                "type": memory_type,
            }
            
            response = requests.post(
                f"{self.base_url}/memories/",
                json=payload,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to add memory: {e}")
            return {"error": str(e)}
    
    def search_memories(
        self,
        query: str,
        user_id: str,
        agent_id: str = "jarvis",
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Search for relevant memories using semantic search."""
        try:
            payload = {
                "query": query,
                "user_id": user_id,
                "agent_id": agent_id,
                "limit": limit,
            }
            
            response = requests.post(
                f"{self.base_url}/memories/search/",
                json=payload,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            return result.get("results", [])
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to search memories: {e}")
            return []
    
    def get_memories(
        self,
        user_id: str,
        agent_id: str = "jarvis",
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Retrieve all memories for a user."""
        try:
            params = {
                "user_id": user_id,
                "agent_id": agent_id,
                "limit": limit,
            }
            
            response = requests.get(
                f"{self.base_url}/memories/",
                params=params,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            return result.get("results", [])
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get memories: {e}")
            return []
    
    def update_memory(
        self,
        memory_id: str,
        messages: List[Dict[str, str]],
    ) -> Dict[str, Any]:
        """Update an existing memory."""
        try:
            payload = {
                "messages": messages,
            }
            
            response = requests.put(
                f"{self.base_url}/memories/{memory_id}/",
                json=payload,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to update memory: {e}")
            return {"error": str(e)}
    
    def delete_memory(self, memory_id: str) -> bool:
        """Delete a memory."""
        try:
            response = requests.delete(
                f"{self.base_url}/memories/{memory_id}/",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to delete memory: {e}")
            return False
    
    def format_memories_for_context(self, memories: List[Dict[str, Any]]) -> str:
        """Format retrieved memories into readable context string."""
        if not memories:
            return "No relevant memories found."
        
        formatted = []
        for mem in memories:
            content = mem.get("memory", mem.get("content", ""))
            if content:
                formatted.append(f"• {content}")
        
        return "\n".join(formatted) if formatted else "No relevant memories found."


# Global Mem0 client instance
mem0_client = Mem0Client(config.MEM0_API_KEY)
