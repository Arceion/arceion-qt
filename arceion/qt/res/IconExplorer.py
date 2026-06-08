from PyQt6.QtCore import QObject, QRunnable, QSize, Qt, QThreadPool, pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QScrollArea,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from ..logger import Logger
from .Icons import Icons, SystemIcon


class SearchWorkerSignals(QObject):
    """Signals for the search worker."""

    results_ready = pyqtSignal(list)


class SearchWorker(QRunnable):
    """Worker for running the search operation in a separate thread."""

    def __init__(self, query, items):
        super().__init__()
        self.query = query
        self.items = items
        self.signals = SearchWorkerSignals()

    def run(self):
        query = self.query.lower()
        filtered_items = []

        # Search for exact matches
        if query in self.items:
            filtered_items.append(query)

        # Search for items that start with query
        for item in self.items:
            if item.startswith(query) and item not in filtered_items:
                filtered_items.append(item)

        # Search for items that contain query
        for item in self.items:
            if query in item and item not in filtered_items:
                filtered_items.append(item)

        self.signals.results_ready.emit(filtered_items)


class IconsExplorer(QWidget):
    def __init__(self, iconSet):
        super().__init__()
        self.iconSet = iconSet
        self.thread_pool = QThreadPool()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Icons Explorer")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(Icons.Filled.home)

        # Main Layout
        main_layout = QHBoxLayout()

        # Left Section (Search & Results)
        left_layout = QVBoxLayout()

        # Search Bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search icons...")
        self.search_bar.textChanged.connect(self.on_search)
        left_layout.addWidget(self.search_bar)

        # Scroll Area for Filtered Icons
        self.scroll_area = QScrollArea()
        self.scroll_area_widget = QWidget()
        self.scroll_area_layout = QVBoxLayout()
        self.scroll_area_widget.setLayout(self.scroll_area_layout)
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.scroll_area.setWidgetResizable(True)
        left_layout.addWidget(self.scroll_area)

        main_layout.addLayout(left_layout)

        # Right Section (Key List)
        self.key_list = QListWidget()
        self.key_list.itemClicked.connect(self.key_selected)
        main_layout.addWidget(self.key_list)

        # Populate Keys in Right Section
        self.populate_keys()

        self.setLayout(main_layout)

    def populate_keys(self):
        """Populates the right section with all iconSet keys."""
        for key in self.iconSet.keys():
            item = QListWidgetItem(key)
            self.key_list.addItem(item)

    def key_selected(self, item):
        """Sets the search query to the selected key from the right section."""
        self.search_bar.setText(item.text())
        self.on_search()

    def on_search(self):
        """Initiates the search operation."""
        query = self.search_bar.text()
        worker = SearchWorker(query, list(self.iconSet.keys()))
        worker.signals.results_ready.connect(self.update_icons)
        self.thread_pool.start(worker)

    def update_icons(self, filtered_items):
        """Updates the UI with the filtered search results."""
        # Clear existing icons
        for i in reversed(range(self.scroll_area_layout.count())):
            widget = self.scroll_area_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Display icon and variants for the filtered items
        for key in filtered_items[:4]:
            self.display_icon_with_variants(key)

    def display_icon_with_variants(self, key):
        try:
            if normal := getattr(Icons, key):
                self.display_icon(normal)
            if normalOutlined := getattr(Icons.Outlined, key):
                self.display_icon(normalOutlined)
            if normalRounded := getattr(Icons.Rounded, key):
                self.display_icon(normalRounded)

            if filled := getattr(Icons.Filled, key):
                self.display_icon(filled)
            if filledOutlined := getattr(Icons.Filled.Outlined, key):
                self.display_icon(filledOutlined)
            if filledRounded := getattr(Icons.Filled.Rounded, key):
                self.display_icon(filledRounded)
        except Exception as e:  # noqa: BLE001
            Logger.error(e)

    def display_icon(self, icon: SystemIcon):
        try:
            """Displays the icon in the left section."""
            label = QToolButton()
            label.setIcon(icon.update(size=64))
            label.setIconSize(QSize(64, 64))
            label.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
            label.setText(icon.toStr())
            label.setStyleSheet("background-color: transparent; border: none;")
            self.scroll_area_layout.addWidget(label)
        except Exception as e:  # noqa: BLE001
            Logger.error(e)
