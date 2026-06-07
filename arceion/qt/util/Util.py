import os
import sys

from arceion.qt.logger import Logger

__all__ = ['Util']


class Util:
	"""
	Utility class offering methods for directory management and utility operations.

	This class provides methods to create directories with specific attributes and
	permissions, as well as a utility function to retrieve the first non-None value
	from a list of arguments.

	Attributes:
		MK_DIR_NORMAL_MODE (int): The default mode for directory creation, typically
			with full permissions (0o777).
		MK_DIR_UAC_MODE (int): The UAC (User Account Control) mode for directory
			creation, typically limiting permissions (0o700).

	Methods:
		mkSecretDir(path: str, mode: int = MK_DIR_NORMAL_MODE) -> bool: Creates a directory with secret (hidden) attributes.
		mkDir(path: str, mode: int = MK_DIR_NORMAL_MODE): Creates a directory at the specified path.
		either(*args, default=None): Returns the first non-None value from the provided arguments.
	"""

	MK_DIR_NORMAL_MODE: int = 0o777
	MK_DIR_UAC_MODE: int = 0o700

	@classmethod
	def mkSecretDir(cls, path: str, mode: int = MK_DIR_NORMAL_MODE) -> bool:
		"""
		Creates a directory with secret (hidden) attributes applied.

		This method utilizes the `mkDir` method to create a directory and applies hidden
		attributes if the operating system is Windows. For non-Windows platforms, the
		directory is created without additional file attributes.

		Args:
			path (str): The path where the directory should be created.
			mode (int): The mode to apply to the directory creation process, with a default
				of MK_DIR_NORMAL_MODE.

		Returns:
			bool: True if the operation succeeded. On Windows, ensures that the hidden attribute
				is applied to the directory.
		"""

		cls.mkDir(path, mode)
		if sys.platform == 'win32':
			from ctypes import windll
			return windll.kernel32.SetFileAttributesW(path, 0x02)  # type: ignore
		return True

	@classmethod
	def mkDir(cls, path: str, mode: int = MK_DIR_NORMAL_MODE):
		"""
		Creates a directory at the specified path.

		This method ensures that all intermediate directories in the given path are
		created, if they do not already exist. It uses the specified mode to create
		the directory. If the directory already exists, a warning is logged. If an
		unexpected error occurs, it logs an error message and exits the program.

		Args:
			path (str): The full path of the directory to create.
			mode (int): The mode (permissions) to use when creating the directory.
				Defaults to MK_DIR_NORMAL_MODE.

		Raises:
			FileNotFoundError: Logs an error message and exits the program if the
				specified folder path cannot be created due to missing parent components.
			FileExistsError: Logs a warning message if the specified directory already
				exists but does not interrupt the process.
		"""

		try:
			path = path.replace('/', '\\') if '/' in path else path
			container = '\\'.join(path.split('\\')[:-1])
			if not os.path.exists(container):
				cls.mkDir(container, mode)
			os.mkdir(path, mode)
		except FileNotFoundError:
			Logger.error(f'Unexpected error, Failed to create {path} folder')
			exit(-1)
		except FileExistsError:
			Logger.warning(f'{path} folder already exists')

	@classmethod
	def either(cls, *args, default=None):
		"""
		Return the first non-None value from the provided arguments.

		This method iterates through the given arguments and returns the first
		non-None value it encounters. If all provided arguments are None, the
		method returns the specified default value.

		Args:
			*args: Variable length argument list that will be checked.
			default: The value to return if all arguments are None.

		Returns:
			Any: The first non-None value found among the arguments, or the
			default value if none are found.
		"""

		for arg in args:
			if arg is not None:
				return arg
		return default
