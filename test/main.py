if __name__ == "__main__":
    import sys

    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    from test.MainWindow import MainWindow

    window = MainWindow()
    sys.exit(app.exec())
