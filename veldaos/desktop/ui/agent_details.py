from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QLineEdit, QTextEdit, QComboBox, QSpinBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import os

class AgentDetailsWindow(QDialog):
    def __init__(self, agent_data, parent=None):
        super().__init__(parent)
        self.agent_data = agent_data
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"Agent Details - {self.agent_data['name']}")
        self.setMinimumSize(500, 600)
        
        layout = QVBoxLayout()
        
        # Header with icon and name
        header = QHBoxLayout()
        icon = QLabel()
        icon_path = os.path.join("veldaos", "desktop", "assets", "icons", self.agent_data["icon"])
        pixmap = QPixmap(icon_path).scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio)
        icon.setPixmap(pixmap)
        header.addWidget(icon)
        
        name_layout = QVBoxLayout()
        name_label = QLabel("Name:")
        name_label.setStyleSheet("font-weight: bold;")
        name_input = QLineEdit(self.agent_data["name"])
        name_layout.addWidget(name_label)
        name_layout.addWidget(name_input)
        header.addLayout(name_layout)
        layout.addLayout(header)
        
        # Description
        desc_label = QLabel("Description:")
        desc_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(desc_label)
        desc_input = QTextEdit(self.agent_data["desc"])
        layout.addWidget(desc_input)
        
        # Model Settings
        settings_label = QLabel("Model Settings")
        settings_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 10px;")
        layout.addWidget(settings_label)
        
        # Model selection
        model_layout = QHBoxLayout()
        model_label = QLabel("Model:")
        model_combo = QComboBox()
        model_combo.addItems(["GPT-4", "GPT-3.5", "Claude-3", "Gemini-Pro"])
        model_layout.addWidget(model_label)
        model_layout.addWidget(model_combo)
        layout.addLayout(model_layout)
        
        # Temperature
        temp_layout = QHBoxLayout()
        temp_label = QLabel("Temperature:")
        temp_spin = QSpinBox()
        temp_spin.setRange(0, 100)
        temp_spin.setValue(70)
        temp_spin.setSingleStep(1)
        temp_layout.addWidget(temp_label)
        temp_layout.addWidget(temp_spin)
        layout.addLayout(temp_layout)
        
        # System prompt
        sys_prompt_label = QLabel("System Prompt:")
        sys_prompt_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(sys_prompt_label)
        sys_prompt_input = QTextEdit()
        sys_prompt_input.setPlaceholderText("Enter the system prompt for this agent...")
        layout.addWidget(sys_prompt_input)
        
        # Schedule settings
        schedule_label = QLabel("Schedule Settings")
        schedule_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 10px;")
        layout.addWidget(schedule_label)
        
        schedule_combo = QComboBox()
        schedule_combo.addItems(["Run on demand", "Run hourly", "Run daily", "Run weekly"])
        layout.addWidget(schedule_combo)
        
        # Action buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save Changes")
        save_btn.clicked.connect(self.save_changes)
        run_btn = QPushButton("Run Agent")
        run_btn.clicked.connect(self.run_agent)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(run_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def save_changes(self):
        # Implement save functionality
        self.accept()
    
    def run_agent(self):
        # Implement run functionality
        pass 