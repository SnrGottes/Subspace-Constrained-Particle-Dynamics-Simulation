import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from src.gui.main_window import MainWindow

def load_stylesheet() -> str:
    qss_path = Path(__file__).parent / "styles" / "base_theme.qss"
    
    if not qss_path.exists():
        print(f"Warning: The style sheet file was not found at the specified path: {qss_path}")
        return ""
        
    with open(qss_path, "r", encoding="utf-8") as f:
        return f.read()

def run_application():
    app = QApplication(sys.argv)
    
    style_data = load_stylesheet()
    if style_data:
        app.setStyleSheet(style_data)
        
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())