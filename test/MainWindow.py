from PyQt6.QtGui import QPalette

from arceion.qt.contrib.widgets.Attr import Margin
from arceion.qt.core import Window
from arceion.qt.res import Icons
from arceion.qt.util import UI

from .AppTheme import AppTheme, Theme
from .components import ButtonView
from .SideBar import SideBar

__all__ = ["MainWindow"]


class MainWindow(Window):
    def __init__(self):
        super().__init__(row=1, column=2)
        self.setObjectName("MainWindow")
        self.setWindowTitle("Arceion Qt Components")
        AppTheme.setColorTheme(Theme.DARK)
        self.resize(800, 600)
        self.setWindowIcon(Icons.Filled.Rounded.dashboard)
        pal = self.palette()
        pal.setColor(QPalette.ColorRole.Window, AppTheme.colors.background)
        pal.setColor(QPalette.ColorRole.WindowText, AppTheme.colors.text)
        self.setPalette(pal)
        self.setFocus()

        self.siderBar = SideBar(self, spacing=UI.dp(8), margin=Margin(UI.dp(16), UI.dp(8)))
        self.mainLayout.addWidget(self.siderBar, 1, 0, 1, 1)

        self.navigate(ButtonView)

        self.show()

    def toggleTheme(self):
        AppTheme.setColorTheme(Theme.LIGHT if AppTheme.colorTheme == Theme.DARK else Theme.DARK)
        self.updateTheme()

    def updateTheme(self):
        pal = self.palette()
        pal.setColor(QPalette.ColorRole.Window, AppTheme.colors.background)
        pal.setColor(QPalette.ColorRole.WindowText, AppTheme.colors.text)
        self.setPalette(pal)
        self.setFocus()

        self.siderBar.updateTheme()
        self.centralWidget.currentWidget().updateTheme()
