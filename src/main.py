try:
    import gui, sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    
    window = gui.MainWindow()
    window.show()
    
    sys.exit(app.exec())

except Exception as e:
    print(e)