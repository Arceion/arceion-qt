import inspect
import logging
import os

__all__ = ["Logger", "LoggerManager"]

from typing import ClassVar

log = logging.getLogger("Logger")
logging.basicConfig(
    format="%(asctime)s [%(filename)s:%(lineno)d] %(levelname)s: %(message)s",
    level=logging.DEBUG,
)


class LoggerManager:
    """
    Logger class for logging messages

    Description:
            This is a logger class for logging messages. This class is used to log messages in the application. This class
            provides the basic structure for logging messages. This class provides the basic structure for logging
            messages.

    Attributes:
            _userName: str = NotImplemented
            _level: int | str = logging.DEBUG
            _format: str = '%(asctime)s %(message)s'
            _messageConfig: Dict[str, str] = dict()
            _messageFormat: str = '[{filename}' + ':' + '{lineno}] {level}' + ':' + ' | {userName} - {msg}'

    Methods:
            setUserName(self, userName: str) -> None
            setConfig(self, config: Dict[str, str]) -> None
            setLevel(self, level: int | str) -> None
            setFormat(self, logFormat: str) -> None
            setDestination(self, filePath: str)
            formatMsg(self, msg: str, level: str) -> str
            debug(self, msg, *args, **kwargs) -> None
            info(self, msg, *args, **kwargs) -> None
            critical(self, msg, *args, **kwargs) -> None
            warning(self, msg, *args, **kwargs) -> None
            error(self, msg, *args, **kwargs) -> None
    """

    _userName: str = NotImplemented
    _level: int | str = logging.DEBUG
    _format: str = "%(asctime)s %(message)s"
    _messageConfig: ClassVar[dict[str, str]] = {}
    _messageFormat: str = "[{filename}" + ":" + "{lineno}] {level}" + ":" + " | {userName} - {msg}"

    def setUserName(self, userName: str) -> None:
        """
        setUserName(self, userName: str) -> None
        :param userName: User name to be set
        :return: None
        """
        self._userName = userName

    def setConfig(self, config: dict[str, str]) -> None:
        """
        setConfig(self, config: Dict[str, str]) -> None
        :param config: Configuration to be set
        :return: None
        """
        self._messageConfig = config

    def setLevel(self, level: int | str) -> None:
        """
        setLevel(self, level: int | str) -> None
        :param level: Level to be set
        :return: None
        """
        self._level = level
        log.setLevel(level)

    def setFormat(self, logFormat: str) -> None:
        """
        setFormat(self, logFormat: str) -> None
        :param logFormat: Format to be set
        :return: None
        """
        self._format = logFormat

    def setDestination(self, filePath: str):
        """
        setDestination(self, filePath: str)
        :param filePath: File path to set the destination
        :return: None
        """
        file_handler = logging.FileHandler(filePath)
        file_handler.setLevel(self._level)
        formatter = logging.Formatter(self._format)
        file_handler.setFormatter(formatter)
        log.addHandler(file_handler)

    def formatMsg(self, msg: str, level: str) -> str:
        """
        formatMsg(self, msg: str, level: str) -> str
        :param msg: Message to be formatted
        :param level: Level of the message
        :return: Formatted message
        """
        frame = inspect.stack()[5 if len(inspect.stack()) > 5 else len(inspect.stack()) - 1]
        filename = os.path.basename(frame.filename)
        lineno = frame.lineno
        return self._messageFormat.format(
            filename=filename,
            lineno=lineno,
            level=level.upper(),
            userName=self._userName if self._userName is not NotImplemented else "",
            msg=msg,
            **self._messageConfig,
        )

    def debug(self, msg, **kwargs) -> None:
        """
        debug method for logging debug messages
        :param msg: Message to be logged
        :param kwargs: Keyword arguments
        :return: None
        """
        log.debug(self.formatMsg(msg, "debug"), **kwargs)

    def info(self, msg, **kwargs) -> None:
        """
        info method for logging info messages
        :param msg: Message to be logged
        :param kwargs: Keyword arguments
        :return: None
        """
        try:
            log.info(self.formatMsg(str(msg), "info"), **kwargs)
        except UnicodeEncodeError:
            log.info(self.formatMsg(str(msg.encode("utf-8")), "info"), **kwargs)

    def critical(self, msg, **kwargs) -> None:
        """
        critical method for logging critical messages
        :param msg: Message to be logged
        :param kwargs: Keyword arguments
        :return: None
        """
        log.critical(self.formatMsg(msg, "critical"), **kwargs)

    def warning(self, msg, **kwargs) -> None:
        """
        warning method for logging warning messages
        :param msg: Message to be logged
        :param kwargs: Keyword arguments
        :return: None
        """
        log.warning(self.formatMsg(msg, "warning"), **kwargs)

    def error(self, msg, **kwargs) -> None:
        """
        error method for logging error messages
        :param msg: Message to be logged
        :param kwargs: Keyword arguments
        :return: None
        """
        log.error(self.formatMsg(msg, "error"), **kwargs)


Logger = LoggerManager()
