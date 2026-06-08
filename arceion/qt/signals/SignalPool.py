from PyQt6.QtCore import QObject

__all__ = ["SignalPool"]


class SignalPool(QObject):
    """
    SignalPool(QObject)
    This class is a QObject that allows to create signals in a more organized way. It is used to create signals that
    are shared between different classes. It is a way to avoid creating signals in the global scope.
    """
