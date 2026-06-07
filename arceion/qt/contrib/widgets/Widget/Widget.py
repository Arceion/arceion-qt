from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLayout, QVBoxLayout, QWidget

from arceion.qt.contrib.widgets.Attr import Margin

__all__ = ['Widget']


class Widget(QWidget):
	"""
	A widget class with a customizable layout for managing child widgets and layouts.

	This class provides a framework for organizing child widgets and layouts with
	a customizable alignment, margin, and spacing configuration. It extends QWidget
	to offer additional control over child widget arrangement. The primary functionality
	includes adding widgets, layouts, spacing, or stretchable areas to the internal layout
	manager. It also allows developers to retrieve the associated layout for advanced
	customization.

	Attributes:
	    parent (QWidget | None): The optional parent widget for this instance. If None, the
	        widget operates without a parent.

	Methods:
		addWidget(w: QWidget, **kwargs): Adds a widget to the layout.
		addLayout(layout: QLayout, **kwargs): Adds a new layout to the existing structure.
		addSpacing(spacing: int): Adds spacing to the layout.
		addStretch(stretch: int = 1): Adds a stretchable space to the layout.
		getLayout(): Returns the layout object associated with this instance.
	"""

	_layout: QLayout

	def __init__(
		self,
		parent: QWidget | None = None,
		layout: QLayout = QVBoxLayout,
		spacing: int = 0,
		margin: Margin | None = None,
		alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft,
		**kwargs,
	):
		"""
		Initializes an instance of the class with a customizable layout and configuration.

		Args:
		    parent (QWidget | None): The parent widget for this instance. If None, no parent is set.
		    layout (QLayout): The chosen layout manager for the instance. Defaults to QVBoxLayout.
		    spacing (int): The spacing between elements in the layout. Defaults to 0.
		    margin (Margin | None): The margins to set for the layout. If None, a default margin of zero is applied.
		    alignment (Qt.AlignmentFlag): The alignment of items within the layout. Defaults to Qt.AlignmentFlag.AlignLeft.
		    **kwargs: Additional keyword arguments to pass to the superclass initializer.
		"""

		super().__init__(parent, **kwargs)
		self.parent = parent

		self._layout = layout(self)
		self._layout.setSpacing(spacing)
		self._layout.setContentsMargins(margin if margin else Margin(0))
		self._layout.setAlignment(alignment)
		self.setStyleSheet('background-color: transparent')
		self.setLayout(self._layout)

	def addWidget(self, w: QWidget, **kwargs):
		"""
		Adds a widget to the internal layout.

		This method allows adding a given QWidget to the layout managed by the class.
		Additional properties of the widget can be specified using keyword arguments.

		Args:
		    w (QWidget): The widget to be added to the layout.
		    **kwargs: Additional keyword arguments that specify properties or behavior
		        of the widget being added.
		"""

		self._layout.addWidget(w, **kwargs)

	def addLayout(self, layout: QLayout, **kwargs):
		"""
		Adds a new QLayout instance to the existing layout.

		This method allows users to add a QLayout to the current layout structure
		with additional optional keyword arguments to customize the layout behavior.

		Args:
		    layout (QLayout): The layout to be added to the current structure.
		    **kwargs: Optional keyword arguments to configure the layout.
		"""

		self._layout.addLayout(layout, **kwargs)

	def addSpacing(self, spacing: int):
		"""
		Adds spacing to the layout.

		Inserts a non-interactive space of a specified size to the layout, enabling
		spacing adjustments between layout elements for better visual structure.

		Args:
		    spacing (int): The size of the spacing to be added to the layout, typically
		        measured in pixels.
		"""

		self._layout.addSpacing(spacing)

	def addStretch(self, stretch: int = 1):
		"""
		Adds a stretchable space to the layout, which can be used to control
		the positioning of widgets in the layout. The stretch factor determines
		how much space will be distributed among other stretches.

		Args:
		    stretch (int): The stretch factor to control the amount of space
		        allocated. Default is 1.
		"""

		self._layout.addStretch(stretch)

	def getLayout(self):
		"""
		Returns the layout object associated with this instance.

		This method retrieves the layout object that defines the structure
		or arrangement of components. It does not modify or alter any
		attributes of the instance.

		Returns:
		    Any: The layout object associated with this instance.
		"""

		return self._layout
