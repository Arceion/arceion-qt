import enum

import requests

__all__ = ["Method"]


class Method(enum.Enum):
    """
    Enumeration of HTTP methods.

    This class represents an enumeration of commonly used HTTP methods, each
    associated with their respective string representation and the `requests` method
    used for making HTTP requests. It simplifies the handling of HTTP requests by
    associating the method type with the corresponding `requests` library function.

    Attributes:
        GET (tuple): Tuple containing the string representation 'GET' and the
            `requests.get` method for performing HTTP GET requests.
        POST (tuple): Tuple containing the string representation 'POST' and the
            `requests.post` method for performing HTTP POST requests.
        PUT (tuple): Tuple containing the string representation 'PUT' and the
            `requests.put` method for performing HTTP PUT requests.
        DELETE (tuple): Tuple containing the string representation 'DELETE' and the
            `requests.delete` method for performing HTTP DELETE requests.
        PATCH (tuple): Tuple containing the string representation 'PATCH' and the
            `requests.patch` method for performing HTTP PATCH requests.
        HEAD (tuple): Tuple containing the string representation 'HEAD' and the
            `requests.head` method for performing HTTP HEAD requests.
        OPTIONS (tuple): Tuple containing the string representation 'OPTIONS' and the
            `requests.options` method for performing HTTP OPTIONS requests.
    """

    GET = ("GET", requests.get)
    POST = ("POST", requests.post)
    PUT = ("PUT", requests.put)
    DELETE = ("DELETE", requests.delete)
    PATCH = ("PATCH", requests.patch)
    HEAD = ("HEAD", requests.head)
    OPTIONS = ("OPTIONS", requests.options)
