from PyQt6.QtWidgets import (QWidget, QGridLayout, QLabel, QMenu, QPushButton, 
                           QVBoxLayout, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QCursor
import os
from .agent_details import AgentDetailsWindow

class AgentGridWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        layout.setSpacing(10)  # Add some spacing between cards
        
        # Sample agents data (in real app, this would come from your agents database)
        agents = [
            {"name": "Velda", "desc": "Manages emails and drafts responses automatically", "icon": "icon.png"},
            {"name": "File Organizer", "desc": "Sorts and categorizes files based on content and type", "icon": "icon.png"},
            {"name": "Code Helper", "desc": "Assists with code review and bug detection", "icon": "icon.png"},
            {"name": "Meeting Scheduler", "desc": "Coordinates and schedules meetings intelligently", "icon": "icon.png"},
            {"name": "Task Manager", "desc": "Prioritizes and tracks tasks intelligently", "icon": "icon.png"},
            {"name": "Document Writer", "desc": "Generates and edits documents professionally", "icon": "icon.png"},
            {"name": "Chat Bot", "desc": "Handles customer service inquiries 24/7", "icon": "icon.png"},
        ]

        # Create agent cards in a 3x4 grid
        row = 0
        col = 0
        for agent in agents:
            card = self.createAgentCard(agent)
            layout.addWidget(card, row, col)
            col += 1
            if col > 2:  # Move to next row after 3 items
                col = 0
                row += 1

        self.setLayout(layout)

    def createAgentCard(self, agent):
        card = QFrame()
        card.setFrameStyle(QFrame.Shape.NoFrame)  # Remove frame
        card.setStyleSheet("""
            QFrame {
                border: none;
                border-radius: 5px;
                padding: 0px;
                background: white;
                height: 50px;
                cursor: pointer;
            }
            QFrame:hover {
                background: #f5f5f5;
            }
        """)
        
        # Store agent data in the card
        card.agent_data = agent
        
        # Make the card clickable
        card.mousePressEvent = lambda event: self.showAgentDetails(card)
        
        layout = QVBoxLayout()
        layout.setSpacing(0)  # Remove spacing between elements
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        # Agent icon
        icon = QLabel()
        icon_path = os.path.join("veldaos", "desktop", "assets", "icons", agent["icon"])
        pixmap = QPixmap(icon_path).scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio)
        icon.setPixmap(pixmap)
        layout.addWidget(icon, alignment=Qt.AlignmentFlag.AlignCenter)

        # Agent name
        name = QLabel(agent["name"])
        name.setStyleSheet("""
            font-weight: bold; 
            font-size: 14px;
            padding: 0px;
            margin: 0px;
        """)
        layout.addWidget(name, alignment=Qt.AlignmentFlag.AlignCenter)

        # Agent description
        desc = QLabel(agent["desc"])
        desc.setWordWrap(True)
        desc.setStyleSheet("""
            color: #666; 
            font-size: 12px;
            padding: 0px;
            margin: 0px;
        """)
        layout.addWidget(desc, alignment=Qt.AlignmentFlag.AlignCenter)

        # Dropdown menu button
        menuBtn = QPushButton("•••")
        menuBtn.setStyleSheet("""
            QPushButton {
                border: none;
                padding: 0px;
                margin: 0px;
                height: 15px;
            }
            QPushButton:hover {
                background: #eee;
                border-radius: 3px;
            }
        """)
        menuBtn.clicked.connect(lambda: self.showMenu(menuBtn))
        layout.addWidget(menuBtn, alignment=Qt.AlignmentFlag.AlignRight)

        card.setLayout(layout)
        return card

    def showAgentDetails(self, card):
        dialog = AgentDetailsWindow(card.agent_data, self)
        dialog.exec()

    def showMenu(self, button):
        menu = QMenu(self)
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