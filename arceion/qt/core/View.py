from abc import ABCMeta, abstractmethod
from typing import Self

from PyQt6.QtWidgets import QWidget

from arceion.qt.logger import Logger

from .Window import Window

__all__ = ["View", "WindowType"]

WindowType = Window


class ViewMeta(type(QWidget), ABCMeta):
    pass


class View(QWidget, metaclass=ViewMeta):
    """
    The View class serves as an abstract base class for creating user interface views. It defines
    the structure and essential methods that these views should implement, enforcing a consistent
    approach to view creation, lifecycle management, and navigation within an application.

    This class enables standardization in the creation of UI components, ensuring that derived
    classes adhere to the outlined behavior and lifecycle. It also provides common functionality
    such as setting object names, managing the busy state of a view, and supporting navigation
    between views.

    Attributes:
            parent (WindowType | None): The parent window or widget associated with this view. Can
                    be None if there is no parent.

    Methods:
            setViewName(self, name: str) -> None: Sets the name of the view.
            getViewName(self) -> str: Retrieves the name of the view.
            onCreate(self) -> None: Handles the initialization logic for the view.
            onResume(self) -> None: Defines the logic to be executed when the view is resumed.
            setStatus(self, isBusy: bool) -> None: Sets the status of the view.
            onDestroy(self) -> bool: Determines if the view can be safely destroyed.
            navigate(self, view: Self | None, *args, **kwargs) -> None: Navigates to a specified view.
    """

    parent: WindowType | None
    __viewName: str = ""
    _isBusy: bool = False

    def __init__(self, parent: WindowType | None, name: str | None = None):
        """
        Initializes a View object with an optional parent and object name.

        Args:
                parent (WindowType | None): The parent window or widget to which this
                        view belongs. Can be None if there is no parent.
                name (str | None): The object name to assign to this view. Defaults to None.
        """

        self.parent = parent

        super().__init__()
        super().setParent(self.parent)

        if name:
            self.setObjectName(name)

    def setViewName(self, name: str) -> None:
        """
        Sets the name of the view.

        Args:
                name (str): The name to set for the view.
        """
        self.__viewName = name

    def getViewName(self) -> str:
        """
        Retrieves the name of the view associated with the current instance.

        Returns:
                str: The name of the view.
        """
        return self.__viewName

    @abstractmethod
    def onCreate(self) -> None:
        """
        Handles the initialization logic for the current object when it is created.

        This method is executed during the creation phase of the object. It initializes
        essential components, prepares necessary resources, and sets up the object for
        use. Override this method to define custom initialization logic specific to
        the derived class.

        Returns:
                None
        """

    @abstractmethod
    def onResume(self) -> None:
        """
        Defines an abstract method that should be implemented by subclasses to handle
        tasks that need to be performed when the related component or object is
        resumed.

        Methods:
                onResume: An abstract method that must be implemented to execute actions
                        during the resumption phase of an object's lifecycle.
        """

    def setStatus(self, isBusy: bool) -> None:
        """
        Sets the status of an object to indicate whether it is busy or not.

        This method updates the internal attribute that tracks the busy status of
        the object. It is commonly used to manage the operational state of an
        object in contexts requiring state-based logic.

        Args:
                isBusy: A boolean indicating the new status of the object. Set to
                        True if the object is busy, or False if it is not.
        """
        self._isBusy = isBusy

    @abstractmethod
    def onDestroy(self) -> bool:
        """
        Determines if the object can be safely destroyed.

        This method evaluates the status of the object to determine whether it is
        busy or not. If the object is not busy, it indicates that it can be
        destroyed safely.

        Returns:
                bool: True if the object is not busy and thus can be destroyed,
                False otherwise.
        """
        return not self._isBusy

    def navigate(self, view: Self | None, *args, **kwargs) -> None:
        """
        Navigates to a specified view within a parent system. Validates that the view
        provided is a subclass of the `View` class and that the current view has a parent
        defined, ensuring navigational integrity.

        Args:
                view (Type['View'] | None): The view class to navigate to. The view must be
                        a subclass of the `View` class.
                *args: Additional positional arguments passed to the parent navigate method.
                **kwargs: Additional keyword arguments passed to the parent navigate method.

        Raises:
                TypeError: Raised if the provided view is not a subclass of `View`.
                ValueError: Raised if the current view does not have a parent defined.
        """
        if not issubclass(view, View):
            Logger.error(f"View {view} is not an instance of View")
            raise TypeError(f"View {view} is not an instance of View")
        if not self.parent:
            Logger.error(f"Parent is not set for the view {self.__viewName}")
            raise ValueError(f"Parent is not set for the view {self.__viewName}")
        self.parent.navigate(view, *args, **kwargs)
