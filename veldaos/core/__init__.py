from typing import Optional, Callable, Any
from datetime import datetime, time
import asyncio
from loguru import logger

from .agent import BaseAgent
from .os_interaction import OSInteraction

class VeldaOS:
    def __init__(self):
        self.os_interaction = OSInteraction()
        self.active_agents = {}
        self.scheduled_tasks = []
    
    def open(self, app_name: str) -> 'AgentSession':
        """
        Open a new agent session for a specific application.
        
        Example:
            with veldaos.open("chrome") as agent:
                agent.loop("Find and click the login button")
        """
        logger.info(f"Opening new agent session for {app_name}")
        return AgentSession(app_name, self.os_interaction)
    
    def schedule(self, time: time) -> 'TaskScheduler':
        """
        Schedule tasks to run at specific times.
        
        Example:
            @veldaos.schedule(time(14, 30))  # Run at 2:30 PM
            def daily_task(agent):
                agent.loop("Check emails")
        """
        return TaskScheduler(time, self.os_interaction)
    
    async def run_forever(self):
        """Run the VeldaOS event loop forever."""
        while True:
            await self.check_scheduled_tasks()
            await asyncio.sleep(1)

class AgentSession:
    def __init__(self, app_name: str, os_interaction: OSInteraction):
        self.app_name = app_name
        self.os_interaction = os_interaction
        
    def __enter__(self):
        logger.info(f"Starting session for {self.app_name}")
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info(f"Closing session for {self.app_name}")
    
    def loop(self, prompt: str, max_attempts: int = 10, 
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
                
                # Process screenshot and determine action
                action = self._process_prompt(prompt, screenshot)
                
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
    
    def _process_prompt(self, prompt: str, screenshot: bytes) -> dict:
        """Process the prompt and screenshot to determine next action."""
        # Here you would implement the AI logic to determine the next action
        # This is a placeholder
        return {"type": "click", "x": 100, "y": 100}
    
    def _execute_action(self, action: dict) -> bool:
        """Execute the determined action."""
        if action["type"] == "click":
            return self.os_interaction.click(action["x"], action["y"])
        # Add more action types as needed
        return False

class TaskScheduler:
    def __init__(self, schedule_time: time, os_interaction: OSInteraction):
        self.schedule_time = schedule_time
        self.os_interaction = os_interaction
    
    def __call__(self, func: Callable):
        async def wrapper(*args, **kwargs):
            while True:
                now = datetime.now().time()
                if now.hour == self.schedule_time.hour and \
                   now.minute == self.schedule_time.minute:
                    with AgentSession("scheduled_task", self.os_interaction) as agent:
                        await func(agent)
                await asyncio.sleep(60)  # Check every minute
        return wrapper

# Create a global instance
veldaos = VeldaOS() 