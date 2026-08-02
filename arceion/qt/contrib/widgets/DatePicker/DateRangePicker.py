from collections.abc import Callable

from PyQt6.QtCore import QDate, QPoint, Qt
from PyQt6.QtWidgets import QCalendarWidget, QFrame, QHBoxLayout, QVBoxLayout, QWidget

from arceion.qt.contrib.styles.DatePicker import defaultDatePicker
from arceion.qt.contrib.widgets.Attr import Padding
from arceion.qt.contrib.widgets.Button import Button
from arceion.qt.util import Style

__all__ = ["DateRangePicker"]


class DateRangePicker(QWidget):
    """
    A date-range picker widget that lets the user choose a start and end date.

    Supports:
    - Selecting a start date first and then an end date from the popup calendar.
    - Displaying the selected range in a single button label.
    - Programmatic set, clear, and read operations.
    - Optional callback notification when the selected range changes.
    - Custom placeholder text and styling.
    """

    _onRangeChangedCallback: Callable[[QDate, QDate], None] | None = None

    def __init__(
        self,
        start: QDate | None = None,
        end: QDate | None = None,
        placeholder: str = "Pick a date range",
        dateFormat: str = "MMM d, yyyy",
        padding: Padding | None = None,
        style: str | Style = defaultDatePicker,
        direction: Qt.LayoutDirection = Qt.LayoutDirection.LeftToRight,
        onRangeChanged: Callable[[QDate, QDate], None] | None = None,
    ):
        """
        Initialize the DateRangePicker widget.

        Args:
            start (QDate | None): Initial start date for the range.
            end (QDate | None): Initial end date for the range.
            placeholder (str): Text shown when no range is selected.
            dateFormat (str): Format used to display both dates.
            padding (Padding | None): Optional padding data stored on the widget.
            style (str | Style): Style or QSS string used by the popup.
            direction (Qt.LayoutDirection): Layout direction of the picker.
            onRangeChanged (Callable[[QDate, QDate], None] | None): Callback
                fired when a complete range is selected.

        Returns:
            None
        """
        super().__init__()

        # Store the widget state so the selected range can be updated later.
        self._start = start
        self._end = end
        self._placeholder = placeholder
        self._dateFormat = dateFormat
        self._padding = padding
        self._style = style
        self._direction = direction
        self._pickingStart: bool = True

        # Create the trigger button that opens and closes the popup.
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._button = Button(
            text=self._placeholder,
            onClick=self._togglePopup,
        )
        layout.addWidget(self._button)

        # Build the popup calendar container used for range selection.
        self._popup = QFrame(self, Qt.WindowType.Popup)
        popupLayout = QVBoxLayout(self._popup)
        self._popup.setStyleSheet(self._style if isinstance(self._style, str) else self._style.qss)
        self._calendar = QCalendarWidget()
        self._calendar.clicked.connect(self._onDateSelected)
        popupLayout.addWidget(self._calendar)

        # Hide the popup until the user opens it.
        self._popup.hide()
        self._updateDisplay()
        if onRangeChanged:
            self.onRangeChanged(onRangeChanged)

    def _updateDisplay(self) -> None:
        """
        Refresh the button text so it reflects the current range state.

        Returns:
            None
        """
        if self._start and self._end:
            self._button.setText(f"{self._start.toString(self._dateFormat)} - {self._end.toString(self._dateFormat)}")
        elif self._start:
            self._button.setText(f"{self._start.toString(self._dateFormat)} - ...")
        else:
            self._button.setText(self._placeholder)

    def _togglePopup(self) -> None:
        """
        Show or hide the calendar popup.

        Positions the popup directly below the trigger button.

        Returns:
            None
        """
        if self._popup.isVisible():
            self._popup.hide()
        else:
            pos = self._button.mapToGlobal(QPoint(0, self._button.height()))
            self._popup.move(pos)
            self._popup.adjustSize()
            self._popup.show()

    def _onDateSelected(self, date: QDate) -> None:
        """
        Handle a date selection from the popup calendar.

        The first selection sets the start date, and the second selection
        completes the range and closes the popup.

        Args:
            date (QDate): The date selected by the user.

        Returns:
            None
        """
        if self._pickingStart:
            self._start = date
            self._end = None
            self._pickingStart = False
        else:
            self._end = date
            self._pickingStart = True
            self._popup.hide()
            if self._onRangeChangedCallback:
                self._onRangeChangedCallback(self._start, self._end)
        self._updateDisplay()

    def setRange(self, start: QDate, end: QDate) -> None:
        """
        Programmatically set the selected range.

        Args:
            start (QDate): The start date of the range.
            end (QDate): The end date of the range.

        Returns:
            None
        """
        self._start = start
        self._end = end
        self._updateDisplay()
        self._calendar.setSelectedDate(start)

    def clearRange(self) -> None:
        """
        Clear the selected range and reset the picker state.

        Returns:
            None
        """
        self._start = None
        self._end = None
        self._pickingStart = True
        self._updateDisplay()

    def selectedRange(self) -> tuple[QDate | None, QDate | None]:
        """
        Return the currently selected date range.

        Returns:
            tuple[QDate | None, QDate | None]: The start and end dates.
        """
        return (self._start, self._end)

    def onRangeChanged(self, action: Callable[[QDate, QDate], None]) -> None:
        """
        Set or replace the callback invoked when a full range is selected.

        Args:
            action (Callable[[QDate, QDate], None]): Function called after the
                end date is selected.

        Returns:
            None
        """
        self._onRangeChangedCallback = action
