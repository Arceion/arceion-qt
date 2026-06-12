from PyQt6.QtCore import pyqtSignal

from .SignalPool import SignalPool

__all__ = ["WinSigPool"]


class WindowSignalPoolManager(SignalPool):
    newViewAdded = pyqtSignal(object)
    tabRemoved = pyqtSignal(object)
    themeChanged = pyqtSignal()


WinSigPool = WindowSignalPoolManager()
