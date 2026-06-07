from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget

from arceion.qt.contrib.widgets.Attr import Margin

from .Widget import Widget

__all__ = ['VBoxWidget']


class VBoxWidget(Widget):
	"""
	VBoxWidget(parent: QWidget | type[QWidget] | None = None, spacing: int = 0, margin: Margin | None = None,
	alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft, **kwargs)

	Manages vertical layout and widget arrangement with customizable spacing, margin,
	and alignment options.

	The VBoxWidget class is designed as a specialized layout manager for arranging
	child widgets in a vertical orientation. It allows for extensive customization
	regarding the spacing between widgets, the layout's margins, and alignment of
	contained elements. This class can be utilized as a layout for GUI
	development where vertical widget placement is essential.
	"""

	def __init__(
		self,
		parent: type[QWidget] | QWidget | None = None,
		spacing: int = 0,
		margin: Margin | None = None,
		alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft,
		**kwargs,
	):
		"""
		Initializes an instance of the specified class with layout properties and options.

		Args:
		    parent (QWidget | type[QWidget] | None): The parent widget reference. Defaults to None.
		    spacing (int): The spacing between child widgets. Defaults to 0.
		    margin (Margin | None): The layout margin settings. Defaults to None.
		    alignment (Qt.AlignmentFlag): Alignment flag for layout positioning. Defaults to
		        Qt.AlignmentFlag.AlignLeft.
		    **kwargs: Additional keyword arguments to be passed to the super constructor.
		"""

		super().__init__(
			parent=parent, spacing=spacing, margin=margin, alignment=alignment, **kwargs,
		)

