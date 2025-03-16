from typing import Optional, Callable, Any
from datetime import datetime, time
import asyncio
from loguru import logger
import os

from .agent import BaseAgent
from .os_interaction import OSInteraction
from .screen_analyzer import ScreenAnalyzer


class VeldaOS:
    def __init__(self, openai_api_key: Optional[str] = None):
        self.os_interaction = OSInteraction()
        self.active_agents = {}
        self.scheduled_tasks = []
        self.screen_analyzer = ScreenAnalyzer(
            openai_api_key or os.getenv("OPENAI_API_KEY")
        )
    
    def open(self, app_name: str) -> 'AgentSession':
        """
        Open a new agent session for a specific application.
        
        Example:
            with veldaos.open("chrome") as agent:
                agent.loop("Find and click the login button")
        """
        logger.info(f"Opening new agent session for {app_name}")
        
        # Press Windows key to open Start menu
        self.os_interaction.press_key("win")
        
        # Wait 1 second
        self.os_interaction.wait(0.1)
        
        # Type cmd to search for Command Prompt
        self.os_interaction.type_text(app_name)

        # Press Enter to launch Command Prompt
        self.os_interaction.press_key("enter")
        self.os_interaction.wait(0.8)
        
        return AgentSession(app_name, self.os_interaction, self.screen_analyzer)
    
    def schedule(self, time: time) -> 'TaskScheduler':
        """
        Schedule tasks to run at specific times.
        
        Example:
            @veldaos.schedule(time(14, 30))  # Run at 2:30 PM
            def daily_task(agent):
                agent.loop("Check emails")
        """
        return TaskScheduler(time, self.os_interaction, self.screen_analyzer)
    
    async def run_forever(self):
        """Run the VeldaOS event loop forever."""
        while True:
            await self.check_scheduled_tasks()
            await asyncio.sleep(1)

class AgentSession:
    def __init__(self, app_name: str, os_interaction: OSInteraction, screen_analyzer: ScreenAnalyzer):
        self.app_name = app_name
        self.os_interaction = os_interaction
        self.screen_analyzer = screen_analyzer
        
    def __enter__(self):
        logger.info(f"Starting session for {self.app_name}")
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info(f"Closing session for {self.app_name}")
    
    def loop(self, prompt: str, max_attempts: int = 1, 
             success_condition: Optional[Callable] = None) -> bool:
        """
        Loop until the prompt is achieved or max attempts reached.
        
        Example:
            agent.loop("Click the login button", 
                      success_condition=lambda: is_logged_in())
        """
        attempts = 0
        while attempts < max_attempts:
            try:
                # Take screenshot
                screenshot = self.os_interaction.take_screenshot()
                
                # Process screenshot and determine action using OCR and LLM
                action = self.screen_analyzer.analyze_screenshot(screenshot, prompt)
                
                # Execute action
                success = self._execute_action(action)
                
                # Check if goal achieved
                if success and (success_condition is None or success_condition()):
                    logger.info(f"Successfully completed prompt: {prompt}")
                    return True
                
                attempts += 1
            except Exception as e:
                logger.error(f"Error in loop: {e}")
                attempts += 1
        
        logger.warning(f"Failed to complete prompt after {max_attempts} attempts")
        return False
    
    def _execute_action(self, action: dict) -> bool:
        """Execute the determined action."""
        try:
            if action["action"] == "click":
                return self.os_interaction.click(
                    action["parameters"]["x"],
                    action["parameters"]["y"]
                )
            elif action["action"] == "type":
                return self.os_interaction.type_text(
                    action["parameters"]["text"],
                    interval=0.1
                )
            elif action["action"] == "scroll":
                # Implement scroll action
                pass
            elif action["action"] == "wait":
                # Implement wait action
                pass
            return False
        except Exception as e:
            logger.error(f"Error executing action: {e}")
            return False

class TaskScheduler:
    def __init__(self, schedule_time: time, os_interaction: OSInteraction, screen_analyzer: ScreenAnalyzer):
        self.schedule_time = schedule_time
        self.os_interaction = os_interaction
        self.screen_analyzer = screen_analyzer
    
    def __call__(self, func: Callable):
        async def wrapper(*args, **kwargs):
            while True:
                now = datetime.now().time()
                if now.hour == self.schedule_time.hour and \
                   now.minute == self.schedule_time.minute:
                    with AgentSession("scheduled_task", self.os_interaction, self.screen_analyzer) as agent:
                        await func(agent)
                await asyncio.sleep(60)  # Check every minute
        return wrapper

# Create a global instance
veldaos = VeldaOS() 