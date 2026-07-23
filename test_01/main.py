from PyQt6.QtCore import Qt, QTimer,QSize
from PyQt6.QtWidgets import QVBoxLayout, QLabel

from arceion.qt.core import Window, View
from arceion.qt.util import UI
from arceion.qt.contrib.enums import FontWeight
from arceion.qt.contrib.styles.Label import label
from arceion.qt.contrib.widgets.Widget import HBoxWidget
from arceion.qt.contrib.widgets.Button import Button
from arceion.qt.contrib.styles.Button import (
    defaultButton,
    destructiveButton,
    secondaryButton,
    outlineButton,
    ghostButton,
    linkButton,
    pill,
)
from arceion.qt.contrib.widgets.Attr import Margin, Padding
from PyQt6.QtGui import QIcon


class HomeView(View):
    def __init__(self, parent: Window | None = None, name: str | None = None):
        super().__init__(parent, name)

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(Margin(horizontal=UI.dp(60), vertical=UI.dp(40)))
        self.mainLayout.setSpacing(UI.dp(20))
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignTop)

        # --- Default Button ---
        self.defaultLabel = QLabel('# Default')
        self.defaultLabel.setStyleSheet(label.update(
            fontSize=UI.sp(16),
            fontWeight=FontWeight.SemiBold,
        ).qss)
        self.btnDefault = Button(text="Default", style=defaultButton)

        # --- Variants ---
        self.variantLabel = QLabel('# Variants')
        self.variantLabel.setStyleSheet(label.update(
            fontSize=UI.sp(16),
            fontWeight=FontWeight.SemiBold,
        ).qss)
        self.variantContainer = HBoxWidget(self, spacing=UI.dp(10))
        self.btnDestructive = Button(text="Destructive", style=destructiveButton)
        self.btnSecondary = Button(text="Secondary", style=secondaryButton)
        self.btnOutline = Button(text="Outline", style=outlineButton)
        self.btnGhost = Button(text="Ghost", style=ghostButton)
        self.btnLink = Button.asLink(text="Link", url="https://www.qt.io",style=linkButton)
        self.variantContainer.addWidget(self.btnDestructive)
        self.variantContainer.addWidget(self.btnSecondary)
        self.variantContainer.addWidget(self.btnOutline)
        self.variantContainer.addWidget(self.btnGhost)
        self.variantContainer.addWidget(self.btnLink)

        # --- Sizes ---
        self.sizeLabel = QLabel('# Sizes')
        self.sizeLabel.setStyleSheet(label.update(
            fontSize=UI.sp(16),
            fontWeight=FontWeight.SemiBold,
        ).qss)
        self.sizeContainer = HBoxWidget(self, spacing=UI.dp(10))
        self.btnSmall = Button(text="Small", style=defaultButton)
        self.btnSmall.setIconSize(UI.size(12, 12))
        self.btnSmall.setFixedSize(UI.dp(60), UI.dp(30))

        self.btnMedium = Button(text="Medium", style=defaultButton)
        self.btnMedium.setIconSize(UI.size(16, 16))
        self.btnMedium.setFixedSize(UI.dp(80), UI.dp(40))

        self.btnLarge = Button(text="Large", style=defaultButton)
        self.btnLarge.setIconSize(UI.size(20, 20))
        self.btnLarge.setPadding(Padding(UI.dp(20)))
        self.btnLarge.setFixedSize(UI.dp(120), UI.dp(50))

        self.sizeContainer.addWidget(self.btnSmall)
        self.sizeContainer.addWidget(self.btnMedium)
        self.sizeContainer.addWidget(self.btnLarge)

        # --- Disabled ---
        self.disabledLabel = QLabel('# Disabled')
        self.disabledLabel.setStyleSheet(label.update(
            fontSize=UI.sp(16),
            fontWeight=FontWeight.SemiBold,
        ).qss)
        self.btnDisabled = Button(text="Disabled", style=defaultButton)
        self.btnDisabled.setDisabled(True)

        # --- Pill Shape ---
        self.pillLabel = QLabel('# Pill Shape')
        self.pillLabel.setStyleSheet(label.update(
            fontSize=UI.sp(16),
            fontWeight=FontWeight.SemiBold,
        ).qss)

        # Use the pill() wrapper on a style
        self.btnPill = Button(text="Rounded", style=pill(defaultButton))
        self.btnPill.setPadding(Padding(UI.dp(8), UI.dp(20)))   # optional: extra horizontal padding
        self.btnPill.setMinimumSize(UI.dp(120), UI.dp(40))      # optional: ensure pill shape


        # --- Loading Demo ---
        self.loadingLabel = QLabel('# Loading State')
        self.loadingLabel.setStyleSheet(label.update(
            fontSize=UI.sp(16),
            fontWeight=FontWeight.SemiBold,
        ).qss)
        self.btnLoadingDemo = Button(text="Load Data", style=defaultButton)

        # --- Icon Showcase ---
        self.iconLabel = QLabel('# Icon Showcase')
        self.iconLabel.setStyleSheet(label.update(
            fontSize=UI.sp(16),
            fontWeight=FontWeight.SemiBold,
        ).qss)

        self.iconContainer = HBoxWidget(self, spacing=UI.dp(10))

        # Icon-only button (square footprint, no text)
        self.btnIconOnly = Button(style=pill(defaultButton))
        self.btnIconOnly.setIcon(QIcon("D:/arcEON/arceion-qt/test_01/assets/icons/arceion.png"))
        self.btnIconOnly.setFixedSize(UI.dp(40), UI.dp(40))
        self.btnIconOnly.setToolTip("Click to upload a file")
        # Text + Icon button
        self.btnTextIcon = Button(text="Upload", style=defaultButton)
        self.btnTextIcon.setIcon(QIcon("D:/arcEON/arceion-qt/test_01/assets/icons/arceion.png"), UI.size(20, 20))

        # Ensure style allows both text and icon
        self.btnTextIcon.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.btnTextIcon.setToolTip("Click to upload a file")

        self.iconContainer.addWidget(self.btnIconOnly)
        self.iconContainer.addWidget(self.btnTextIcon)
        # Add everything to layout
        self.mainLayout.addWidget(self.defaultLabel)
        self.mainLayout.addWidget(self.btnDefault, alignment=Qt.AlignmentFlag.AlignLeft)
        self.mainLayout.addWidget(self.variantLabel)
        self.mainLayout.addWidget(self.variantContainer)
        self.mainLayout.addWidget(self.sizeLabel)
        self.mainLayout.addWidget(self.sizeContainer)
        self.mainLayout.addWidget(self.disabledLabel)
        self.mainLayout.addWidget(self.btnDisabled, alignment=Qt.AlignmentFlag.AlignLeft)
        self.mainLayout.addWidget(self.pillLabel)
        self.mainLayout.addWidget(self.btnPill, alignment=Qt.AlignmentFlag.AlignLeft)
        self.mainLayout.addWidget(self.loadingLabel)
        self.mainLayout.addWidget(self.btnLoadingDemo)
        self.mainLayout.addWidget(self.iconLabel)
        self.mainLayout.addWidget(self.iconContainer)

        self.setLayout(self.mainLayout)

    def onCreate(self) -> None:
        self.btnDefault.onClick(lambda: print("Default clicked"))
        self.btnDestructive.onClick(lambda: print("Destructive clicked"))
        self.btnSecondary.onClick(lambda: print("Secondary clicked"))
        self.btnOutline.onClick(lambda: print("Outline clicked"))
        self.btnGhost.onClick(lambda: print("Ghost clicked"))
        self.btnPill.onClick(lambda: print("Pill clicked"))

        self.btnLoadingDemo.onClick(self.startLoading)

    def onResume(self) -> None:
        print("HomeView resumed — refreshing state")
        if self.btnLoadingDemo.isLoading():
            self.btnLoadingDemo.setLoading(False)

    def onDestroy(self) -> bool:
        print("HomeView destroyed — cleaning up")
        if self.btnLoadingDemo.isLoading():
            self.btnLoadingDemo.setLoading(False)
        return super().onDestroy()

    def startLoading(self):
        self.btnLoadingDemo.setLoading(True, spinnerColor="#00FF00")
        QTimer.singleShot(2000, lambda: self.btnLoadingDemo.setLoading(False))


class MainWindow(Window):
    def __init__(self):
        super().__init__()
        self.setObjectName('MainWindow')
        self.setWindowTitle('Test Buttons')
        self.resize(800, 600)
        self.setStyleSheet("background-color: black;")

        self.navigate(HomeView)
        self.show()


if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
