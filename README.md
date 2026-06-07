<p align="center">
  <img src="arceion/qt/static/img/Arceion Logo 1024X1024 Transparent Round.png" alt="Arceion Logo" width="200"/>
</p>

<h1 align="center">Arceion Qt</h1>

<p align="center">
  <strong>A professional collection of Qt components and framework for Python.</strong>
</p>

<p align="center">
  <a href="https://pypi.org/project/arceion-qt/"><img src="https://img.shields.io/pypi/v/arceion-qt.svg" alt="PyPI version"></a>
  <a href="https://pypi.org/project/arceion-qt/"><img src="https://img.shields.io/pypi/pyversions/arceion-qt.svg" alt="Python versions"></a>
  <a href="https://github.com/Arceion/arceion-qt/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-Proprietary-blue.svg" alt="License"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>
</p>

---

Arceion Qt is a comprehensive suite of UI components and a structured framework designed to accelerate the development of desktop applications using PyQt6. It provides a robust architecture for managing views, navigation, asynchronous tasks, and API interactions.

## Key Features

- **Structured UI Framework**: Decoupled `Window` and `View` architecture for clean application flow.
- **Advanced Icon System**: Integrated Google Material Symbols support with customizable styles (Outlined, Rounded, Sharp).
- **Asynchronous Execution**: Built-in `ThreadPool` and `Worker` system for responsive UIs.
- **API Controller**: Simplified REST API interaction with automatic retry logic and authentication support.
- **ORM Integration**: Ready-to-use SQLAlchemy-based database layer.
- **Theming & Styles**: Flexible theme management and utility functions for CSS/QSS styling.
- **Logging**: Integrated logging system for better debugging and monitoring.

## Installation

Install Arceion Qt using `pip`:

```bash
pip install arceion-qt
```

### Dependencies
- PyQt6
- SQLAlchemy
- Requests
- Cryptography
- FontTools

## Quick Start

### 1. Creating a Basic Window and View

```python
from arceion.qt.core import Window, View
from PyQt6.QtWidgets import QLabel, QVBoxLayout

class MainView(View):
    def onCreate(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Hello from Arceion Qt!"))

    def onResume(self):
        print("View resumed")

    def onDestroy(self) -> bool:
        return super().onDestroy()

def main():
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = Window()
    window.navigate(MainView)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

### 2. Using Icons

```python
from arceion.qt.res import Icons
from PyQt6.QtWidgets import QPushButton

# Access material symbols easily
button = QPushButton()
button.setIcon(Icons.search.toPixmap(size=24, color="#FFFFFF"))
```

### 3. Background Tasks

```python
from arceion.qt.thread import ThreadPool

def heavy_computation(data):
    # Perform long-running task
    return f"Processed {data}"

def on_finished(result):
    print(f"Task result: {result}")

ThreadPool.start(heavy_computation, "my data", callback=on_finished)
```

## Documentation

For full documentation, please visit the [Wiki](https://github.com/Arceion/arceion-qt/wiki).

## Project Structure

- `arceion.qt.core`: Core Window and View management.
- `arceion.qt.api`: REST API client and controllers.
- `arceion.qt.db`: Database and ORM utilities.
- `arceion.qt.res`: Resource management (Icons, Themes, Colors).
- `arceion.qt.thread`: Multithreading and worker pools.
- `arceion.qt.util`: General purpose UI and stylesheet utilities.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under a Proprietary License. See `pyproject.toml` for more information.

---

<p align="center">
  Built with ❤️ by <strong>Arceion</strong>
</p>
