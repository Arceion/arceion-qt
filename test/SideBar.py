from PyQt6.QtGui import QIcon

from arceion.qt.contrib.enums import Size
from arceion.qt.contrib.styles.Button import ghostButton
from arceion.qt.contrib.styles.Label import defaultLabel
from arceion.qt.contrib.widgets.Attr import Margin
from arceion.qt.contrib.widgets.Button import Button
from arceion.qt.contrib.widgets.Card import ScrollableFrame
from arceion.qt.contrib.widgets.Label import Label
from arceion.qt.contrib.widgets.Widget import HBoxWidget
from arceion.qt.logger import Logger
from arceion.qt.res import Icons
from arceion.qt.util import UI

from .AppTheme import AppTheme, Theme
from .components import ButtonView

__all__ = ["SideBar"]


class SideBar(ScrollableFrame):
    components: dict = {"Button": ButtonView}

    @staticmethod
    def getThemeIcon() -> QIcon:
        return (
            Icons.Filled.Rounded.sunny.update(color="#FFFFFF")
            if AppTheme.colorTheme == Theme.DARK
            else Icons.Filled.Rounded.nightlight.update(color="#000000")
        )

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.widgets: list[Label] = []
        self.parent = parent
        self.setFixedWidth(UI.dp(200))

        defaultLabelStyle = defaultLabel.update(color=AppTheme.colors.text.name(), fontSize=UI.sp(14))

        self.layout.addSpacing(UI.dp(16))

        self.topBar = HBoxWidget(self, margin=Margin(0))
        self.componentsLabel = Label("Components", style=defaultLabelStyle.update(fontSize=UI.sp(16)))
        self.themeButton = Button(
            icon=self.getThemeIcon(), size=Size.ExtraSmall, onClick=self.parent.toggleTheme, style=ghostButton
        )
        self.topBar.addWidget(self.componentsLabel)
        self.topBar.addStretch(1)
        self.topBar.addWidget(self.themeButton)

        self.layout.addWidget(self.topBar)

        self.layout.addSpacing(UI.dp(24))
        for component in self.components.keys():
            label = Label(component, parent=self, onClick=lambda c=component: self.view(c), style=defaultLabelStyle)
            self.widgets.append(label)
            self.layout.addWidget(label)
        self.layout.addStretch(1)

    def view(self, component: str):
        if not self.parent or component not in self.components.keys() or not hasattr(self.parent, "navigate"):
            Logger.warning(f"Parent or component not found: {component}")
            return
        self.parent.navigate(self.components[component])

    def updateTheme(self):
        defaultLabelStyle = defaultLabel.update(color=AppTheme.colors.text.name(), fontSize=UI.sp(14))

        self.componentsLabel.setStyle(defaultLabelStyle.update(fontSize=UI.sp(16)))
        self.themeButton.setIcon(self.getThemeIcon())
        for widget in self.widgets:
            widget.setStyle(defaultLabelStyle)
