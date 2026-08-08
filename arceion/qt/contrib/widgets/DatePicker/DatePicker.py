from collections.abc import Callable

from PyQt6.QtCore import QDate, QPoint, Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout

from arceion.qt.contrib.styles.Button import outlineButton
from arceion.qt.contrib.styles.DatePicker import defaultDatePicker
from arceion.qt.contrib.widgets.Attr import Padding
from arceion.qt.contrib.widgets.Button import Button
from arceion.qt.contrib.widgets.CalendarGrid import CalendarGrid
from arceion.qt.util import UI, Style

__all__ = ["DatePicker"]


class DatePicker(QFrame):
    """
    A button-triggered date picker, matching shadcn's basic DatePicker:
    a single button showing the selected date (or a placeholder) that
    opens a calendar popup on click. No text entry — use DateInput for
    typed date entry with format validation.

    Supports:
    - Selecting a date from a popup calendar.
    - Programmatic set, clear, and read operations.
    - Optional callback notification when the selected date changes.
    - Custom placeholder text and styling.
    """

    _onDateChangedCallback: Callable[[QDate], None] | None = None

    def __init__(
        self,
        date: QDate | None = None,
        tooltip: str = "",
        placeholder: str = "Pick a date",
        dateFormat: str = "MMMM dd, yyyy",
        width: int = 240,
        height: int = 40,
        padding: Padding | None = None,
        style: str | Style = defaultDatePicker,
        direction: Qt.LayoutDirection = Qt.LayoutDirection.LeftToRight,
        onDateChanged: Callable[[QDate], None] | None = None,
    ):
        super().__init__()

        self._date = date
        self._tooltip = tooltip
        self._placeholder = placeholder
        self._dateFormat = dateFormat
        self._width = width
        self._height = height
        self._padding = padding
        self._style = style
        self._direction = direction

        self._buildUi()
        self._applyInitialDate()

        if onDateChanged:
            self.onDateChanged(onDateChanged)

    def _buildUi(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.setObjectName("DatePicker")
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setLayoutDirection(self._direction)
        self.setFixedSize(UI.dp(self._width), UI.dp(self._height))

        # outline variant already gives us the bordered box — no need for a
        # separate DatePickerTrigger QSS rule or a wrapping QFrame.
        self._button = Button(
            text="\U0001f5d3  " + self._placeholder,
            tooltip=self._tooltip or "Open calendar",
            style=outlineButton,
            onClick=self._togglePopup,
        )
        self._button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._button.setLayoutDirection(self._direction)
        self._button.setFixedSize(UI.dp(self._width), UI.dp(self._height))
        layout.addWidget(self._button)

        self._popup = QFrame(self, Qt.WindowType.Popup)
        self._popup.setObjectName("DatePickerPopup")
        self._popup.setStyleSheet(self._style if isinstance(self._style, str) else self._style.qss)
        popupLayout = QVBoxLayout(self._popup)
        popupLayout.setContentsMargins(0, 0, 0, 0)

        self._calendar = CalendarGrid(selectedDate=self._date, parent=self._popup)
        self._calendar.dateSelected.connect(self._onDateSelected)
        popupLayout.addWidget(self._calendar)
        self._popup.hide()

        if self._padding is not None:
            layout.setContentsMargins(
                self._padding.left,
                self._padding.top,
                self._padding.right,
                self._padding.bottom,
            )

    def _applyInitialDate(self) -> None:
        if self._date is not None:
            self._calendar.setSelectedDate(self._date)
            self._updateDisplay()
        else:
            # Scroll to the current month WITHOUT marking today as selected —
            # setSelectedDate would render today as a filled pill even though
            # nothing has actually been chosen yet.
            self._calendar.setViewDate(QDate.currentDate())

    def _updateDisplay(self) -> None:
        if self._date is not None:
            self._button.setText("\U0001f5d3  " + self._date.toString(self._dateFormat))
        else:
            self._button.setText("\U0001f5d3  " + self._placeholder)

    def _onDateSelected(self, date: QDate) -> None:
        if self._date is not None and date == self._date:
            self.clearDate()
            self._popup.hide()
            return

        self._setDate(date, notify=True)
        self._popup.hide()

    def _togglePopup(self) -> None:
        if self._popup.isVisible():
            self._popup.hide()
            return

        pos = self._button.mapToGlobal(QPoint(0, self._button.height()))
        self._popup.move(pos)
        self._popup.adjustSize()
        self._popup.show()
        self._popup.raise_()
        self._calendar.setFocus()

    def _setDate(self, date: QDate, notify: bool = False) -> None:
        self._date = date
        self._calendar.setSelectedDate(date)
        self._updateDisplay()
        if notify and self._onDateChangedCallback is not None:
            self._onDateChangedCallback(date)

    def setDate(self, date: QDate) -> None:
        self._setDate(date, notify=True)

    def clearDate(self) -> None:
        self._date = None
        self._updateDisplay()
        self._calendar.setViewDate(QDate.currentDate())

    def selectedDate(self) -> QDate | None:
        return self._date

    def onDateChanged(self, action: Callable[[QDate], None]) -> None:
        self._onDateChangedCallback = action
