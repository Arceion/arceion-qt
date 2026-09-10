from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout

from arceion.qt.contrib.styles.Label import defaultLabel
from arceion.qt.contrib.styles.Table import defaultTable
from arceion.qt.contrib.widgets.Attr import Margin
from arceion.qt.contrib.widgets.Card import ScrollableFrame
from arceion.qt.contrib.widgets.Label import Label
from arceion.qt.contrib.widgets.Table import Table
from arceion.qt.core import View, Window
from arceion.qt.util import UI

from ..AppTheme import AppTheme

__all__ = ["TableView"]


class TableView(View):
    def __init__(self, parent: Window | None = None, name: str | None = None):
        super().__init__(parent, name)

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(Margin(horizontal=UI.dp(60), vertical=UI.dp(40)))
        self.mainLayout.setSpacing(UI.dp(20))
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignTop)

        self.scrollArea = ScrollableFrame(self)
        self.tableLabel = Label()
        self.table = Table(
            headers=["Invoice", "Status", "Method", "Amount"],
            rows=[
                ["INV001", "Paid", "Credit Card", "$250.00"],
                ["INV002", "Pending", "PayPal", "$150.00"],
                ["INV003", "Unpaid", "Bank Transfer", "$350.00"],
                ["INV004", "Paid", "Credit Card", "$450.00"],
                ["INV005", "Paid", "PayPal", "$550.00"],
            ],
            footer=["", "", "Total", "$1,750.00"],
        )

        self.scrollArea.layout.addWidget(self.tableLabel)
        self.scrollArea.layout.addWidget(self.table)
        self.mainLayout.addWidget(self.scrollArea)
        self.setLayout(self.mainLayout)
        self.updateTheme()

    def onCreate(self) -> None:
        pass

    def onResume(self) -> None:
        pass

    def onDestroy(self) -> bool:
        return super().onDestroy()

    def updateTheme(self):
        self.tableLabel.setStyle(defaultLabel.update(color=AppTheme.colors.text.name()))
        self.tableLabel.setText("Table")
        self.table.setStyle(
            defaultTable.update(
                backgroundColor=AppTheme.colors.background.name(),
                alternateBackgroundColor=AppTheme.colors.background.name(),
                color=AppTheme.colors.text.name(),
                gridlineColor=AppTheme.colors.borderColor.name(),
                selectionBackgroundColor=AppTheme.colors.hoverSecondary.name(),
                selectionColor=AppTheme.colors.text.name(),
                rowBorder=f"1px solid {AppTheme.colors.borderColor.name()}",
                headerBackgroundColor=AppTheme.colors.secondary.name(),
                headerBorder=f"1px solid {AppTheme.colors.borderColor.name()}",
                headerColor=AppTheme.colors.text.name(),
            )
        )
        self.table.setHoverColor(AppTheme.colors.hoverSecondary.name())
        self.table.setFooterColors(
            AppTheme.colors.secondary.name(),
            AppTheme.colors.borderColor.name(),
        )
