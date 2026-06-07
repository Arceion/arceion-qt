from datetime import datetime
from typing import Any, ClassVar, Generic, TypeVar

import pytz

from arceion.qt.exceptions import ParseError
from arceion.qt.logger import Logger
from arceion.qt.models.util import getAllAnnotations

__all__ = ['ModelAbstract']

T = TypeVar('T', bound='ModelAbstract')


class ModelAbstract(Generic[T]):
	"""
	A generic base class that supports dynamic attribute assignment with type conversion.

	This abstract base class provides functionality for dynamically setting attributes
	with type conversion based on specified type annotations. It includes utility methods
	for handling various data conversions, such as dates, optional types, lists, and dictionaries.
	This class is designed to facilitate the creation of models, ensuring attribute values
	adhere to the expected types.

	Methods:
		fromList(data: List) -> List: Creates a list of instances of the current class from a list of dictionaries.
		fromDict(data: dict): Creates a new instance of the class from a dictionary input.
		json() -> Any: Converts the object's attributes into a JSON-compatible dictionary.
	"""

	@classmethod
	def _convertInt(cls, value: Any) -> int:
		"""
		Converts a given value to an integer.

		This method converts the provided value to an integer by first
		casting it to a float, ensuring compatibility with floating-point numbers.
		It is an internal utility method and typically used for data normalization.

		Args:
		    value (Any): The value to be converted to an integer. It could be of any
		        type that supports casting to a float.

		Returns:
		    int: The integer representation of the provided value.
		"""
		return int(float(value))

	_dateFormat = '%Y-%m-%dT%H:%M:%S.%f%z'
	_dateFormats: ClassVar[list[str]] = [
		'%Y-%m-%d %H:%M:%S',
		'%Y-%m-%d %H:%M:%S.%f',
		'%Y-%m-%dT%H:%M:%S',
		'%Y-%m-%dT%H:%M:%S.%f',
		'%Y-%m-%d',
		'%Y-%m-%dT%H:%M:%S',
		'%Y-%m-%dT%H:%M:%S.%f%z',
		'%Y-%m-%dT%H:%M:%S%z',
	]
	_typeCasting: ClassVar[dict[str, type]] = dict(str=str, int=int, float=float, bool=bool)

	def __init__(self, **kwargs):
		"""
		Initializes an instance of the class and dynamically sets attributes with type conversion.

		Args:
		    **kwargs: A dictionary of attributes passed as keyword arguments. Keys are attribute names, and
		        values are their corresponding assigned values. The method dynamically assigns these values
		        to attributes of the instance after performing type conversion based on annotations.
		"""

		annotations = getAllAnnotations(self.__class__)
		for key, value in kwargs.items():
			if key in annotations:
				setattr(self, key, self._convert(value, annotations[key]))

	@classmethod
	def _convertDict(cls, value: Any, dateType: type) -> dict:
		"""
		Converts a dictionary's values to the specified type using recursive conversion.

		This method is intended to handle the conversion of a dictionary's values to
		the type specified in the given `dateType`, utilizing the `_convert` method
		for each value. The method verifies whether the `dateType` parameter contains
		type arguments and, if so, processes the dictionary accordingly.

		Args:
		    value: The input dictionary whose values need to be converted.
		    dateType: The type to which the dictionary values should be converted.

		Returns:
		    A dictionary with its values converted to the specified type.
		"""

		if not hasattr(dateType, '__args__'):
			return value
		return {
			key: cls._convert(item, dateType.__args__[1])
			for key, item in value.items()
		}

	@classmethod
	def _convertOptional(cls, value: Any, dateType: type) -> Any:
		"""
		Converts a value to a specified type if it is optional.

		Args:
		    value: The value to be converted. Can be of any type.
		    dateType: The target type to which the value should be converted.
		        Must specify a generic type with optional arguments.

		Returns:
		    The converted value matching the specified type, or None if the input
		    value is None.
		"""

		if value is None:
			return None
		if not hasattr(dateType, '__args__'):
			return value
		return cls._convert(value, dateType.__args__[0])

	@classmethod
	def _convertList(cls, value: Any, dateType: type) -> list:
		"""
		Converts a list of items to a desired type by recursively applying a conversion
		method to each item in the list.

		Args:
		    value: Input value expected to be a list containing items to convert.
		    dateType: The target type for the items in the list, including potential
		        type constraints for generic types.

		Returns:
		    A new list with each item converted to the specified type.
		"""

		return [
			cls._convert(
				item, (next(iter(dateType.__args__)) if hasattr(dateType, '__args__') else Any),
			) for item in value
		]

	@classmethod
	def _convertUnexpected(cls, value: Any, dateType: type) -> Any:
		"""
		Converts an unexpected value into the specified data type using a series of attempts.

		This method attempts to convert the given value into the specified data type by first
		invoking its constructor with the provided value directly. If that fails with a TypeError,
		it then attempts to apply the data type constructor by unpacking the value as positional
		arguments. Finally, if both previous attempts fail, it tries unpacking the value as keyword
		arguments. If none of these approaches succeed, the original behavior of the constructor
		determines the ultimate outcome.

		Args:
		    value: The input value to be converted. Can be of any type, depending on what the
		        specified data type expects.
		    dateType: The type or class into which the value should be converted.

		Returns:
		    Any: The resulting value converted into the specified data type.
		"""

		try:
			return dateType.__call__(value)
		except TypeError:
			pass
		try:
			return dateType.__call__(*value)
		except TypeError:
			pass
		return dateType.__call__(**value)

	@classmethod
	def _convertDate(cls, value: Any) -> datetime:
		"""
		Converts a date string or an object into a timezone-aware datetime object in UTC.

		The method attempts to handle multiple date format possibilities by iterating through
		the defined `_dateFormats` in the class. If no match is found using these formats, it
		then falls back to the default `_dateFormat`. For valid date strings with timezone
		information, it converts them to UTC. If no timezone is provided, it assumes UTC
		and localizes the datetime accordingly. In case conversion fails, the original
		value is returned.

		Args:
		    value (Any): An input value, which is expected to be a date string or an object.
		        If it's a string, it should follow one of the date formats defined in the
		        class.

		Returns:
		    Union[datetime, Any]: A timezone-aware datetime object in UTC if the conversion
		        succeeds. Otherwise, the original input value is returned.
		"""

		try:
			if value.endswith('Z'):
				value = value[:-1]
			convertedDate: datetime | None = None
			for dateFormat in cls._dateFormats:
				try:
					convertedDate = datetime.strptime(value, dateFormat)
				except ValueError:
					pass
			if convertedDate is None and isinstance(value, str):
				convertedDate = datetime.strptime(value, cls._dateFormat)
			if convertedDate.tzinfo is not None:
				return convertedDate.replace(tzinfo=pytz.timezone('UTC'))
			utc_timezone = pytz.utc
			parsed_date = utc_timezone.localize(convertedDate)
			return parsed_date
		except Exception as e:  # noqa: BLE001
			Logger.debug(f"{value} : {type(value)}\n {e}")
			return value


	@classmethod
	def _convert(cls, value: Any, dateType: type) -> Any:
		"""
		Converts a given value to the specified data type, handling various types such as datetime,
		optional types, lists, dictionaries, and custom types. Raises an error if the conversion fails or
		encounters unexpected types. Designed to support dynamic value parsing to ensure type conformity.

		Args:
		    value: The input value to be converted. The type of the input value may vary depending on
		        the expected data type specified by the `dateType` parameter.
		    dateType: The target type to which the `value` should be converted. It supports built-in
		        data types like int, list, and datetime, as well as complex types such as typing.Optional,
		        typing.List, and typing.Dict.

		Returns:
		    The input value successfully converted to the target data type, if the conversion is valid.

		Raises:
		    TypeError: Indicates that the value could not be converted to the specified data type due to
		        type mismatch or unsupported types.
		    ParseError: Contains additional information (line number and file path of the traceback)
		        when an error occurs during the conversion process. Thrown when a `TypeError`
		        is caught in the operation.

		"""

		try:
			if dateType is datetime:
				return cls._convertDate(value)
			if str(dateType).startswith('typing.Optional') or str(dateType).startswith('typing.Union'):
				return cls._convertOptional(value, dateType)
			if str(dateType).startswith('typing.List'):
				return cls._convertList(value, dateType)
			if str(dateType).startswith('typing.Dict'):
				return cls._convertDict(value, dateType)
			if str(dateType).startswith('typing.Any'):
				return value
			if dateType in cls._typeCasting.values():
				if dateType is int:
					return cls._convertInt(value)
				return cls._typeCasting[dateType.__name__](value)
			return cls._convertUnexpected(value, dateType)
		except TypeError as e:
			Logger.debug(f"{value} : {type(value)}\n {e}")
			line = 0
			column = NotImplemented
			if e.__traceback__ is not None:
				line = e.__traceback__.tb_lineno if hasattr(e.__traceback__, 'tb_lineno') else 0
				column = e.__traceback__.tb_frame.f_code.co_filename
			raise ParseError('Type Error', line, column) from e

	@classmethod
	def fromList(cls, data: list) -> list:
		"""
		Creates a list of instances of the current class from a list of dictionaries.

		Args:
		    data (List): A list of dictionaries, where each dictionary contains
		        initialization parameters for a single instance of the class.

		Returns:
		    List: A list of new instances of the class, based on the data provided.
		"""

		return [cls(**item) for item in data]

	@classmethod
	def fromDict(cls, data: dict):
		"""
		Creates a new instance of the class from a dictionary input.

		This method is a class method that takes a dictionary containing key-value
		pairs that map to the attributes of the class and creates an instance by
		passing those key-value pairs to the class constructor.

		Args:
		    data (dict): A dictionary where keys match the names of the class
		        attributes and their corresponding values are used to initialize
		        the class instance.

		Returns:
		    object: An instance of the class created using the provided dictionary data.
		"""

		return cls(**data)

	def _json(self, data):
		"""
		Converts various data types to their respective JSON-compatible representations. Specifically handles datetime
		objects, objects with a `json` method, lists containing either datetime objects or objects with a `json` method,
		and dictionaries with such objects as keys or values. Other data types are returned as-is.

		Args:
		    data: The input data to convert, which could be of any type such as datetime, list, dict, or an object with
		        a `json` method. Specific handling will depend on the input type.

		Returns:
		    The JSON-compatible representation of the input data, e.g. for `datetime` - a string, for an object with
		    a `json` method - the result of calling the `json` method, and so on.
		"""

		if isinstance(data, datetime):
			return data.strftime(self._dateFormat)
		if hasattr(data, 'json'):
			return data.json()
		if isinstance(data, list) and len(data) > 0 and hasattr(data[0], 'json'):
			return [item.json() for item in data]
		if isinstance(data, list) and len(data) > 0 and isinstance(data[0], datetime):
			return [item.strftime(self._dateFormat) for item in data]
		if isinstance(data, dict):
			return {
				self._json(k): self._json(v)
				for k, v in data.items()
			}
		return data

	def json(self) -> Any:
		"""
		Converts the object's attributes into a JSON-compatible dictionary.

		This method uses the internal `_json` method to serialize the object's
		dictionary (`__dict__`) into a JSON-compatible format.

		Returns:
		    Any: A JSON-compatible dictionary representation of the object.
		"""

		return self._json(self.__dict__)

	def __repr__(self):
		"""
		Returns a string representation of the object.

		This method provides a formatted string that represents the object instance,
		which includes the class name and the key-value pairs of its public attributes.

		Returns:
		    str: A detailed string representation of the object instance.
		"""

		return """{}(\n{}\n)""".format(
			self.__class__.__name__,
			'\n\t, '.join([
				f'{key}={value}'
				for key, value in self.__dict__.items()
			]),
		)

	def __str__(self):
		"""
		Converts the object to its string representation by calling the `__repr__` method.

		This method allows the object to be represented as a string in contexts where a
		string representation is required, such as when printing the object or when
		interpolating it into a string.

		Returns:
		    str: A string representation of the object as returned by the `__repr__`
		    method.
		"""

		return self.__repr__()
