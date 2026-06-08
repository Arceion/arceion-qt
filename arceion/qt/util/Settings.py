import os.path
from os import environ
from sys import platform
from typing import Any

from cryptography.fernet import Fernet

from arceion.qt.logger import Logger

from .Util import Util

__all__ = ["Settings"]

_ROOT = environ.get("BASE_PATH", None)
_APP = environ.get("APP_NAME", None)
_APP_PATH = f"{environ.get('LOCALAPPDATA')}\\{_APP}"
_APP_FOLDER = "arceion"  # noqa: S105
_SECRET_PATH = f"{_APP_PATH}/.{_APP_FOLDER}"

if not os.path.exists(_SECRET_PATH):
    if platform in ("win32", "win64"):
        Util.mkSecretDir(_SECRET_PATH, Util.MK_DIR_UAC_MODE)
    if platform == "win32":
        Util.mkSecretDir(_APP_PATH, Util.MK_DIR_UAC_MODE)
    # TODO: Handle Mac OS and Linux platforms


class Settings:
    """
    Represents application settings secured through encryption.

    This class provides functionality to securely store, retrieve, and remove settings or configuration data.
    It employs encryption to ensure that sensitive information remains protected when persisted to disk.
    The settings are stored as files, with the filenames acting as identifiers for the associated values.

    Methods:
            set(key: str, value: str): Encrypts and saves a value associated with a key.
            remove(key: str): Deletes the file associated with a key.
            get(key: str, default: str | None = None): Retrieves and decrypts the value associated with a key.
    """

    _KEY = environ.get("SECRET_KEY", None)
    _CIPHER = Fernet(_KEY.encode()) if _KEY else Fernet.generate_key()

    @classmethod
    def set(cls, key: str, value: str):
        """
        Encrypts a given value and saves it to a specified file.

        This method takes a key and a value as input, encrypts the value using a cipher,
        and writes the encrypted result to a file named after the provided key. If the
        specified file path is not found, the method logs an error and terminates the
        program.

        Args:
                key (str): The name of the file (without extension) where the encrypted
                        value will be stored. This acts as an identifier for the value.
                value (str): The plain text string to be encrypted and saved.

        Raises:
                FileNotFoundError: If the file path where the encrypted value is to be
                        stored does not exist, an error is logged, and the program terminates.
        """

        try:
            encrypted_value = cls._CIPHER.encrypt(value.encode())
            with open(f"{_SECRET_PATH}/{key}.txt", "wb") as file:
                file.write(encrypted_value)
        except FileNotFoundError:
            Logger.error("Unable locate settings containing file, try rerunning the application.")
            exit(-1)

    @classmethod
    def remove(cls, key: str):
        """
        Removes a file associated with the given key from a predefined directory.

        This method attempts to delete a file specified by the key parameter from a
        defined directory. If the file does not exist, it logs an error message
        indicating the issue.

        Args:
                key (str): The name of the file (without extension) to be removed.
        """

        try:
            os.remove(f"{_SECRET_PATH}/{key}.txt")
        except FileNotFoundError:
            Logger.error("Unable locate settings containing file, try rerunning the application.")

    @classmethod
    def get(cls, key: str, default: Any = None):
        """
        Retrieves a decrypted value associated with the given key.

        This method fetches an encrypted value from a file named after the key, decrypts
        it, and returns the plain text value. If the file is not found, a warning is
        logged, and the optional default value is returned instead.

        Args:
                key (str): The identifier for the file containing the encrypted value.
                default (Any): The value to return if the file for the given key is
                        not found. Defaults to None.

        Returns:
                str | None: The decrypted value from the file if found, otherwise the
                given default value or None.
        """

        try:
            with open(f"{_SECRET_PATH}/{key}.txt", "rb") as file:
                encrypted_value = file.read()
            decrypted_value = cls._CIPHER.decrypt(encrypted_value).decode()
            return decrypted_value
        except FileNotFoundError:
            Logger.warning(
                f"Unable find the file containing the key {key}, Make sure you have set 'BASE_PATH' and "
                f"'APP_NAME' environment variables."
            )
            return default
