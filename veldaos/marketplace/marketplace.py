from typing import List, Dict, Any, Optional
import json
import os
import shutil
from pathlib import Path
import requests
from pydantic import BaseModel
from loguru import logger

class AgentPackage(BaseModel):
    """Represents an agent package in the marketplace."""
    id: str
    name: str
    version: str
    description: str
    author: str
    price: float
    download_url: str
    capabilities: List[str]
    requirements: Dict[str, Any]
    rating: float
    downloads: int

class Marketplace:
    """Handles agent discovery, installation, and management."""
    
    def __init__(self, marketplace_url: str, local_agents_dir: str):
        self.marketplace_url = marketplace_url
        self.local_agents_dir = Path(local_agents_dir)
        self.local_agents_dir.mkdir(parents=True, exist_ok=True)
    
    def get_available_agents(self) -> List[AgentPackage]:
        """Fetch available agents from the marketplace."""
        try:
            response = requests.get(f"{self.marketplace_url}/agents")
            response.raise_for_status()
            return [AgentPackage(**agent) for agent in response.json()]
        except Exception as e:
            logger.error(f"Failed to fetch available agents: {e}")
            return []
    
    def get_agent_details(self, agent_id: str) -> Optional[AgentPackage]:
        """Get detailed information about a specific agent."""
        try:
            response = requests.get(f"{self.marketplace_url}/agents/{agent_id}")
            response.raise_for_status()
            return AgentPackage(**response.json())
        except Exception as e:
            logger.error(f"Failed to fetch agent details: {e}")
            return None
    
    def install_agent(self, agent_id: str) -> bool:
        """Install an agent from the marketplace."""
        try:
            agent = self.get_agent_details(agent_id)
            if not agent:
                return False
            
            # Download the agent package
            response = requests.get(agent.download_url, stream=True)
            response.raise_for_status()
            
            # Create agent directory
            agent_dir = self.local_agents_dir / agent_id
            agent_dir.mkdir(exist_ok=True)
            
            # Save the package
            package_path = agent_dir / f"{agent_id}-{agent.version}.zip"
            with open(package_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Extract the package
            shutil.unpack_archive(package_path, agent_dir)
            
            # Clean up the zip file
            package_path.unlink()
            
            logger.info(f"Successfully installed agent {agent.name}")
            return True
        except Exception as e:
            logger.error(f"Failed to install agent {agent_id}: {e}")
            return False
    
    def uninstall_agent(self, agent_id: str) -> bool:
        """Uninstall an agent."""
        try:
            agent_dir = self.local_agents_dir / agent_id
            if agent_dir.exists():
                shutil.rmtree(agent_dir)
                logger.info(f"Successfully uninstalled agent {agent_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to uninstall agent {agent_id}: {e}")
            return False
    
    def get_installed_agents(self) -> List[AgentPackage]:
        """Get list of installed agents."""
        installed_agents = []
        for agent_dir in self.local_agents_dir.iterdir():
            if agent_dir.is_dir():
                metadata_file = agent_dir / "metadata.json"
                if metadata_file.exists():
                    try:
                        with open(metadata_file) as f:
                            metadata = json.load(f)
                            installed_agents.append(AgentPackage(**metadata))
                    except Exception as e:
                        logger.error(f"Failed to read agent metadata: {e}")
        return installed_agents
    
    def update_agent(self, agent_id: str) -> bool:
        """Update an installed agent to the latest version."""
        try:
            # First uninstall the current version
            if not self.uninstall_agent(agent_id):
                return False
            
            # Install the latest version
            return self.install_agent(agent_id)
        except Exception as e:
            logger.error(f"Failed to update agent {agent_id}: {e}")
            return False 