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
    QSizePolicy,
    QTabWidget
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
from veldaos.desktop.ui.agent_grid import AgentGridWidget

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
        
        # Set dark theme
        self.setStyleSheet("""
            QMainWindow {
                background: #1a1a1a;
            }
            QWidget {
                background: #1a1a1a;
                color: #ecf0f1;
            }
            QPushButton {
                background: #2c3e50;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                color: #ecf0f1;
            }
            QPushButton:hover {
                background: #34495e;
            }
            QLineEdit {
                background: #2c3e50;
                border: none;
                padding: 8px;
                border-radius: 4px;
                color: #ecf0f1;
            }
            QLineEdit:focus {
                background: #34495e;
            }
        """)
        
        # Initialize marketplace
        self.marketplace = Marketplace(
            marketplace_url="https://velda.pro",
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
        search_input.setStyleSheet("""
            QLineEdit {
                background: #2c3e50;
                border: none;
                padding: 8px;
                border-radius: 4px;
                color: #ecf0f1;
            }
            QLineEdit:focus {
                background: #34495e;
            }
            QLineEdit::placeholder {
                color: #7f8c8d;
            }
        """)
        search_layout.addWidget(search_input)
        layout.addLayout(search_layout)
        
        # Create tab widget
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: #1a1a1a;
            }
            QTabWidget::tab-bar {
                alignment: left;
            }
            QTabBar::tab {
                background: #2c3e50;
                padding: 8px 16px;
                margin-right: 2px;
                border: none;
                border-radius: 4px 4px 0 0;
                color: #bdc3c7;
            }
            QTabBar::tab:selected {
                background: #34495e;
                color: #ecf0f1;
                font-weight: bold;
            }
            QTabBar::tab:hover:!selected {
                background: #34495e;
            }
        """)
        
        # Create scroll areas for each tab
        installed_scroll = QScrollArea()
        installed_scroll.setWidgetResizable(True)
        installed_scroll.setStyleSheet("""
            QScrollArea { 
                border: none;
                background: #1a1a1a;
            }
            QScrollBar:vertical {
                border: none;
                background: #2c3e50;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #34495e;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #3498db;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        uninstalled_scroll = QScrollArea()
        uninstalled_scroll.setWidgetResizable(True)
        uninstalled_scroll.setStyleSheet(installed_scroll.styleSheet())
        
        # Add agent grids to scroll areas
        self.installed_grid = AgentGridWidget()
        installed_scroll.setWidget(self.installed_grid)
        
        self.uninstalled_grid = AgentGridWidget()
        uninstalled_scroll.setWidget(self.uninstalled_grid)
        
        # Add tabs
        tab_widget.addTab(installed_scroll, "Installed")
        tab_widget.addTab(uninstalled_scroll, "Available")
        
        layout.addWidget(tab_widget)
        
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
        try:
            # Load available agents
            available_agents = []  # self.marketplace.get_available_agents()
            available_agent_data = [
                {"name": agent.name, "desc": agent.description, "icon": "icon.png"}
                for agent in available_agents
            ]
            
            # Load installed agents
            installed_agents = []  # self.marketplace.get_installed_agents()
            installed_agent_data = [
                {"name": agent.name, "desc": f"v{agent.version}", "icon": "icon.png"}
                for agent in installed_agents
            ]
            
            # Update the grids with actual data
            # For now, they will use the sample data defined in AgentGridWidget
            # self.installed_grid.update_agents(installed_agent_data)
            # self.uninstalled_grid.update_agents(available_agent_data)
            
        except Exception as e:
            logger.error(f"Failed to load agents: {e}")
            QMessageBox.warning(self, "Error", f"Failed to load agents: {e}")
    
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