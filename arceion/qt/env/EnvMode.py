import enum

__all__ = ['EnvMode']


class EnvMode(enum.Enum):
	"""Enumeration for environment modes.

	Represents the operational modes of an application, typically used
	to distinguish between development and production environments.
	"""

	DEBUG = 'Debug'
	RELEASE = 'Release'
