import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # APIs
    MEM0_API_KEY = os.getenv("MEM0_API_KEY", "")
    MEM0_API_BASE = os.getenv("MEM0_API_BASE", "https://api.mem0.ai/v1")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Server
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Loop engine
    MAX_RETRIES = 3
    MAX_LOOP_ITERATIONS = 20
    
    # Tools
    WORK_DIR = "/tmp/jarvis-workspace"
    PYTHON_TIMEOUT = 30
    
    @classmethod
    def validate(cls):
        """Validate required config at startup."""
        if not cls.MEM0_API_KEY:
            raise ValueError("MEM0_API_KEY not set")
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY not set")

config = Config()
