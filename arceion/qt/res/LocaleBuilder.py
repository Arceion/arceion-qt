import json
import os
from enum import Enum

__all__ = ['LocaleBuilder']


class LocaleBuilder:
	"""
	LocaleBuilder class to manage locale JSON files.
	This class allows setting and retrieving locale-specific strings from JSON files
	based on the current locale and a default locale. It raises errors if the JSON files
	are not found or if the locale is not an instance of Enum.

	Methods:
		setBase(self, base: str) -> None:
			Sets the base directory for locale JSON files.
		getBase(self) -> str:
			Returns the base directory for locale JSON files.
		setLocale(self, locale: Enum) -> None:
			Sets the current locale and loads its JSON file.
		getLocale(self) -> Enum:
			Returns the current locale.
		setDefaultLocale(self, default: Enum) -> None:
			Sets the default locale and loads its JSON file.
		getDefaultLocale(self) -> Enum:
			Returns the default locale.
		get(self, key: str) -> str:
			Retrieves a string from the current or default locale based on the key.

	Raises:
		TypeError: If the locale or default is not an instance of Enum.
		FileNotFoundError: If the JSON file for the locale or default locale does not exist.
		AttributeError: If the requested attribute is not defined in the locale JSON files.

	Usage:
	>>> from enum import Enum
	>>> class Locale(Enum):
	...     enUS = 'English (US)'
	...     siLK = 'Sinhala (LK)'
	>>> localeBuilder = LocaleBuilder(locale=Locale.siLK, default=Locale.enUS)
	>>> print(localeBuilder.hello_world)  # Example usage, assuming 'hello_world' is defined in the locale JSON files
	"""

	_base: str = 'res/locale'
	_locale: Enum = NotImplemented
	_default: Enum = NotImplemented
	_json: dict
	_defaultJson: dict
	_attributes = (
		'_base', '_locale', '_json', '_default', '_defaultJson', 'setLocale', 'getLocale', 'setDefaultLocale',
		'getDefaultLocale', 'get', 'setBase', 'getBase',
	)

	def __init__(self, base: str = _base, locale: Enum = NotImplemented, default: Enum = NotImplemented) -> None:
		"""
		Initializes the class with specified base path, locale, and default locale.

		Args:
			base: The base path to be used for the instance.
			locale: The locale to be used, must be an instance of Enum.
			default: The default locale to fall back on, must be an instance of Enum.

		Raises:
			TypeError: If the provided 'locale' is not an instance of Enum.
			TypeError: If the provided 'default' is not an instance of Enum.
		"""

		self._json, self._defaultJson = {}, {}
		if not isinstance(locale, Enum):
			raise TypeError(f'Locale must be an instance of Enum, got {type(locale)}')
		self._locale = locale
		if not isinstance(default, Enum):
			raise TypeError(f'Default must be an instance of Enum, got {type(default)}')
		self._default = default
		self.setBase(base)

	def setBase(self, base: str) -> None:
		"""
		Sets the base directory for the system and updates locale settings accordingly.

		Args:
			base: A string representing the path to the base directory.

		Raises:
			FileNotFoundError: If the specified base directory does not exist.
		"""

		if not os.path.exists(base):
			raise FileNotFoundError(f'Base directory {base} does not exist')
		self._base = base
		self.setLocale(self._locale)
		self.setDefaultLocale(self._default)

	def getBase(self) -> str:
		"""
		Retrieves the value of the base attribute.

		This method provides access to the internal `_base` attribute, returning
		its current value as a string.

		Returns:
			str: The current value of the `_base` attribute.
		"""

		return self._base

	def setLocale(self, locale: Enum) -> None:
		"""
		Sets the locale for the application and loads the corresponding JSON file.

		This method sets the locale using the provided `Enum` value and derives the
		path to the JSON file associated with that specific locale. If the file
		is not found at the derived path, a `FileNotFoundError` is raised. If
		the file exists, it is loaded and parsed as a JSON object.

		Args:
			locale (Enum): The locale to be set, represented as an Enum value.

		Raises:
			FileNotFoundError: If the JSON file corresponding to the specified
				locale is not found at the derived path.
		"""

		self._locale = locale
		localePath = f'{self._base}/{self._locale.name}.json'

		if not os.path.exists(localePath):
			raise FileNotFoundError(f'{localePath} not found')

		with open(localePath) as file:
			self._json = json.load(file)

	def getLocale(self) -> Enum:
		"""
		Retrieves the locale setting.

		This method returns the locale as an enumeration value, which represents the
		current locale setting of an object.

		Returns:
			Enum: The current locale setting of the object.
		"""

		return self._locale

	def setDefaultLocale(self, default: Enum) -> None:
		"""
		Sets the default locale for the application by loading the corresponding JSON file.

		The method assigns the specified locale as the default and attempts to load the
		associated JSON file. If the specified file is not found, a FileNotFoundError
		is raised.

		Args:
			default (Enum): The Enum value representing the default locale to be set.

		Raises:
			FileNotFoundError: If the JSON file corresponding to the specified default
				locale does not exist.

		"""

		self._default = default
		defaultPath = f'{self._base}/{self._default.name}.json'

		if not os.path.exists(defaultPath):
			raise FileNotFoundError(f'{defaultPath} not found')

		with open(defaultPath) as file:
			self._defaultJson = json.load(file)

	def getDefaultLocale(self) -> Enum:
		"""
		Retrieves the default locale setting.

		This method returns the default locale configuration stored within
		the class. The returned value is represented as an Enum type.

		Returns:
			Enum: The default locale setting.
		"""

		return self._default

	def get(self, key: str) -> str:
		"""
		Retrieves the value of an attribute by its name.

		This method fetches the value of the specified attribute from the
		object's properties based on the attribute name provided as input.
		If the attribute does not exist, it raises an AttributeError.

		Args:
			key (str): The name of the attribute to retrieve.

		Returns:
			str: The value of the requested attribute.

		Raises:
			AttributeError: If the attribute with the specified name does not exist.
		"""

		return getattr(self, key)

	def __getattribute__(self, item):
		"""
		Overrides the default behavior for attribute access in the class.
		This method checks for an attribute in the following order:
		1. Internal attributes list (`_attributes`).
		2. JSON-based definition (`_json`).
		3. Default JSON-based definition (`_defaultJson`).
		If the attribute is not found in any of these locations, an AttributeError is raised.

		Args:
			item: The name of the attribute being accessed.

		Returns:
			Any: The value associated with the requested attribute.

		Raises:
			AttributeError: If the requested attribute is not found in the available definitions.
		"""

		if item == '_attributes':
			return super().__getattribute__(item)
		if item in self._attributes:
			return super().__getattribute__(item)
		if item in self._json:
			return self._json[item]
		if item in self._defaultJson:
			return self._defaultJson[item]
		raise AttributeError(f'{item} is not defined in the locale')
