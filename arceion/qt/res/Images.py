import os
from enum import Enum

__all__ = ['Images']


class Images:
	"""
	Images class to manage image paths based on themes and defaults.
	This class allows setting and retrieving image paths based on the current theme
	and a default theme. It raises errors if images are not found in the specified themes.

	Methods:
		setBase(self, base: str): Sets the base directory for images.
		getBase(self) -> str: Gets the base directory for images.
		setTheme(self, theme: Enum): Sets the current theme for images.
		getTheme(self) -> Enum: Gets the current theme for images.
		setDefaultTheme(self, default: Enum): Sets the default theme for images.
		getDefaultTheme(self) -> Enum: Gets the default theme for images.

	Raises:
		ValueError: If an invalid image name is provided.
		TypeError: If theme or default is not an instance of Enum.
		AttributeError: If the requested image is not defined.
		FileNotFoundError: If the image file does not exist in the specified themes.

	Usage:
		>>> from enum import Enum
		>>> class Theme(Enum):
		...     LIGHT = 'light'
		...     DARK = 'dark'
		>>> images = Images(theme=Theme.DARK, default=Theme.LIGHT, helody='helody.png')
		>>> print(images.helody)  # Should print the path to the helody.png image in the light theme
		>>> print(images.some_non_existent_image)  # Raises FileNotFoundError
	"""

	_base ='res/images/'
	_theme: Enum = NotImplemented
	_default: Enum = NotImplemented
	_backup: dict[str, str]
	_attributes = (
		'_base', '_theme', '_default', '_backup', 'setBase', 'getBase', 'setTheme', 'getTheme', 'setDefaultTheme',
		'getDefaultTheme',
	)

	def __setattr__(self, key, value) -> None:
		"""
		Sets the value of an attribute for the object. Ensures the attribute name is a valid Python identifier
		and updates the backup storage with the new value. Overrides the attribute if it is a valid and
		existing key.

		Args:
			key (str): The name of the attribute to be set. Must be a valid Python identifier.
			value (Any): The value to assign to the attribute.

		Raises:
			ValueError: If the provided `key` is not a string or is not a valid Python identifier.
		"""

		if not isinstance(key, str) or not key.isidentifier():
			raise ValueError(f'Invalid image name: {key}')
		if key in self._attributes:
			super().__setattr__(key, value)
			return
		self._backup[key] = str(value)

	def __init__(
		self, base: str = _base, theme: Enum = NotImplemented, default: Enum = NotImplemented, **kwargs,
	) -> None:
		"""
		Initializes the instance with the given base, theme, default values, and any additional keyword
		arguments. Ensures that the theme and default are instances of the Enum type.

		Args:
			base: String value representing the base configuration.
			theme: Enum representing the chosen theme configuration. Must be an instance of Enum.
			default: Enum representing the default configuration. Must be an instance of Enum.
			**kwargs: Additional keyword arguments that can be dynamically attached as attributes.

		Raises:
			TypeError: If 'theme' is not an instance of Enum.
			TypeError: If 'default' is not an instance of Enum.
		"""

		self._backup = {}
		self._base = base
		if not isinstance(theme, Enum):
			raise TypeError(f'Theme must be an instance of Enum, got {type(theme)}')
		self._theme = theme
		if not isinstance(default, Enum):
			raise TypeError(f'Default must be an instance of Enum, got {type(default)}')
		self._default = default

		for key, value in kwargs.items():
			setattr(self, key, value)

	def __getattribute__(self, item):
		"""
		Retrieves the value of an attribute. If the attribute is part of `_attributes`, it is directly retrieved.
		If the attribute corresponds to a file path, checks paths based on theme and default settings.

		Args:
			item: The name of the attribute to retrieve.

		Raises:
			AttributeError: If the attribute `item` is not defined in `_backup`.
			FileNotFoundError: If the corresponding file for `item` is not found in either the specified theme
				or the default theme.

		Returns:
			The value of the specified attribute if it exists or a valid file path if the attribute represents
			a file and its path exists.
		"""

		if item == '_attributes':
			return super().__getattribute__(item)
		if item in self._attributes:
			return super().__getattribute__(item)
		if item not in self._backup:
			raise AttributeError(f'{item} is not defined in the images')
		if os.path.exists(os.path.join(self._base, self._theme.value.lower(), self._backup[item])):
			return os.path.join(self._base, self._theme.value.lower(), self._backup[item])
		if os.path.exists(os.path.join(self._base, self._default.value.lower(), self._backup[item])):
			return os.path.join(self._base, self._default.value.lower(), self._backup[item])
		raise FileNotFoundError(f'Image {item} not found in theme {self._theme.value} or default {self._default.value}')

	def setBase(self, base: str) -> None:
		"""
		Sets the base attribute for the object.

		This method allows setting the value of the `_base` attribute to a new string
		value provided as an argument. It is used to update the state of the object with
		a new `base` value.

		Args:
			base (str): The new base value to be set.
		"""

		self._base = base

	def getBase(self) -> str:
		"""
		Retrieves the base value.

		This method returns the base value of the object, which is stored internally.
		It is intended to provide read-only access to this value.

		Returns:
			str: The base value stored in the object.
		"""

		return self._base

	def setTheme(self, theme: Enum) -> None:
		"""
		Sets the theme for the application. The theme must be an instance of the
		Enum class. This method updates the internal theme setting for the
		application with the provided value.

		Args:
			theme (Enum): The theme to be set. Must be an instance of the Enum
			class.

		Raises:
			TypeError: If the provided theme is not an instance of the Enum class.
		"""

		if not isinstance(theme, Enum):
			raise TypeError(f'Theme must be an instance of Enum, got {type(theme)}')
		self._theme = theme

	def getTheme(self) -> Enum:
		"""
		Retrieves the current theme.

		This method returns the current theme that is set for the application or
		context. The theme is represented as an Enum object.

		Returns:
			Enum: The current theme.
		"""

		return self._theme

	def setDefaultTheme(self, default: Enum) -> None:
		"""
		Sets the default theme for the application.

		This method allows the user to configure the default theme by providing an
		enumeration value representing the desired theme. An error is raised if
		the provided value is not an instance of Enum.

		Args:
			default (Enum): The enumeration value representing the default theme.

		Raises:
			TypeError: If the provided default value is not an instance of Enum.
		"""

		if not isinstance(default, Enum):
			raise TypeError(f'Default must be an instance of Enum, got {type(default)}')
		self._default = default

	def getDefaultTheme(self) -> Enum:
		"""
		Retrieves the default theme.

		This method retrieves the default theme from the internal state and
		returns it as an Enum value. The default theme represents the pre-set
		theme configuration for the system.

		Returns:
			Enum: The default theme configuration.
		"""

		return self._default
