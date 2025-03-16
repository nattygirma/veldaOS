from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel
from loguru import logger

class AgentMetadata(BaseModel):
    """Metadata for an AI agent."""
    name: str
    version: str
    description: str
    author: str
    price: float
    capabilities: list[str]
    requirements: Dict[str, Any]

class AgentAction(BaseModel):
    """Represents an action that an agent can take."""
    action_type: str  # click, type, screenshot, etc.
    parameters: Dict[str, Any]
    confidence: float

class BaseAgent(ABC):
    """Base class for all AI agents in the VeldaOS system."""
    
    def __init__(self):
        self.metadata: Optional[AgentMetadata] = None
        self.is_running: bool = False
        self.current_task: Optional[str] = None
        
    @abstractmethod
    def initialize(self) -> None:
        """Initialize the agent with necessary resources."""
        pass
    
    @abstractmethod
    def process_screenshot(self, screenshot: bytes) -> AgentAction:
        """Process a screenshot and determine the next action."""
        pass
    
    @abstractmethod
    def handle_action_result(self, action: AgentAction, success: bool) -> None:
        """Handle the result of an executed action."""
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Clean up resources when the agent is stopped."""
        pass
    
    def start(self) -> None:
        """Start the agent."""
        if self.is_running:
            logger.warning("Agent is already running")
            return
        
        self.is_running = True
        logger.info(f"Agent {self.metadata.name} started")
    
    def stop(self) -> None:
        """Stop the agent."""
        if not self.is_running:
            logger.warning("Agent is not running")
            return
        
        self.is_running = False
        self.cleanup()
        logger.info(f"Agent {self.metadata.name} stopped")
    
    def set_task(self, task: str) -> None:
        """Set the current task for the agent."""
        self.current_task = task
        logger.info(f"Agent {self.metadata.name} received new task: {task}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the agent."""
        return {
            "name": self.metadata.name,
            "is_running": self.is_running,
            "current_task": self.current_task,
            "version": self.metadata.version
        } 