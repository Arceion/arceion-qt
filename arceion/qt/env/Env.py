import os

from .EnvMode import EnvMode

__all__ = ['Env']


class Env:
	def __init__(self, mode: EnvMode, **kwargs):
		"""
		Initializes an instance of the class with the provided mode and additional
		keyword arguments. The mode determines whether the instance is in debug
		mode, and additional attributes are dynamically added from the provided
		keyword arguments.

		Args:
		    mode: Specifies the mode of the instance. Determines whether the instance
		        is in debug mode.
		    **kwargs: Arbitrary keyword arguments that are dynamically added as
		        instance attributes.
		"""

		self.mode = mode
		self.debug = mode == EnvMode.DEBUG

		self.__dict__.update(kwargs)

	def set(self, key: str, value):
		"""
		Sets an attribute to the instance and defines a corresponding environment variable.

		This method dynamically sets an attribute on the current instance with the
		specified key and value. Additionally, it sets the key-value pair as an
		environment variable in the operating system's environment. If the key
		already exists in the environment, its value will not be overwritten.

		Args:
		    key (str): The name of the attribute and environment variable to be set.
		    value: The value to assign to the attribute and the environment variable.
		"""

		setattr(self, key, value)
		os.environ.setdefault(key, value)

	def get(self, key: str):
		"""
		Retrieves the value of an attribute by its name.

		This method is used to dynamically access the value of an attribute
		from the object using the attribute's name as a string.

		Args:
		    key (str): The name of the attribute to retrieve.

		Returns:
		    Any: The value of the requested attribute.

		Raises:
		    AttributeError: If the attribute with the specified name does not exist on
		    the object.
		"""

		return getattr(self, key)

	def init(self):
		"""
		Sets environment variables based on the attributes of the instance.

		This method iterates through all the attributes of the instance. Depending
		on the type of the attribute value, it sets a corresponding environment variable
		using `os.environ.setdefault`. For string values, the environment variable
		is set directly. For boolean values, the boolean is converted to its string
		representation in lowercase. For all other value types, the string representation
		of the value is used.

		Raises:
		    None
		"""

		for key, value in self.__dict__.items():
			if isinstance(value, str):
				os.environ.setdefault(key, value)
			elif isinstance(value, bool):
				os.environ.setdefault(key, str(value).lower())
			else:
				os.environ.setdefault(key, str(value))
