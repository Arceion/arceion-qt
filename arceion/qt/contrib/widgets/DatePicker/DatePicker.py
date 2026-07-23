from collections.abc import Callable

from PyQt6.QtCore import QDate, QPoint, Qt
from PyQt6.QtWidgets import QCalendarWidget, QFrame, QHBoxLayout, QVBoxLayout, QWidget

from arceion.qt.contrib.styles.DatePicker import defaultDatePicker
from arceion.qt.contrib.widgets.Attr import Padding
from arceion.qt.contrib.widgets.Button import Button
from arceion.qt.util import Style

__all__ = ["DatePicker"]

class DatePicker(QWidget):
    """
    A compact date picker widget with a button trigger and a calendar popup.

    Supports:
    - Selecting a single date from a popup calendar.
    - Displaying the selected date with a custom format string.
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
        dateFormat: str = "MMM d,yyyy",
        padding: Padding | None = None,
        style: str | Style = defaultDatePicker,
        direction: Qt.LayoutDirection = Qt.LayoutDirection.LeftToRight,
        onDateChanged: Callable[[QDate], None] | None = None,
    ):
        """
        Initialize the DatePicker widget.

        Args:
            date (QDate | None): Initial date shown by the widget.
            tooltip (str): Tooltip text for the trigger button.
            placeholder (str): Text shown when no date is selected.
            dateFormat (str): Format used to display the selected date.
            padding (Padding | None): Optional padding data stored on the widget.
            style (str | Style): Style or QSS string used by the popup.
            direction (Qt.LayoutDirection): Layout direction of the picker.
            onDateChanged (Callable[[QDate], None] | None): Callback fired when
                the selected date changes.

        Returns:
            None
        """
        super().__init__()

        # Store the widget state so it can be updated later.
        self._date = date
        self._tooltip = tooltip
        self._placeholder = placeholder
        self._dateFormat = dateFormat
        self._padding = padding
        self._style = style
        self._direction = direction

        # Create the trigger button that opens and closes the popup.
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._button = Button(
            text=self._placeholder,
            onClick=self._togglePopup,
        )
        layout.addWidget(self._button)

        # Build the popup calendar container used for date selection.
        self._popup = QFrame(self, Qt.WindowType.Popup)
        popupLayout = QVBoxLayout(self._popup)
        self._popup.setStyleSheet(
            self._style if isinstance(self._style, str) else self._style.qss
        )
        self._calendar = QCalendarWidget()
        self._calendar.clicked.connect(self._onDateSelected)
        popupLayout.addWidget(self._calendar)

        # Hide the popup until the user opens it.
        self._popup.hide()
        self._updateDisplay()
        if onDateChanged:
            self.onDateChanged(onDateChanged)

    def _updateDisplay(self) -> None:
        """
        Refresh the button text so it reflects the current date state.

        Returns:
            None
        """
        if self._date:
            self._button.setText(self._date.toString(self._dateFormat))
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

        Args:
            date (QDate): The date selected by the user.

        Returns:
            None
        """
        self._date = date
        self._updateDisplay()
        self._popup.hide()
        if self._onDateChangedCallback:
            self._onDateChangedCallback(date)

    def setDate(self, date: QDate) -> None:
        """
        Programmatically set the selected date.

        Args:
            date (QDate): The date to display and store.

        Returns:
            None
        """
        self._date = date
        self._updateDisplay()
        self._calendar.setSelectedDate(date)

    def clearDate(self) -> None:
        """
        Clear the selected date and reset the calendar state.

        Returns:
            None
        """
        self._date = None
        self._updateDisplay()
        self._calendar.setSelectedDate(QDate.currentDate())

    def selectedDate(self) -> QDate | None:
        """
        Return the currently selected date.

        Returns:
            QDate | None: The selected date, or None if nothing is set.
        """
        return self._date

    def onDateChanged(self, action: Callable[[QDate], None]) -> None:
        """
        Set or replace the callback invoked when the date changes.

        Args:
            action (Callable[[QDate], None]): Function called after a date is
                selected or updated.

        Returns:
            None
        """
        self._onDateChangedCallback = action
