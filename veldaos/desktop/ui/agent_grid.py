from PyQt6.QtWidgets import (QWidget, QGridLayout, QLabel, QMenu, QPushButton, 
                           QVBoxLayout, QFrame, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QCursor
import os
from .agent_details import AgentDetailsWindow

class AgentGridWidget(QWidget):
    def __init__(self):
        super().__init__()
        # Define card dimensions
        self.CARD_WIDTH = 200  # pixels
        self.CARD_HEIGHT = 100  # pixels
        self.ICON_SIZE = 32  # pixels
        self.CARD_SPACING = 10  # pixels
        self.MAX_CARDS_PER_ROW = 5
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        # Set fixed spacing between cards
        layout.setSpacing(self.CARD_SPACING)
        # Prevent the grid from expanding beyond card sizes
        layout.setSizeConstraint(QGridLayout.SizeConstraint.SetMinAndMaxSize)
        # Align grid to top-left
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        # Sample agents from database
        self.agents = [
            {"name": "Velda", "desc": "Manages emails and drafts responses automatically", "icon": "icon.png"},
            {"name": "File Organizer", "desc": "Sorts and categorizes files based on content and type", "icon": "icon.png"},
            {"name": "Code Helper", "desc": "Assists with code review and bug detection", "icon": "icon.png"},
            {"name": "Meeting Scheduler", "desc": "Coordinates and schedules meetings intelligently", "icon": "icon.png"},
            {"name": "Task Manager", "desc": "Prioritizes and tracks tasks intelligently", "icon": "icon.png"},
            {"name": "Document Writer", "desc": "Generates and edits documents professionally", "icon": "icon.png"},
            {"name": "Chat Bot", "desc": "Handles customer service inquiries 24/7", "icon": "icon.png"},
            {"name": "Code Helper", "desc": "Assists with code review and bug detection", "icon": "icon.png"},
            {"name": "Meeting Scheduler", "desc": "Coordinates and schedules meetings intelligently", "icon": "icon.png"},
            {"name": "Task Manager", "desc": "Prioritizes and tracks tasks intelligently", "icon": "icon.png"},
            {"name": "Document Writer", "desc": "Generates and edits documents professionally", "icon": "icon.png"},
            {"name": "Chat Bot", "desc": "Handles customer service inquiries 24/7", "icon": "icon.png"},
            {"name": "Velda", "desc": "Manages emails and drafts responses automatically", "icon": "icon.png"},
            {"name": "File Organizer", "desc": "Sorts and categorizes files based on content and type", "icon": "icon.png"},
            {"name": "Code Helper", "desc": "Assists with code review and bug detection", "icon": "icon.png"},
            {"name": "Meeting Scheduler", "desc": "Coordinates and schedules meetings intelligently", "icon": "icon.png"},
            {"name": "Task Manager", "desc": "Prioritizes and tracks tasks intelligently", "icon": "icon.png"}
        ]

        # Create agent cards in a 3x4 grid
        self.update_grid_layout(layout)
        self.setLayout(layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Update grid layout when widget is resized
        self.update_grid_layout()

    def update_grid_layout(self, layout=None):
        if layout is None:
            layout = self.layout()
            if layout is None:
                return

        # Clear existing widgets
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Calculate number of cards that can fit in the current width
        available_width = self.width()
        min_cards = 1  # Minimum cards per row
        max_cards = self.MAX_CARDS_PER_ROW  # Maximum cards per row
        
        # Calculate how many cards can fit
        card_width_with_spacing = self.CARD_WIDTH + self.CARD_SPACING
        cards_that_fit = max(min_cards, min(max_cards, available_width // card_width_with_spacing))
        
        # Create agent cards grid
        row = 0
        col = 0
        for agent in self.agents:
            card = self.createAgentCard(agent)
            layout.addWidget(card, row, col)
            col += 1
            if col >= cards_that_fit:  # Move to next row
                col = 0
                row += 1

        # Set size policy to allow horizontal expansion
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def createAgentCard(self, agent):
        card = QFrame()
        card.setFrameStyle(QFrame.Shape.NoFrame)  # Remove frame
        card.setFixedSize(self.CARD_WIDTH, self.CARD_HEIGHT)  # Set fixed size
        card.setStyleSheet(f"""
            QFrame {{
                border: none;
                border-radius: 85x;
                padding: 0px;
                background: #2c3e50;
                width: {self.CARD_WIDTH}px;
                height: {self.CARD_HEIGHT}px;
            }}
            QFrame:hover {{
                background: #34495e;
            }}
        """)
        
        # Store agent data in the card
        card.agent_data = agent
        
        # Make the card clickable and set cursor
        card.mousePressEvent = lambda event: self.showAgentDetails(card)
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        
        layout = QVBoxLayout()
        layout.setSpacing(0)  # Small spacing between elements
        layout.setContentsMargins(3, 3, 3, 3)  # Add some padding inside cards

        # Agent icon
        icon = QLabel()
        icon_path = os.path.join("veldaos", "desktop", "assets", "icons", agent["icon"])
        pixmap = QPixmap(icon_path).scaled(self.ICON_SIZE, self.ICON_SIZE, Qt.AspectRatioMode.KeepAspectRatio)
        icon.setPixmap(pixmap)
        layout.addWidget(icon, alignment=Qt.AlignmentFlag.AlignCenter)

        # Agent name
        name = QLabel(agent["name"])
        name.setStyleSheet("""
            font-weight: bold; 
            font-size: 16px;
            padding: 0px 0px;
            margin: 0px;
            color: #ecf0f1;
        """)
        name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(name)

        # Agent description
        desc = QLabel(agent["desc"])
        desc.setWordWrap(True)
        desc.setStyleSheet("""
            color: #bdc3c7; 
            font-size: 12px;
            padding: 0px;
            margin: 0px;
        """)
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc)

        # Add spacer to push menu button to bottom
        layout.addStretch()

        # Dropdown menu button
        menuBtn = QPushButton("•••")
        menuBtn.setStyleSheet("""
            QPushButton {
                border: none;
                padding: 0px;
                margin: 0px;
                height: 10px;
                color: #bdc3c7;
            }
            QPushButton:hover {
                background: #2980b9;
                border-radius: 3px;
                color: white;
            }
        """)
        menuBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        menuBtn.clicked.connect(lambda: self.showMenu(menuBtn))
        layout.addWidget(menuBtn, alignment=Qt.AlignmentFlag.AlignRight)

        card.setLayout(layout)
        return card

    def update_agents(self, agents):
        """Update the grid with new agent data."""
        self.agents = agents
        self.update_grid_layout()

    def showAgentDetails(self, card):
        dialog = AgentDetailsWindow(card.agent_data, self)
        dialog.exec()

    def showMenu(self, button):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #2c3e50;
                border: 1px solid #34495e;
                border-radius: 4px;
                padding: 5px;
            }
            QMenu::item {
                padding: 5px 15px;
                color: #ecf0f1;
            }
            QMenu::item:selected {
                background: #2980b9;
                border-radius: 3px;
            }
        """)
        menu.addAction("Run", lambda: self.runAgent())
        menu.addAction("Uninstall", lambda: self.uninstallAgent())
        menu.addAction("Schedule", lambda: self.scheduleAgent())
        menu.exec(button.mapToGlobal(button.rect().bottomLeft()))

    def runAgent(self):
        # Implement run functionality
        pass

    def uninstallAgent(self):
        # Implement uninstall functionality
        pass

    def scheduleAgent(self):
        # Implement schedule functionality
        pass 