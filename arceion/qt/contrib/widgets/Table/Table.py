from collections.abc import Iterable, Sequence

from PyQt6.QtCore import QEvent, Qt
from PyQt6.QtGui import QColor, QFont, QMouseEvent, QPainter, QPen
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QStyle,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
)

from arceion.qt.contrib.styles.Table import defaultTable
from arceion.qt.util import Style

__all__ = ["Table"]


class _TableItemDelegate(QStyledItemDelegate):
    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index) -> None:
        table = self.parent()
        if isinstance(table, Table) and table.footerRow == index.row():
            painter.save()
            painter.fillRect(option.rect, table.footerColor)
            painter.setPen(QPen(table.footerBorderColor))
            painter.drawLine(option.rect.topLeft(), option.rect.topRight())
            painter.restore()
            footerOption = QStyleOptionViewItem(option)
            footerOption.font.setWeight(QFont.Weight.DemiBold)
            super().paint(painter, footerOption, index)
            return
        if (
            isinstance(table, Table)
            and table.hoveredRow == index.row()
            and not option.state & QStyle.StateFlag.State_Selected
        ):
            painter.save()
            painter.fillRect(option.rect, table.hoverColor)
            painter.restore()
        super().paint(painter, option, index)


class Table(QTableWidget):
    """A compact, shadcn-inspired table backed by ``QTableWidget``.

    ``headers`` and ``rows`` are optional convenience data. Cells are converted
    to text unless a ``QTableWidgetItem`` is supplied directly.
    """

    def __init__(
        self,
        headers: Sequence[str] | None = None,
        rows: Iterable[Sequence[object]] | None = None,
        footer: Sequence[object] | None = None,
        style: str | Style = defaultTable,
        selectable: bool = True,
        hoverColor: QColor | str = "#F4F4F5",
        parent: QWidget | None = None,
    ):
        super().__init__(parent)

        self.hoveredRow = -1
        self.footerRow = -1
        self._footerValues: list[object] | None = None
        self.hoverColor = QColor(hoverColor)
        self.footerColor = QColor("#FAFAFA")
        self.footerBorderColor = QColor("#E4E4E7")
        self.setObjectName("Table")
        self.setStyleSheet(style if isinstance(style, str) else style.qss)
        self.setAlternatingRowColors(False)
        self.setShowGrid(False)
        self.setWordWrap(False)
        self.setMouseTracking(True)
        self.viewport().setMouseTracking(True)
        self.setItemDelegate(_TableItemDelegate(self))
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
            if selectable
            else QAbstractItemView.SelectionMode.NoSelection
        )
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        horizontalHeader = self.horizontalHeader()
        horizontalHeader.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        horizontalHeader.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        horizontalHeader.setHighlightSections(False)
        self.verticalHeader().setVisible(False)

        if headers is not None:
            self.setHeaders(headers)
        if rows is not None:
            self.setRows(rows)
        if footer is not None:
            self.setFooter(footer)

    def setHeaders(self, headers: Sequence[str]) -> None:
        """Replace the table headers while preserving the current rows."""
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels([str(header) for header in headers])

    def setStyle(self, style: str | Style) -> None:
        """Apply a raw QSS string or a ``Style`` object to the table."""
        self.setStyleSheet(style if isinstance(style, str) else style.qss)

    def setHoverColor(self, color: QColor | str) -> None:
        """Set the background color used for the hovered row."""
        self.hoverColor = QColor(color)
        self.viewport().update()

    def setFooterColors(self, background: QColor | str, border: QColor | str) -> None:
        """Set the background and top border colors used by the footer row."""
        self.footerColor = QColor(background)
        self.footerBorderColor = QColor(border)
        self.viewport().update()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        row = self.indexAt(event.position().toPoint()).row()
        if row != self.hoveredRow:
            previousRow = self.hoveredRow
            self.hoveredRow = row
            self._updateRow(previousRow)
            self._updateRow(row)
        super().mouseMoveEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        previousRow = self.hoveredRow
        self.hoveredRow = -1
        self._updateRow(previousRow)
        super().leaveEvent(event)

    def _updateRow(self, row: int) -> None:
        if row >= 0:
            self.viewport().update(
                self.visualRect(self.model().index(row, 0)).united(
                    self.visualRect(self.model().index(row, self.columnCount() - 1))
                )
            )

    def setRows(self, rows: Iterable[Sequence[object]]) -> None:
        """Replace all rows with the supplied values."""
        materializedRows = list(rows)
        footer = self._footerValues
        self.clearFooter()
        columnCount = self.columnCount()
        if materializedRows and columnCount == 0:
            columnCount = max(len(row) for row in materializedRows)
            self.setColumnCount(columnCount)

        self.setRowCount(0)
        for row in materializedRows:
            self.addRow(row)
        if footer is not None:
            self.setFooter(footer)

    def addRow(self, values: Sequence[object]) -> int:
        """Append a row and return its zero-based index."""
        rowIndex = self.rowCount()
        self.insertRow(rowIndex)
        for columnIndex, value in enumerate(values):
            if columnIndex >= self.columnCount():
                break
            item = value if isinstance(value, QTableWidgetItem) else QTableWidgetItem(str(value))
            self.setItem(rowIndex, columnIndex, item)
        return rowIndex

    def clearRows(self) -> None:
        """Remove all data rows without changing the headers."""
        self.setRows([])

    def setFooter(self, values: Sequence[object]) -> None:
        """Replace the footer row with the supplied values."""
        self.clearFooter()
        if self.columnCount() == 0:
            self.setColumnCount(len(values))

        self.footerRow = self.rowCount()
        self._footerValues = list(values)
        self.insertRow(self.footerRow)
        for columnIndex, value in enumerate(values):
            if columnIndex >= self.columnCount():
                break
            item = value if isinstance(value, QTableWidgetItem) else QTableWidgetItem(str(value))
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable & ~Qt.ItemFlag.ItemIsEditable)
            self.setItem(self.footerRow, columnIndex, item)

    def clearFooter(self) -> None:
        """Remove the footer row without changing the table data."""
        if self.footerRow >= 0:
            self.removeRow(self.footerRow)
        self.footerRow = -1
        self._footerValues = None
