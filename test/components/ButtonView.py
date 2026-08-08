from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QTransform
from PyQt6.QtWidgets import QVBoxLayout

from arceion.qt.contrib.enums import BorderStyle, Size
from arceion.qt.contrib.styles.Button import (
    defaultButton,
    destructiveButton,
    ghostButton,
    linkButton,
    outlineButton,
    secondaryButton,
)
from arceion.qt.contrib.styles.Label import defaultLabel
from arceion.qt.contrib.widgets.Attr import Border, Margin
from arceion.qt.contrib.widgets.Button import Button
from arceion.qt.contrib.widgets.Card import ScrollableFrame
from arceion.qt.contrib.widgets.Label import Label
from arceion.qt.contrib.widgets.Widget import HBoxWidget
from arceion.qt.core import View, Window
from arceion.qt.res import Icons
from arceion.qt.util import UI

from ..AppTheme import AppTheme

__all__ = ["ButtonView"]


class ButtonView(View):
    def __init__(self, parent: Window | None = None, name: str | None = None):
        super().__init__(parent, name)

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(Margin(horizontal=UI.dp(60), vertical=UI.dp(40)))
        self.mainLayout.setSpacing(UI.dp(20))
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignTop)

        self.scrollArea = ScrollableFrame(self)

        defaultLabelStyle = defaultLabel.update(color=AppTheme.colors.text.name())
        defaultButtonStyle = defaultButton.update(
            backgroundColor=AppTheme.colors.primary.name(),
            color=AppTheme.colors.color.name(),
            hoverColor=AppTheme.colors.hoverPrimary.name(),
        )
        outlineButtonStyle = outlineButton.update(
            color=AppTheme.colors.text.name(),
            hoverColor=AppTheme.colors.hoverGhost.name(),
            border=Border(AppTheme.colors.borderColor.name(), BorderStyle.SOLID, 1).qss,
            hoverBorder=Border(AppTheme.colors.hoverBorderColor.name(), BorderStyle.SOLID, 1).qss,
        )
        secondaryButtonStyle = secondaryButton.update(
            color=AppTheme.colors.text.name(),
            backgroundColor=AppTheme.colors.secondary.name(),
            hoverColor=AppTheme.colors.hoverSecondary.name(),
        )
        ghostButtonStyle = ghostButton.update(
            color=AppTheme.colors.text.name(),
            hoverColor=AppTheme.colors.hoverGhost.name(),
        )
        destructiveButtonStyle = destructiveButton.update(
            color=AppTheme.colors.colorDestructive.name(),
            backgroundColor=AppTheme.colors.destructive.name(),
            hoverColor=AppTheme.colors.hoverDestructive.name(),
        )
        linkButtonStyle = linkButton.update(
            color=AppTheme.colors.text.name(),
        )

        self.basicButtonLabel = Label("Basic Button", style=defaultLabelStyle)
        self.basicButtonContainer = HBoxWidget(self, spacing=UI.dp(12))

        self.btn1 = Button("Button", style=defaultButtonStyle, size=Size.Default)
        self.btn2 = Button(
            icon=Icons.Rounded.arrow_upward_alt.update(color=AppTheme.colors.color.name()),
            style=defaultButtonStyle,
            size=Size.Default,
        )
        self.btn3 = Button("Button", style=outlineButtonStyle, size=Size.Default)
        self.btn4 = Button(
            icon=Icons.Rounded.arrow_upward_alt.update(color=AppTheme.colors.text.name()),
            style=outlineButtonStyle,
            size=Size.Default,
        )

        self.basicButtonContainer.addWidget(self.btn1)
        self.basicButtonContainer.addWidget(self.btn2)
        self.basicButtonContainer.addWidget(self.btn3)
        self.basicButtonContainer.addWidget(self.btn4)

        self.buttonSizeLabel = Label("Size", style=defaultLabelStyle)
        self.buttonSizeContainer = HBoxWidget(self, spacing=UI.dp(12))

        topRightArrow = QIcon(
            Icons.Rounded.arrow_upward_alt.update(color=AppTheme.colors.primary.name())
            .toPixmap()
            .transformed(QTransform().rotate(45))
        )
        self.btn5 = Button("Extra Small", style=outlineButtonStyle, size=Size.ExtraSmall)
        self.btn6 = Button(icon=topRightArrow, style=outlineButtonStyle, size=Size.ExtraSmall)
        self.btn7 = Button("Small", style=outlineButtonStyle, size=Size.Small)
        self.btn8 = Button(icon=topRightArrow, style=outlineButtonStyle, size=Size.Small)
        self.btn9 = Button("Default", style=outlineButtonStyle, size=Size.Default)
        self.btn10 = Button(icon=topRightArrow, style=outlineButtonStyle, size=Size.Default)
        self.btn11 = Button("Large", style=outlineButtonStyle, size=Size.Large)
        self.btn12 = Button(icon=topRightArrow, style=outlineButtonStyle, size=Size.Large)

        self.buttonSizeContainer.addWidget(self.btn5)
        self.buttonSizeContainer.addWidget(self.btn6)
        self.buttonSizeContainer.addSpacing(UI.dp(32))
        self.buttonSizeContainer.addWidget(self.btn7)
        self.buttonSizeContainer.addWidget(self.btn8)
        self.buttonSizeContainer.addSpacing(UI.dp(32))
        self.buttonSizeContainer.addWidget(self.btn9)
        self.buttonSizeContainer.addWidget(self.btn10)
        self.buttonSizeContainer.addSpacing(UI.dp(32))
        self.buttonSizeContainer.addWidget(self.btn11)
        self.buttonSizeContainer.addWidget(self.btn12)

        self.defaultButtonLabel = Label("Default Button", style=defaultLabelStyle)
        self.defaultButton = Button("Button", style=defaultButtonStyle, size=Size.Default)

        self.outlineButtonLabel = Label("Outline Button", style=defaultLabelStyle)
        self.outlineButton = Button("Button", style=outlineButtonStyle, size=Size.Default)

        self.secondaryButtonLabel = Label("Secondary Button", style=defaultLabelStyle)
        self.secondaryButton = Button("Button", style=secondaryButtonStyle, size=Size.Default)

        self.ghostButtonLabel = Label("Ghost Button", style=defaultLabelStyle)
        self.ghostButton = Button("Button", style=ghostButtonStyle, size=Size.Default)

        self.destructiveButtonLabel = Label("Destructive Button", style=defaultLabelStyle)
        self.destructiveButton = Button("Button", style=destructiveButtonStyle, size=Size.Default)

        self.linkButtonLabel = Label("Link Button", style=defaultLabelStyle)
        self.linkButton = Button("Button", style=linkButtonStyle, size=Size.Default)

        self.iconButtonLabel = Label("Icon Button", style=defaultLabelStyle)
        self.iconButton = Button(
            icon=Icons.Rounded.arrow_circle_up.update(color=AppTheme.colors.text.name()),
            style=outlineButtonStyle,
            size=Size.Default,
        )

        self.withIconButtonLabel = Label("With Icon Button", style=defaultLabelStyle)
        self.withIconButtonContainer = HBoxWidget(self, spacing=UI.dp(12))

        self.btn13 = Button(
            "New Branch",
            icon=Icons.Rounded.fork_right.update(color=AppTheme.colors.text.name()),
            style=outlineButtonStyle,
            size=Size.Default,
            toolButtonStyle=Qt.ToolButtonStyle.ToolButtonTextBesideIcon,
        )
        self.btn14 = Button(
            "Fork",
            icon=Icons.Rounded.fork_left.update(color=AppTheme.colors.text.name()),
            style=outlineButtonStyle,
            size=Size.Default,
            toolButtonStyle=Qt.ToolButtonStyle.ToolButtonTextUnderIcon,
        )

        self.withIconButtonContainer.addWidget(
            self.btn13, alignment=Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignTop
        )
        self.withIconButtonContainer.addWidget(
            self.btn14, alignment=Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignTop
        )

        self.roundedButtonLabel = Label("Rounded", style=defaultLabelStyle)
        self.roundedButtonContainer = HBoxWidget(self, spacing=UI.dp(12))

        self.btn15 = Button("Get Started", style=defaultButtonStyle.update(borderRadius=UI.dp(16)), size=Size.Default)
        self.btn16 = Button(
            icon=Icons.Rounded.arrow_upward_alt.update(color=AppTheme.colors.text.name()),
            style=outlineButtonStyle.update(borderRadius=UI.dp(16)),
            size=Size.Default,
        )

        self.roundedButtonContainer.addWidget(self.btn15)
        self.roundedButtonContainer.addWidget(self.btn16)

        self.spinnerButtonLabel = Label("Spinner", style=defaultLabelStyle)
        self.spinnerButton = Button(size=Size.Default)
        self.spinnerButton.setLoading(True, AppTheme.colors.color.name())
        self.spinnerButton.onClick(self.spinnerButton.toggleLoading)

        self.scrollArea.layout.addWidget(self.basicButtonLabel)
        self.scrollArea.layout.addWidget(self.basicButtonContainer)
        self.scrollArea.layout.addWidget(self.buttonSizeLabel)
        self.scrollArea.layout.addWidget(self.buttonSizeContainer)
        self.scrollArea.layout.addWidget(self.defaultButtonLabel)
        self.scrollArea.layout.addWidget(self.defaultButton, alignment=Qt.AlignmentFlag.AlignLeft)
        self.scrollArea.layout.addWidget(self.outlineButtonLabel)
        self.scrollArea.layout.addWidget(self.outlineButton, alignment=Qt.AlignmentFlag.AlignLeft)
        self.scrollArea.layout.addWidget(self.secondaryButtonLabel)
        self.scrollArea.layout.addWidget(self.secondaryButton, alignment=Qt.AlignmentFlag.AlignLeft)
        self.scrollArea.layout.addWidget(self.ghostButtonLabel)
        self.scrollArea.layout.addWidget(self.ghostButton, alignment=Qt.AlignmentFlag.AlignLeft)
        self.scrollArea.layout.addWidget(self.destructiveButtonLabel)
        self.scrollArea.layout.addWidget(self.destructiveButton, alignment=Qt.AlignmentFlag.AlignLeft)
        self.scrollArea.layout.addWidget(self.linkButtonLabel)
        self.scrollArea.layout.addWidget(self.linkButton, alignment=Qt.AlignmentFlag.AlignLeft)
        self.scrollArea.layout.addWidget(self.iconButtonLabel)
        self.scrollArea.layout.addWidget(self.iconButton, alignment=Qt.AlignmentFlag.AlignLeft)
        self.scrollArea.layout.addWidget(self.withIconButtonLabel)
        self.scrollArea.layout.addWidget(self.withIconButtonContainer)
        self.scrollArea.layout.addWidget(self.roundedButtonLabel)
        self.scrollArea.layout.addWidget(self.roundedButtonContainer)
        self.scrollArea.layout.addWidget(self.spinnerButtonLabel)
        self.scrollArea.layout.addWidget(self.spinnerButton, alignment=Qt.AlignmentFlag.AlignLeft)

        self.mainLayout.addWidget(self.scrollArea)

        self.setLayout(self.mainLayout)

    def onCreate(self) -> None:
        pass

    def onResume(self) -> None:
        pass

    def onDestroy(self) -> bool:
        return super().onDestroy()

    def updateTheme(self):
        defaultLabelStyle = defaultLabel.update(color=AppTheme.colors.text.name())
        defaultButtonStyle = defaultButton.update(
            backgroundColor=AppTheme.colors.primary.name(),
            color=AppTheme.colors.color.name(),
            hoverColor=AppTheme.colors.hoverPrimary.name(),
        )
        outlineButtonStyle = outlineButton.update(
            color=AppTheme.colors.text.name(),
            hoverColor=AppTheme.colors.hoverGhost.name(),
            border=Border(AppTheme.colors.borderColor.name(), BorderStyle.SOLID, 1).qss,
            hoverBorder=Border(AppTheme.colors.hoverBorderColor.name(), BorderStyle.SOLID, 1).qss,
        )
        secondaryButtonStyle = secondaryButton.update(
            color=AppTheme.colors.text.name(),
            backgroundColor=AppTheme.colors.secondary.name(),
            hoverColor=AppTheme.colors.hoverSecondary.name(),
        )
        ghostButtonStyle = ghostButton.update(
            color=AppTheme.colors.text.name(),
            hoverColor=AppTheme.colors.hoverGhost.name(),
        )
        destructiveButtonStyle = destructiveButton.update(
            color=AppTheme.colors.colorDestructive.name(),
            backgroundColor=AppTheme.colors.destructive.name(),
            hoverColor=AppTheme.colors.hoverDestructive.name(),
        )
        linkButtonStyle = linkButton.update(
            color=AppTheme.colors.text.name(),
        )

        self.basicButtonLabel.setStyle(defaultLabelStyle)

        self.btn1.setStyleSheetFromStyle(defaultButtonStyle)
        self.btn2.setStyleSheetFromStyle(defaultButtonStyle)
        self.btn2.setIcon(Icons.Rounded.arrow_upward_alt.update(color=AppTheme.colors.color.name()))
        self.btn3.setStyleSheetFromStyle(outlineButtonStyle)
        self.btn4.setStyleSheetFromStyle(outlineButtonStyle)
        self.btn4.setIcon(Icons.Rounded.arrow_upward_alt.update(color=AppTheme.colors.text.name()))

        self.buttonSizeLabel.setStyle(defaultLabelStyle)

        topRightArrow = QIcon(
            Icons.Rounded.arrow_upward_alt.update(color=AppTheme.colors.primary.name())
            .toPixmap()
            .transformed(QTransform().rotate(45))
        )

        self.btn5.setStyleSheetFromStyle(outlineButtonStyle)
        self.btn6.setStyleSheetFromStyle(outlineButtonStyle)
        self.btn6.setIcon(topRightArrow)
        self.btn7.setStyleSheetFromStyle(outlineButtonStyle)
        self.btn8.setStyleSheetFromStyle(outlineButtonStyle)
        self.btn8.setIcon(topRightArrow)
        self.btn9.setStyleSheetFromStyle(outlineButtonStyle)
        self.btn10.setStyleSheetFromStyle(outlineButtonStyle)
        self.btn10.setIcon(topRightArrow)
        self.btn11.setStyleSheetFromStyle(outlineButtonStyle)
        self.btn12.setStyleSheetFromStyle(outlineButtonStyle)
        self.btn12.setIcon(topRightArrow)

        self.defaultButtonLabel.setStyle(defaultLabelStyle)
        self.defaultButton.setStyleSheetFromStyle(defaultButtonStyle)

        self.outlineButtonLabel.setStyle(defaultLabelStyle)
        self.outlineButton.setStyleSheetFromStyle(outlineButtonStyle)

        self.secondaryButtonLabel.setStyle(defaultLabelStyle)
        self.secondaryButton.setStyleSheetFromStyle(secondaryButtonStyle)

        self.ghostButtonLabel.setStyle(defaultLabelStyle)
        self.ghostButton.setStyleSheetFromStyle(ghostButtonStyle)

        self.destructiveButtonLabel.setStyle(defaultLabelStyle)
        self.destructiveButton.setStyleSheetFromStyle(destructiveButtonStyle)

        self.linkButtonLabel.setStyle(defaultLabelStyle)
        self.linkButton.setStyleSheetFromStyle(linkButtonStyle)

        self.iconButtonLabel.setStyle(defaultLabelStyle)
        self.iconButton.setStyleSheetFromStyle(outlineButtonStyle)
        self.iconButton.setIcon(Icons.Rounded.arrow_circle_up.update(color=AppTheme.colors.text.name()))

        self.withIconButtonLabel.setStyle(defaultLabelStyle)
        self.btn13.setStyleSheetFromStyle(outlineButtonStyle)
        self.btn13.setIcon(Icons.Rounded.fork_right.update(color=AppTheme.colors.text.name()))
        self.btn14.setStyleSheetFromStyle(outlineButtonStyle)
        self.btn14.setIcon(Icons.Rounded.fork_left.update(color=AppTheme.colors.text.name()))

        self.roundedButtonLabel.setStyle(defaultLabelStyle)
        self.btn15.setStyleSheetFromStyle(defaultButtonStyle.update(borderRadius=UI.dp(16)))
        self.btn16.setStyleSheetFromStyle(outlineButtonStyle.update(borderRadius=UI.dp(16)))
        self.btn16.setIcon(Icons.Rounded.arrow_upward_alt.update(color=AppTheme.colors.text.name()))
