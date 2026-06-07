import dataclasses
from typing import Any

import requests

__all__ = ['Result']


@dataclasses.dataclass
class Result:
    """
    Represents the result of an operation.

    This class encapsulates the result of an operation, providing information
    about the success or failure of the operation, along with any associated
    details such as status code, server response, or error messages.

    Attributes:
        status (bool): Indicates whether the operation was successful or not.
        res (requests.Response | None): The server response object, if available.
        status_code (int | None): The HTTP status code of the response, if applicable.
        json (Any | None): The JSON payload from the response, if available.
        message (str | None): A descriptive message about the result of the operation.
        error (dict | None): A dictionary containing details about any error that occurred.

    Methods:
        getErrorMessage(self, default: str = '') -> str: Returns the error message if available,
            otherwise returns a default message.
    """

    status: bool
    res: requests.Response | None = None
    status_code: int | None = None
    json: Any | None = None
    message: str | None = None
    error: dict | None = None

    def getErrorMessage(self, default: str = ''):
        if isinstance(self.error, list) and len(self.error) > 0 and isinstance(self.error[0], str):
            return self.error[0]
        return self.error.get('details', default)
