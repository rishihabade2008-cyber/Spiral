"""Tool implementations for Jarvis agent."""

import os
import subprocess
import json
from typing import Dict, Any, Optional
from pathlib import Path
from core.config import config
import logging

logger = logging.getLogger(__name__)


class FileManager:
    """Handle file and folder operations."""
    
    def __init__(self):
        self.work_dir = config.WORK_DIR
        os.makedirs(self.work_dir, exist_ok=True)
    
    def create_folder(self, path: str) -> Dict[str, Any]:
        """Create a folder."""
        try:
            full_path = os.path.join(self.work_dir, path)
            os.makedirs(full_path, exist_ok=True)
            return {
                "success": True,
                "message": f"Folder created: {path}",
                "path": full_path,
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to create folder: {path}",
            }
    
    def write_file(self, path: str, content: str) -> Dict[str, Any]:
        """Write content to a file."""
        try:
            full_path = os.path.join(self.work_dir, path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, "w") as f:
                f.write(content)
            
            return {
                "success": True,
                "message": f"File written: {path}",
                "path": full_path,
                "size": len(content),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to write file: {path}",
            }
    
    def read_file(self, path: str) -> Dict[str, Any]:
        """Read a file."""
        try:
            full_path = os.path.join(self.work_dir, path)
            
            with open(full_path, "r") as f:
                content = f.read()
            
            return {
                "success": True,
                "content": content,
                "size": len(content),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to read file: {path}",
            }
    
    def list_files(self, path: str = ".") -> Dict[str, Any]:
        """List files in a directory."""
        try:
            full_path = os.path.join(self.work_dir, path)
            
            if not os.path.exists(full_path):
                return {
                    "success": False,
                    "error": "Path does not exist",
                }
            
            items = os.listdir(full_path)
            return {
                "success": True,
                "items": items,
                "count": len(items),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
    
    def delete_file(self, path: str) -> Dict[str, Any]:
        """Delete a file or folder."""
        try:
            full_path = os.path.join(self.work_dir, path)
            
            if os.path.isdir(full_path):
                import shutil
                shutil.rmtree(full_path)
            else:
                os.remove(full_path)
            
            return {
                "success": True,
                "message": f"Deleted: {path}",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }


class PythonExecutor:
    """Execute Python scripts safely."""
    
    def __init__(self):
        self.work_dir = config.WORK_DIR
        self.timeout = config.PYTHON_TIMEOUT
    
    def execute_script(self, script_path: str) -> Dict[str, Any]:
        """Execute a Python script from the work directory."""
        try:
            full_path = os.path.join(self.work_dir, script_path)
            
            if not os.path.exists(full_path):
                return {
                    "success": False,
                    "error": f"Script not found: {script_path}",
                }
            
            result = subprocess.run(
                ["python", full_path],
                cwd=self.work_dir,
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Script timeout (>{self.timeout}s)",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
    
    def execute_code(self, code: str, filename: str = "temp_script.py") -> Dict[str, Any]:
        """Execute Python code directly."""
        try:
            script_path = os.path.join(self.work_dir, filename)
            
            with open(script_path, "w") as f:
                f.write(code)
            
            result = subprocess.run(
                ["python", script_path],
                cwd=self.work_dir,
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Code timeout (>{self.timeout}s)",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
    
    def run_command(self, command: str) -> Dict[str, Any]:
        """Run a shell command in the work directory."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.work_dir,
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Command timeout (>{self.timeout}s)",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }


# Global tool instances
file_manager = FileManager()
python_executor = PythonExecutor()


def execute_tool(tool_name: str, tool_input: Dict[str, Any]) -> Dict[str, Any]:
    """Route tool execution based on tool name."""
    
    if tool_name == "file_manager":
        action = tool_input.get("action")
        
        if action == "create_folder":
            return file_manager.create_folder(tool_input.get("path", ""))
        elif action == "write_file":
            return file_manager.write_file(
                tool_input.get("path", ""),
                tool_input.get("content", ""),
            )
        elif action == "read_file":
            return file_manager.read_file(tool_input.get("path", ""))
        elif action == "list_files":
            return file_manager.list_files(tool_input.get("path", "."))
        elif action == "delete":
            return file_manager.delete_file(tool_input.get("path", ""))
    
    elif tool_name == "python_executor":
        action = tool_input.get("action")
        
        if action == "execute_script":
            return python_executor.execute_script(tool_input.get("script_path", ""))
        elif action == "execute_code":
            return python_executor.execute_code(
                tool_input.get("code", ""),
                tool_input.get("filename", "temp_script.py"),
            )
        elif action == "run_command":
            return python_executor.run_command(tool_input.get("command", ""))
    
    return {"success": False, "error": f"Unknown tool: {tool_name}"}
