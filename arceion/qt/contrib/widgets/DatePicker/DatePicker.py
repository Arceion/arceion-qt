from typing import Callable, Optional

from PyQt6.QtCore import  Qt, QDate ,QPoint
from PyQt6.QtWidgets import  QWidget, QHBoxLayout,QVBoxLayout,QFrame , QCalendarWidget

from arceion.qt.util import  Style
from arceion.qt.contrib.styles.DatePicker import defaultDatePicker
from arceion.qt.contrib.widgets.Attr import Padding
from arceion.qt.contrib.widgets.Button import Button

__all__ = ["DatePicker"]

class DatePicker(QWidget):
    """..."""
    
    _onDateChangedCallback: Optional[Callable[[QDate],None]] = None

    def __init__(
        self,
        date: Optional[QDate] = None,
        tooltip: str = "",
        placeholder: str = "Pick a date",
        dateFormat: str = "MMM d,yyyy",
        padding: Optional[Padding] = None,
        style: str | Style = defaultDatePicker,
        direction: Qt.LayoutDirection = Qt.LayoutDirection.LeftToRight,
        onDateChanged: Optional[Callable[[QDate],None]] = None,
    ):
        super().__init__()
        # store attributes
        # build child widgets
        # call _updateDisplay()
        self._date = date
        self._tooltip = tooltip
        self._placeholder = placeholder 
        self._dateFormat = dateFormat
        self._padding = padding
        self._style = style
        self._direction = direction
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._button = Button(
            text=self._placeholder,   # before any date is picked, show placeholder
            onClick=self._togglePopup # clicking opens/closes the calendar
        )
        layout.addWidget(self._button)
        self._popup = QFrame(self, Qt.WindowType.Popup)
        popupLayout = QVBoxLayout(self._popup)
        self._popup.setStyleSheet(self._style if isinstance(self._style, str) else self._style.qss)
        self._calendar = QCalendarWidget()
        self._calendar.clicked.connect(self._onDateSelected)
        popupLayout.addWidget(self._calendar)

        self._popup.hide()  # hidden by default
        self._updateDisplay()
        if onDateChanged:
            self.onDateChanged(onDateChanged)

    def _updateDisplay(self) -> None:
        if self._date:
            self._button.setText(self._date.toString(self._dateFormat))
        else:
            self._button.setText(self._placeholder)

    def _togglePopup(self) -> None:
        if self._popup.isVisible():
            self._popup.hide()
        else:
            # calculate position: directly below the button
            pos = self._button.mapToGlobal(QPoint(0, self._button.height()))
            self._popup.move(pos)
            self._popup.adjustSize()
            self._popup.show()

    def _onDateSelected(self, date: QDate) -> None:
        self._date = date                          # 1. remember the picked date
        self._updateDisplay()                      # 2. update button text
        self._popup.hide()                         # 3. close the calendar
        if self._onDateChangedCallback:            # 4. fire callback if set
            self._onDateChangedCallback(date)

    def setDate(self, date: QDate) -> None:
        # store date, update display
        self._date = date
        self._updateDisplay()
        self._calendar.setSelectedDate(date)

    def clearDate(self) -> None:
        # set self._date to None, update display
        self._date= None
        self._updateDisplay()
        self._calendar.setSelectedDate(QDate.currentDate())

    def selectedDate(self) -> Optional[QDate]:
        # just return self._date
        return self._date

    def onDateChanged(self, action: Callable[[QDate], None]) -> None:
        # store the callback, same as Button's onClick
        self._onDateChangedCallback =action
