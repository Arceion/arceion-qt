from typing import Generic, Self, TypeVar

from .Style import Style

__all__ = ['StyleSheet']

T = TypeVar('T', bound='StyleSheet')


class StyleSheet(Generic[T]):
	def __init__(self, **kwargs: dict[str, Style]) -> None:
		"""
		Initializes a class with dynamically assigned attributes based on the provided keyword arguments.

		Each keyword argument corresponds to an attribute of the class. The value for each keyword
		argument must be an instance of the `Style` type. If a value provided for a keyword argument
		is not of the `Style` type, a `TypeError` is raised.

		Args:
		    **kwargs (Dict[str, Style]): Arbitrary keyword arguments where the key serves as the
		        attribute name, and the value must be an instance of `Style`.

		Raises:
		    TypeError: If any provided value is not an instance of `Style`.
		"""

		for key, value in kwargs.items():
			if not isinstance(value, Style):
				raise TypeError(f"Invalid type, expected 'Style', got {type(value).__name__}")
			setattr(self, key, value)

	def update(self, **kwargs) -> Self:
		"""
		Updates attributes of the object with the specified keyword arguments.

		The method iterates over the provided keyword arguments, and for each key-value pair,
		it checks whether the object has an attribute matching the key. If the attribute exists
		and the value is of the correct type `Style`, the attribute is updated with the given value.

		Raises:
		    KeyError: If an attribute specified in the keyword arguments does not exist in the object.
		    TypeError: If the value provided for an attribute is not of type `Style`.

		Args:
		    **kwargs: Keyword arguments where the key represents the attribute to be updated, and the
		        value must be of type `Style`.

		Returns:
			Self: Returns the updated instance of the object.
		"""

		for key, value in kwargs.items():
			if not hasattr(self, key):
				raise KeyError(f'{key} attribute not found')
			if not isinstance(value, Style):
				raise TypeError(f"Invalid type, expected 'Style', got {type(value).__name__}")
			setattr(self, key, value)
		return self
