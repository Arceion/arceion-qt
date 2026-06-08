from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import (
    QGridLayout,
    QMainWindow,
    QSizePolicy,
    QStackedWidget,
    QWidget,
)

from arceion.qt.contrib.widgets.Attr import Margin
from arceion.qt.logger import Logger
from arceion.qt.signals import WinSigPool
from arceion.qt.util import UI

__all__ = ["Window"]


class Window(QMainWindow):
    """
    Window(parent: Optional[QWidget] = None, flags: Union[Qt.WindowFlags, Qt.WindowType] = Qt.WindowFlags(),
    row: int = 1, column: int = 1, rowSpan: int = 1, columnSpan: int = 1,
    alignment: Union[Qt.Alignment, Qt.AlignmentFlag] = Qt.Alignment())

    Description:
            Represents the main window of the application with a modular layout structure and
            navigation capabilities.

            This class is designed as the primary window container for the application. It incorporates
            a central widget that uses QStackedWidget to enable dynamic view switching. The window
            supports navigation, including moving forward to specific views or navigating backward in
            the navigation history. Views can be dynamically added, removed, or replaced, making the
            window suitable for applications with multi-view management requirements.

    Attributes:
            mainWidget (QWidget): The parent widget that encapsulates the main layout.
            mainLayout (QGridLayout): The grid layout applied to the `mainWidget` for managing
                    child widgets.
            centralWidget (QStackedWidget): The central widget that contains views for dynamic
                    switching.
            navigationHistory (List[type]): List maintaining the history of navigated views.

    Methods:
            navigate(self, view: Type['View'], *args, **kwargs) -> None: Navigates to a specified view.
            navigateBack(self) -> None: Handles navigation back to a previous view.
            getViews(self) -> Dict[QWidget, QWidget]: Retrieves a dictionary mapping views to their corresponding widgets.
            removeView(self, view) -> None: Removes a specified view from the user interface.
            onTabChanged(self, tab: str) -> None: Handles updates when a tab is changed in the application.
            removeCurrentView(self) -> None: Removes the currently displayed view from the central widget.
    """

    _PAGES: dict[QWidget, QWidget]
    mainWidget: QWidget
    mainLayout: QGridLayout
    centralWidget: QStackedWidget
    navigationHistory: list[type]

    def __init__(self, **__kwargs):
        """
        Initializes the main window of the application with customizable layout and
        central widget configuration. The class creates a QMainWindow instance with
        a QStackedWidget as its central widget, wrapped in a parent QWidget containing
        a QGridLayout. Margins, spacing, and alignment are configurable via arguments.

        Args:
                **__kwargs: Keyword arguments to customize the main window configuration.
                        parent (Optional[QObject]): The parent widget of the QMainWindow.
                        row (Optional[int]): The row at which the central widget is added
                                in the QGridLayout (default is 1).
                        column (Optional[int]): The column at which the central widget is added
                                in the QGridLayout (default is 1).
                        rowSpan (Optional[int]): The number of rows spanned by the central widget
                                in the QGridLayout (default is 1).
                        columnSpan (Optional[int]): The number of columns spanned by the central
                                widget in the QGridLayout (default is 1).
                        alignment (Optional[Qt.AlignmentFlag]): Alignment of the central widget
                                inside the QGridLayout (default is Qt.AlignmentFlag.AlignCenter).
        """

        super(QMainWindow, self).__init__(__kwargs.get("parent"))

        self._PAGES, self.navigationHistory = {}, []

        UI.setLogicalDpi(self.screen().logicalDotsPerInch())

        self.mainWidget = QWidget()
        self.mainLayout = QGridLayout(self.mainWidget)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(Margin(0))
        self.mainWidget.setLayout(self.mainLayout)
        self.mainWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.centralWidget = QStackedWidget()
        row = __kwargs.get("row") or 1
        column = __kwargs.get("column") or 1
        row_span = __kwargs.get("rowSpan") or 1
        column_span = __kwargs.get("columnSpan") or 1
        alignment = __kwargs.get("alignment")
        if alignment:
            self.mainLayout.addWidget(self.centralWidget, row, column, row_span, column_span, alignment)
        else:
            self.mainLayout.addWidget(self.centralWidget, row, column, row_span, column_span)

        self.setCentralWidget(self.mainWidget)

    def navigate(self, view, *args, **kwargs) -> None:
        """
        Navigates to a specified view in the application. If the view already exists, it
        resumes the existing instance. If the view does not exist, it creates a new
        instance, adds it to the central widget, and executes its creation lifecycle
        method.

        Args:
                view: Type of the view to navigate to. It should be a callable that returns
                        an instance of the desired view class.
                *args: Variable length argument list to pass to the view's constructor or
                        lifecycle methods.
                **kwargs: Arbitrary keyword arguments to pass to the view's constructor or
                        lifecycle methods.

        Raises:
                AttributeError: If the view does not define the required lifecycle
                        methods (`onResume` or `onCreate`) when invoked.
        """

        resume = False
        if view is None:
            return
        if view in self._PAGES.keys():
            resume = True
        if view not in self._PAGES.keys():
            page = view(self, *args, **kwargs)
            self._PAGES[view] = page
            self.centralWidget.addWidget(self._PAGES[view])
        self.centralWidget.setCurrentWidget(self._PAGES[view])
        self.navigationHistory.append(self._PAGES[view].__class__)
        Logger.debug(f"Navigated to {view.__name__}, resume: {resume}")
        if resume:
            if not hasattr(self._PAGES[view], "onResume"):
                raise AttributeError(f"View {view} does not have an onResume method")
            self._PAGES[view].onResume(*args, **kwargs)
        if not resume:
            if not hasattr(self._PAGES[view], "onCreate"):
                raise AttributeError(f"View {view} does not have an onCreate method")
            WinSigPool.newViewAdded.emit(self._PAGES[view])
            self._PAGES[view].onCreate(*args, **kwargs)

    def navigateBack(self) -> None:
        """
        Handles navigation within an application by allowing the user to navigate back
        to previously visited views. Maintains a history of navigated views and invokes
        the appropriate navigation action for the last view in the history.

        Returns:
                None

        Raises:
                None
        """

        Logger.debug(f"navigation history {self.navigationHistory}")
        if len(self.navigationHistory) > 1:
            self.navigationHistory.pop()
            lastView = self.navigationHistory[-1]
            Logger.debug(f"last view {lastView}")
            self.navigate(lastView)
        else:
            Logger.warning("No more views to navigate back to.")

    def getViews(self) -> dict[QWidget, QWidget]:
        """
        Retrieves a dictionary mapping views to their corresponding widgets.

        Returns:
                Dict[QWidget, QWidget]: A dictionary where the keys are QWidget instances
                representing views and the values are QWidget instances representing the
                corresponding widgets.
        """

        return self._PAGES

    def removeView(self, view) -> None:
        """
        Removes a view from the user interface and its associated resources.

        This method handles the safe removal of a view, including calling its
        `onDestroy` method if present, emitting the `tabRemoved` signal,
        removing the associated widget from the layout, and deallocating its
        resources. Any error during the process is logged.

        Args:
                view: The instance of the view to be removed.

        Raises:
                KeyError: If the view's class is not found in the `_PAGES` dictionary,
                        the exception is caught and logged without propagation.
        """

        try:
            if hasattr(self._PAGES[view.__class__], "onDestroy") and self._PAGES[view.__class__].onDestroy():
                WinSigPool.tabRemoved.emit(self._PAGES[view.__class__])
                self.mainLayout.removeWidget(self._PAGES[view.__class__])
                self._PAGES[view.__class__].deleteLater()
                del self._PAGES[view.__class__]
        except KeyError as e:
            Logger.error(f"Remove View Error: {e}")

    @pyqtSlot(str)
    def onTabChanged(self, tab: str) -> None:
        """
        Handles updates when a tab is changed in the application.

        Args:
                tab (str): The identifier or name of the newly selected tab.

        """

    def removeCurrentView(self) -> None:
        """
        Removes the currently displayed view from the central widget.

        This method accesses the current view displayed in the central widget and removes it
        from the layout.

        Raises:
                Any exceptions raised by `self.centralWidget.currentWidget()` or
                `self.removeView()` internally.
        """
        self.removeView(self.centralWidget.currentWidget())
