from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QScrollArea

__all__ = ['ScrollArea']


class ScrollArea(QScrollArea):
	"""
	Custom QScrollArea subclass to provide additional functionality.

	This class extends the QScrollArea to add capabilities for monitoring and responding
	to changes in the visibility state of its scroll bars. It emits custom signals
	when the visibility state of the vertical or horizontal scroll bars changes.

	Attributes:
	    resized (pyqtSignal): Signal emitted when the scroll area is resized.
	    verticalScrollBarStateChanged (pyqtSignal): Signal emitted when the visibility state
	        of the vertical scroll bar changes. Emits a bool indicating the new state.
	    horizontalScrollBarStateChanged (pyqtSignal): Signal emitted when the visibility state
	        of the horizontal scroll bar changes. Emits a bool indicating the new state.
	    verticalScrollBarLastState (bool): Stores the last known visibility state of the vertical
	        scroll bar. Defaults to True.
	    horizontalScrollBarLastState (bool): Stores the last known visibility state of the horizontal
	        scroll bar. Defaults to True.
	"""

	resized: pyqtSignal = pyqtSignal()
	verticalScrollBarStateChanged: pyqtSignal = pyqtSignal(bool)
	horizontalScrollBarStateChanged: pyqtSignal = pyqtSignal(bool)

	verticalScrollBarLastState: bool = True
	horizontalScrollBarLastState: bool = True

	def resizeEvent(self, a0):
		"""
		Handles the resize event for the widget.

		This method overrides the parent class's `resizeEvent` method and checks the
		state of both the vertical and horizontal scroll bars after the resize action
		is performed.

		Args:
		    a0: The resize event object containing information about the resize event.
		"""

		super().resizeEvent(a0)
		self.checkVerticalScrollBarState()
		self.checkHorizontalScrollBarState()

	def checkVerticalScrollBarState(self):
		"""
		Checks the visibility state of the vertical scroll bar and emits a state change signal if the state
		has changed since the last check.

		This method monitors the visibility of the vertical scroll bar associated with the object. If the
		current visibility state differs from the previously recorded state, it updates the internal state
		and emits the `verticalScrollBarStateChanged` signal with the new state.

		Raises:
		    None
		"""

		verticalScrollBarState = self.verticalScrollBar().isVisible()
		if self.verticalScrollBarLastState != verticalScrollBarState:
			self.verticalScrollBarLastState = verticalScrollBarState
			self.verticalScrollBarStateChanged.emit(verticalScrollBarState)

	def checkHorizontalScrollBarState(self):
		"""
		Checks the state of the horizontal scroll bar and emits a signal if its state changes.

		This method determines whether the horizontal scroll bar is currently visible and compares this
		state with the previously stored state. If there is a change in state, it updates the stored state
		and emits the `horizontalScrollBarStateChanged` signal with the new state.

		Raises:
		    Emits a signal `horizontalScrollBarStateChanged` with the current visibility status
		    of the horizontal scroll bar when its state changes.
		"""

		horizontalScrollBarState = self.horizontalScrollBar().isVisible()
		if self.horizontalScrollBarLastState != horizontalScrollBarState:
			self.horizontalScrollBarLastState = horizontalScrollBarState
			self.horizontalScrollBarStateChanged.emit(horizontalScrollBarState)
