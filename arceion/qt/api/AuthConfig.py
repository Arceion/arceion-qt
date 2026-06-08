import dataclasses

from .Method import Method

__all__ = ["AuthConfig"]


@dataclasses.dataclass
class AuthConfig:
    """
    Configuration for authentication mechanisms.

    This class is used to define the configuration settings for handling
    authentication, such as refreshing tokens using specified endpoints,
    methods, and keys.

    Attributes:
        refreshEndpoint (str | None): The endpoint URL where token refresh
            requests will be sent. If None, token refreshing will be disabled.
        refreshUrl (str | None): The base URL for the token refresh process.
            It can be combined with endpoint paths for a full configuration.
            If None, no specific URL will be associated for token refresh.
        refreshReturnTokenKey (str): The key under which the refreshed token
            will be returned in the response payload. Defaults to 'access'.
        refreshMethod (Method): The HTTP method used for token refresh
            requests. Defaults to Method.POST.
    """

    refreshEndpoint: str | None = None
    refreshUrl: str | None = None
    refreshReturnTokenKey: str = "access"
    refreshMethod: Method = Method.POST
