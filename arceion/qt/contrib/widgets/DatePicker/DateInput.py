from collections.abc import Callable

from PyQt6.QtCore import QDate, QPoint, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QCalendarWidget, QFrame, QHBoxLayout, QLineEdit, QVBoxLayout, QWidget

from arceion.qt.contrib.styles.Button import ghostButton
from arceion.qt.contrib.styles.DateInput import defaultDateInput
from arceion.qt.contrib.widgets.Attr import Padding
from arceion.qt.contrib.widgets.Button import Button
from arceion.qt.util import Style

__all__ = ["DateInput"]


class DateInput(QWidget):
    """
    A date input widget combining a text field and a calendar popup button.

    Supports:
    - Manual date entry via a QLineEdit with format validation.
    - Visual date selection via a calendar popup triggered by an icon button.
    - Automatic validation and reset on invalid input.
    - Programmatic get/set/clear of the selected date.
    - Callback notification when the date changes via typing or calendar selection.
    - Custom date format string (e.g. 'yyyy-MM-dd', 'MMM d, yyyy').
    - Custom placeholder text shown inside the input field.
    - Optional custom icon for the calendar trigger button.
    - RTL layout via `direction`.
    - Style customization via a Style object or raw QSS string.
    """

    _onDateChangedCallback: Callable[[QDate], None] | None = None

    def __init__(
        self,
        date: QDate | None = None,
        placeholder: str = "yyyy-MM-dd",
        dateFormat: str = "yyyy-MM-dd",
        icon: QIcon | None = None,
        padding: Padding | None = None,
        style: str | Style = defaultDateInput,
        direction: Qt.LayoutDirection = Qt.LayoutDirection.LeftToRight,
        onDateChanged: Callable[[QDate], None] | None = None,
    ):
        """
        Initialize the DateInput widget.

        Args:
            date (QDate | None): Initial date to display. Defaults to None (empty).
            placeholder (str): Hint text shown inside the input when empty.
                Should match the dateFormat so the user knows what to type.
            dateFormat (str): Format string used for both displaying and parsing
                the date (e.g. 'yyyy-MM-dd', 'MMM d, yyyy').
            icon (QIcon | None): Optional icon for the calendar trigger button.
                Defaults to a calendar emoji if not provided.
            padding (Padding | None): Padding applied to the widget. Currently
                stored for future use in layout adjustments.
            style (str | Style): Style object or raw QSS string applied to the
                container frame and calendar popup.
            direction (Qt.LayoutDirection): Layout direction for the input field
                (LTR or RTL).
            onDateChanged (Callable[[QDate], None] | None): Callback fired when
                the date changes via typing or calendar selection.

        Returns:
            None
        """
        super().__init__()

        # -- store attributes ------------------------------------------
        self._date = date
        self._placeholder = placeholder
        self._dateFormat = dateFormat
        self._icon = icon
        self._padding = padding
        self._style = style
        self._direction = direction

        # -- outer layout ----------------------------------------------
        # holds only the container frame; zero margins so the container
        # border sits flush with the widget boundary
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # -- container -------------------------------------------------
        # a QFrame that draws a single shared border around both the
        # input field and the calendar button, matching shadcn's
        # InputGroup pattern where the border wraps the whole group
        self._container = QFrame()
        self._container.setStyleSheet(
            self._style if isinstance(self._style, str) else self._style.qss
        )
        containerLayout = QHBoxLayout(self._container)
        containerLayout.setContentsMargins(0, 0, 0, 0)
        containerLayout.setSpacing(0)

        # -- text input ------------------------------------------------
        # user types a date here; validated on editingFinished signal
        self._input = QLineEdit()
        self._input.setPlaceholderText(self._placeholder)
        self._input.setLayoutDirection(self._direction)
        self._input.editingFinished.connect(self._onEditingFinished)
        containerLayout.addWidget(self._input)

        # -- calendar trigger button -----------------------------------
        # ghost style (transparent, no border) so it blends into the
        # container border rather than drawing its own border on top
        self._button = Button(
            text="📅" if not self._icon else "",
            icon=self._icon if self._icon else None,
            style=ghostButton,
            onClick=self._togglePopup,
        )
        containerLayout.addWidget(self._button)

        # add the assembled container into the outer layout
        layout.addWidget(self._container)

        # -- calendar popup --------------------------------------------
        # Qt.WindowType.Popup closes automatically on outside click,
        # matching shadcn's Popover dismiss behavior
        self._popup = QFrame(self, Qt.WindowType.Popup)
        popupLayout = QVBoxLayout(self._popup)
        self._popup.setStyleSheet(
            self._style if isinstance(self._style, str) else self._style.qss
        )
        self._calendar = QCalendarWidget()
        self._calendar.clicked.connect(self._onDateSelected)
        popupLayout.addWidget(self._calendar)
        self._popup.hide()

        # -- apply initial date ----------------------------------------
        if self._date:
            self._input.setText(self._date.toString(self._dateFormat))
            self._calendar.setSelectedDate(self._date)

        # -- wire callback ---------------------------------------------
        if onDateChanged:
            self.onDateChanged(onDateChanged)

    # -- private -------------------------------------------------------

    def _onEditingFinished(self) -> None:
        """
        Handle the editingFinished signal from the input field.

        Parses the typed text against dateFormat. If valid, stores the
        date and fires the callback. If invalid, resets the input to the
        last valid date or clears it if no date was previously set.

        Returns:
            None
        """
        text = self._input.text().strip()
        parsed = QDate.fromString(text, self._dateFormat)
        if parsed.isValid():
            self._date = parsed
            self._calendar.setSelectedDate(parsed)
            if self._onDateChangedCallback:
                self._onDateChangedCallback(self._date)
        else:
            # reset to last known valid date to prevent invalid state
            if self._date:
                self._input.setText(self._date.toString(self._dateFormat))
            else:
                self._input.clear()

    def _onDateSelected(self, date: QDate) -> None:
        """
        Handle a date click in the calendar popup.

        Updates the input field text, stores the date, closes the popup,
        and fires the callback.

        Args:
            date (QDate): The date the user clicked in the calendar.

        Returns:
            None
        """
        self._date = date
        self._input.setText(date.toString(self._dateFormat))
        self._calendar.setSelectedDate(date)
        self._popup.hide()
        if self._onDateChangedCallback:
            self._onDateChangedCallback(date)

    def _togglePopup(self) -> None:
        """
        Show or hide the calendar popup.

        Positions the popup aligned to the right edge of the trigger
        button with a 10px gap below it, matching shadcn's Popover
        align='end' and sideOffset=10 behavior.

        Returns:
            None
        """
        if self._popup.isVisible():
            self._popup.hide()
        else:
            # align popup to right edge of the calendar button
            buttonBottomRight = self._button.mapToGlobal(
                QPoint(self._button.width(), self._button.height())
            )
            self._popup.adjustSize()
            pos = QPoint(
                buttonBottomRight.x() - self._popup.width(),
                buttonBottomRight.y() + 10,  # sideOffset=10 from shadcn
            )
            self._popup.move(pos)
            self._popup.show()

    # -- public API ----------------------------------------------------

    def setDate(self, date: QDate) -> None:
        """
        Programmatically set the selected date.

        Updates both the input field text and the calendar selection.

        Args:
            date (QDate): The date to set.

        Returns:
            None
        """
        self._date = date
        self._input.setText(date.toString(self._dateFormat))
        self._calendar.setSelectedDate(date)

    def clearDate(self) -> None:
        """
        Reset the widget to an unselected state.

        Clears the input field and resets the calendar to today's date.

        Returns:
            None
        """
        self._date = None
        self._input.clear()
        self._calendar.setSelectedDate(QDate.currentDate())

    def selectedDate(self) -> QDate | None:
        """
        Return the currently selected date.

        Returns:
            QDate: The selected date, or None if no date is set.
        """
        return self._date

    def onDateChanged(self, action: Callable[[QDate], None]) -> None:
        """
        Set or replace the date-changed callback.

        Fired when the date changes via either typing or calendar
        selection. The callback receives the new QDate as its argument.

        Args:
            action (Callable[[QDate], None]): Function executed when
                the date changes.

        Returns:
            None
        """
        self._onDateChangedCallback = action
