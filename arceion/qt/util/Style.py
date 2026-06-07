from typing import Any, Self

__all__ = ['Style']


class Style:
	"""
	Represents a styling utility for applying formatted stylesheets to widgets.

	This class provides functionality to dynamically manage and apply stylesheets
	to widgets by formatting predefined styles with arguments. It also allows
	creating updated instances with modified styles or arguments for further
	customizations.

	Methods:
		update(*args, **kwargs) -> Self: Creates and returns a deep copy of the current object with updated arguments and keyword arguments.
		apply(widget: Any, *args, **kwargs) -> None: Applies a formatted stylesheet to a widget's `setStyleSheet` method.

	Properties:
	    qss (str): A property representing the dynamically formatted and processed
	        stylesheet as a string.
	"""

	_styleSheet: str
	_args: tuple
	_kwargs: dict

	def __init__(self, styleSheet: str, *args, **kwargs):
		"""
		Initializes the instance with a specified stylesheet and optional arguments.

		Args:
		    styleSheet (str): A string representing the stylesheet to be used.
		    *args: Variable positional arguments to be passed.
		    **kwargs: Variable keyword arguments to be passed.
		"""

		self._args, self._kwargs = (), {}
		self._styleSheet = styleSheet
		self._args = args
		self._kwargs = kwargs

	def update(self, *args, **kwargs) -> Self:
		"""
		Creates and returns a deep copy of the current object with updated arguments and keyword arguments.

		This method generates an updated instance of the current class based on new arguments or keyword
		arguments passed. If no arguments are provided, it retains the current instance's attributes.

		Args:
		    *args: Optional positional arguments for the updated instance.
		    **kwargs: Optional keyword arguments for the updated instance.

		Returns:
		    Self: A deep copy of the current object with updated arguments and keyword arguments.
		"""

		deepCopy = self.__class__(self._styleSheet, *self._args, **self._kwargs)
		deepCopy._args = args if args else self._args
		deepCopy._kwargs = {**self._kwargs, **kwargs}
		return deepCopy

	def apply(self, widget: Any, *args, **kwargs) -> None:
		"""
		Applies a formatted stylesheet to a widget's `setStyleSheet` method.

		This method dynamically formats a predefined stylesheet using the provided
		arguments and applies it to the given widget. It ensures that the widget
		has the `setStyleSheet` method available before attempting to apply the
		stylesheet. The dynamic formatting replaces placeholders in the stylesheet
		while converting bracket symbols to curly braces.

		Args:
		    widget (Any): The widget to which the stylesheet will be applied. Must
		        support the `setStyleSheet` method.
		    *args: Positional arguments passed to format the stylesheet.
		    **kwargs: Keyword arguments passed to format the stylesheet.

		Raises:
		    AttributeError: If the provided widget does not have a `setStyleSheet`
		        method.

		"""

		if not hasattr(widget, 'setStyleSheet'):
			raise AttributeError(f'Widget {widget} does not have a setStyleSheet method')
		style = self._styleSheet.format(*args, *self._args, **kwargs, **self._kwargs)
		style = style.replace('[', '{').replace(']', '}')
		widget.setStyleSheet(style)

	@property
	def qss(self) -> str:
		"""
		A property that generates and returns a formatted style sheet as a string.

		Returns:
		    str: A formatted and processed style sheet string.
		"""

		style = self._styleSheet.format(*self._args, **self._kwargs)
		style = style.replace('[', '{').replace(']', '}')
		return style
