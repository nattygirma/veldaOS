from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QListWidget,
    QLabel,
    QStackedWidget,
    QMessageBox,
    QProgressBar,
    QLineEdit,
    QFrame,
    QScrollArea,
    QSizePolicy
)
from PyQt6.QtCore import (
    Qt,
    QThread,
    pyqtSignal,
    QSize,
    QTimer
)
from PyQt6.QtGui import (
    QIcon,
    QFont,
    QColor,
    QPalette
)
import qtawesome as qta
from typing import Optional, Dict, Any
from loguru import logger

from veldaos.marketplace.marketplace import Marketplace, AgentPackage
from veldaos.core.agent import BaseAgent

class AgentRunner(QThread):
    """Thread for running agents to prevent UI freezing."""
    finished = pyqtSignal(bool)
    
    def __init__(self, agent: BaseAgent, task: str):
        super().__init__()
        self.agent = agent
        self.task = task
    
    def run(self):
        try:
            self.agent.initialize()
            self.agent.start()
            self.agent.set_task(self.task)
            # Here you would implement the main agent loop
            self.finished.emit(True)
        except Exception as e:
            logger.error(f"Agent execution failed: {e}")
            self.finished.emit(False)

class MainWindow(QMainWindow):
    """Main window of the VeldaOS desktop application."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VeldaOS - AI Agent Marketplace")
        self.setMinimumSize(800, 600)
        
        # Initialize marketplace
        self.marketplace = Marketplace(
            marketplace_url="https://api.veldaos.com/marketplace",
            local_agents_dir="./agents"
        )
        
        self.setup_ui()
        self.load_agents()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Create sidebar
        sidebar = QWidget()
        sidebar.setMaximumWidth(200)
        sidebar_layout = QVBoxLayout(sidebar)
        
        # Add sidebar buttons
        marketplace_btn = QPushButton("Marketplace")
        marketplace_btn.setIcon(qta.icon('fa5s.store'))
        marketplace_btn.clicked.connect(self.show_marketplace)
        
        installed_btn = QPushButton("Installed Agents")
        installed_btn.setIcon(qta.icon('fa5s.robot'))
        installed_btn.clicked.connect(self.show_installed)
        
        settings_btn = QPushButton("Settings")
        settings_btn.setIcon(qta.icon('fa5s.cog'))
        settings_btn.clicked.connect(self.show_settings)
        
        sidebar_layout.addWidget(marketplace_btn)
        sidebar_layout.addWidget(installed_btn)
        sidebar_layout.addWidget(settings_btn)
        sidebar_layout.addStretch()
        
        # Create main content area
        self.content = QStackedWidget()
        
        # Add pages
        self.marketplace_page = self.create_marketplace_page()
        self.installed_page = self.create_installed_page()
        self.settings_page = self.create_settings_page()
        
        self.content.addWidget(self.marketplace_page)
        self.content.addWidget(self.installed_page)
        self.content.addWidget(self.settings_page)
        
        # Add widgets to main layout
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.content)
    
    def create_marketplace_page(self) -> QWidget:
        """Create the marketplace page."""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Add search bar
        search_layout = QHBoxLayout()
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search agents...")
        search_layout.addWidget(search_input)
        layout.addLayout(search_layout)
        
        # Add agent list
        self.marketplace_list = QListWidget()
        layout.addWidget(self.marketplace_list)
        
        return page
    
    def create_installed_page(self) -> QWidget:
        """Create the installed agents page."""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Add agent list
        self.installed_list = QListWidget()
        layout.addWidget(self.installed_list)
        
        # Add control buttons
        control_layout = QHBoxLayout()
        start_btn = QPushButton("Start Agent")
        stop_btn = QPushButton("Stop Agent")
        uninstall_btn = QPushButton("Uninstall")
        
        start_btn.clicked.connect(self.start_agent)
        stop_btn.clicked.connect(self.stop_agent)
        uninstall_btn.clicked.connect(self.uninstall_agent)
        
        control_layout.addWidget(start_btn)
        control_layout.addWidget(stop_btn)
        control_layout.addWidget(uninstall_btn)
        layout.addLayout(control_layout)
        
        return page
    
    def create_settings_page(self) -> QWidget:
        """Create the settings page."""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Add settings options
        layout.addWidget(QLabel("Settings"))
        # Add more settings widgets here
        
        return page
    
    def load_agents(self):
        """Load available and installed agents."""
        # Load marketplace agents
        available_agents = self.marketplace.get_available_agents()
        self.marketplace_list.clear()
        for agent in available_agents:
            self.marketplace_list.addItem(f"{agent.name} - {agent.description}")
        
        # Load installed agents
        installed_agents = self.marketplace.get_installed_agents()
        self.installed_list.clear()
        for agent in installed_agents:
            self.installed_list.addItem(f"{agent.name} v{agent.version}")
    
    def show_marketplace(self):
        """Show the marketplace page."""
        self.content.setCurrentWidget(self.marketplace_page)
    
    def show_installed(self):
        """Show the installed agents page."""
        self.content.setCurrentWidget(self.installed_page)
    
    def show_settings(self):
        """Show the settings page."""
        self.content.setCurrentWidget(self.settings_page)
    
    def start_agent(self):
        """Start the selected agent."""
        current_item = self.installed_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Error", "Please select an agent to start")
            return
        
        # Here you would implement agent starting logic
        QMessageBox.information(self, "Success", "Agent started successfully")
    
    def stop_agent(self):
        """Stop the selected agent."""
        current_item = self.installed_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Error", "Please select an agent to stop")
            return
        
        # Here you would implement agent stopping logic
        QMessageBox.information(self, "Success", "Agent stopped successfully")
    
    def uninstall_agent(self):
        """Uninstall the selected agent."""
        current_item = self.installed_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Error", "Please select an agent to uninstall")
            return
        
        reply = QMessageBox.question(
            self,
            "Confirm Uninstall",
            "Are you sure you want to uninstall this agent?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Here you would implement agent uninstallation logic
            self.load_agents()
            QMessageBox.information(self, "Success", "Agent uninstalled successfully") 