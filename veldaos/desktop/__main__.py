import sys
from PyQt6.QtWidgets import QApplication
from .main_window import MainWindow
from loguru import logger

def main():
    """Main entry point for the VeldaOS desktop application."""
    try:
        # Configure logging
        logger.add(
            "veldaos.log",
            rotation="500 MB",
            retention="10 days",
            level="INFO"
        )
        
        # Create Qt application
        app = QApplication(sys.argv)
        
        # Set application style
        app.setStyle("Fusion")
        
        # Create and show main window
        window = MainWindow()
        window.show()
        
        # Start event loop
        sys.exit(app.exec())
    except Exception as e:
        logger.error(f"Application failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 