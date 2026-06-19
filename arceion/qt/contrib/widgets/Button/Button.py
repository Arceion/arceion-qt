from typing import Callable, Optional

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QSizePolicy, QToolButton

from arceion.qt.util import UI, Style
from arceion.qt.contrib.styles.Button import defaultButton
from arceion.qt.contrib.widgets.Attr import Padding
__all__ = ['Button']


class Button(QToolButton):
	_onPressCallback: Optional[Callable] = None
	_style: Style = defaultButton

	def __init__(
		self,
		text: str = '',
		tooltip: str = '',
		icon: Optional[QIcon] = None,
		iconSize: Optional[QSize] = None,
		padding: Optional[Padding] = None,
		style: Qt.ToolButtonStyle = Qt.ToolButtonStyle.ToolButtonFollowStyle,
		direction: Qt.LayoutDirection = Qt.LayoutDirection.LeftToRight,
		onClick: Optional[Callable] = None,
	):
		super().__init__()

		# Store attributes
		self._text = text
		self._tooltip = tooltip
		self._icon = icon
		self._iconSize = iconSize if iconSize else QSize(UI.dp(16), UI.dp(16))
		self._padding = padding if padding else Padding(0)
		self._style = style
		self._direction = direction

		# Initialize button
		self.setCursor(Qt.CursorShape.PointingHandCursor)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
		self.setContentsMargins(self._padding)

		# Update button properties
		self.updateTextAndIcon()

		# Connect click handler if provided
		if onClick:
			self.onClick(onClick)

	def updateTextAndIcon(self):
		"""Update button text, icon, style, and direction."""
		if self._tooltip:
			self.setToolTip(self._tooltip)

		# Set tool button style based on icon and text presence
		if self._icon and self._text:
			self.setToolButtonStyle(self._style if self._style else Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
		elif self._icon:
			self.setToolButtonStyle(self._style if self._style else Qt.ToolButtonStyle.ToolButtonIconOnly)
		elif self._text:
			self.setToolButtonStyle(self._style if self._style else Qt.ToolButtonStyle.ToolButtonTextOnly)

		# Set layout direction
		self.setLayoutDirection(self._direction)

		# Set icon and text
		if self._icon:
			super().setIcon(self._icon)
			super().setIconSize(self._iconSize)
		if self._text:
			super().setText(self._text)

		# Adjust size
		self.adjustSize()

	def setText(self, text: str):
		"""Set the button text and update the UI."""
		self._text = text
		self.updateTextAndIcon()

	def setToolTip(self, tooltip: str):
		"""Set the button tooltip and update the UI."""
		self._tooltip = tooltip
		super().setToolTip(tooltip)

	def setIcon(self, icon: QIcon, iconSize: Optional[QSize] = None):
		"""Set the button icon and optional icon size."""
		self._icon = icon
		if iconSize:
			self._iconSize = iconSize
		self.updateTextAndIcon()

	def setIconSize(self, iconSize: QSize):
		"""Set the icon size and update the UI."""
		self._iconSize = iconSize
		self.updateTextAndIcon()

	def setPadding(self, padding: Padding):
		"""Set the padding for the button."""
		self._padding = padding
		self.setContentsMargins(padding)
		self.adjustSize()

	def setStyle(self, style: Qt.ToolButtonStyle):
		"""Set the button style and update the UI."""
		self._style = style
		self.updateTextAndIcon()

	def setDirection(self, direction: Qt.LayoutDirection):
		"""Set the layout direction and update the UI."""
		self._direction = direction
		self.setLayoutDirection(direction)
		self.updateTextAndIcon()

	def onClick(self, action: Callable):
		"""Connect a click handler to the button."""
		self.clicked.connect(action)

	def onPress(self, action: Callable):
		self._onPressCallback = action

	def mousePressEvent(self, a0):
		if self._onPressCallback:
			self._onPressCallback(a0)
		else:
			self.clicked.emit()

	def sizeHint(self):
		"""Provide a custom size hint based on the icon size and padding."""
		base_size = super().sizeHint()
		return QSize(
			base_size.width() + self._padding.totalHorizontal(),
			max(base_size.height(), self._iconSize.height() + self._padding.totalVertical()),
		)