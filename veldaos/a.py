import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLineEdit, 
                            QPushButton, QLabel)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

class ModernLoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VeldaOS Login")
        self.setFixedSize(400, 500)
        self.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                color: #ecf0f1;
                font-family: 'Segoe UI', Arial;
            }
            QLineEdit {
                padding: 12px;
                border: 2px solid #34495e;
                border-radius: 6px;
                background-color: #34495e;
                color: white;
                font-size: 14px;
                margin: 8px 0px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
            QPushButton {
                padding: 12px;
                background-color: #3498db;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                margin: 8px 0px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLabel {
                font-size: 14px;
                margin: 4px 0px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)

        # Title
        title = QLabel("Welcome to VeldaOS")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px 0px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Username
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        
        # Password
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        
        # Login button
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.handle_login)
        
        # Register link
        register_link = QLabel("Don't have an account? <a href='#' style='color: #3498db;'>Register</a>")
        register_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        register_link.setOpenExternalLinks(False)
        register_link.linkActivated.connect(self.handle_register)

        # Add widgets to layout
        layout.addWidget(title)
        layout.addStretch(1)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(login_btn)
        layout.addWidget(register_link)
        layout.addStretch(1)
        
        self.setLayout(layout)

    def handle_login(self):
        username = self.username.text()
        password = self.password.text()
        print(f"Login attempt - Username: {username}, Password: {password}")
        # Add your authentication logic here

    def handle_register(self):
        print("Opening registration window")
        # Add your registration logic here

def main():
    # Create the application
    app = QApplication(sys.argv)
    
    # Optional: Set application-wide stylesheet
    app.setStyle("Fusion")  # Use Fusion style for a modern look
    
    # Create and show the login window
    login_window = ModernLoginWindow()
    
    # Center the window on the screen
    screen = app.primaryScreen().geometry()
    x = (screen.width() - login_window.width()) // 2
    y = (screen.height() - login_window.height()) // 2
    login_window.move(x, y)
    
    # Show the window
    login_window.show()
    
    # Start the event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()