from typing import Optional, Callable
from loguru import logger
from ..screen_analyzer import ScreenAnalyzer
from ..os_interaction import OSInteraction

class PythonVersionAgent:
    """Agent that checks Python version using CMD."""
    
    def __init__(self, os_interaction: OSInteraction, screen_analyzer: ScreenAnalyzer):
        self.os_interaction = os_interaction
        self.screen_analyzer = screen_analyzer
    
    def check_python_version(self) -> bool:
        """Check Python version using CMD."""
        try:
            # Open CMD
            self.os_interaction.open("cmd")

            
            # Type python --version and let the LLM analyze the output
            success = self.screen_analyzer.loop(
                "Type 'python --version' and tell me what version of Python is installed",
                max_attempts=3,
                success_condition=lambda: True  # We trust the LLM's analysis
            )
            
            if not success:
                logger.error("Failed to detect Python version")
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Error checking Python version: {e}")
            return False

# Example usage:
"""
from veldaos.core import veldaos

with veldaos.open("cmd") as agent:
    python_agent = PythonVersionAgent(agent.os_interaction, agent.screen_analyzer)
    python_agent.check_python_version()
""" 