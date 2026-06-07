import os

import requests
from icecream import ic

from arceion.qt.logger import Logger
from arceion.qt.util import Settings

from .AuthConfig import AuthConfig
from .Method import Method
from .Result import Result

__all__ = ['Controller']


class Controller:
	"""
	Represents a controller that handles API communication, URL generation, and token authentication.

	This class provides functionality to configure API connections, generate URLs, manage
	authentication tokens, and make various types of HTTP requests to specified endpoints.

	Attributes:
	    auth (AuthConfig): Configuration object for managing authentication-related settings.
	    api (str | None): The base URL of the API that is being communicated with. Can be None if
	        no API is configured.
	    service (str): The specific service name or path associated with the controller.
	    verbose (bool): Determines whether detailed logs and debug information should be printed
	        during execution.

	Methods:
		get(endpoint: str, params=None, authorized: bool = False) -> Any:
			Sends an HTTP GET request to the specified endpoint.
		post(endpoint: str, data=None, params=None, authorized: bool = False) -> Any:
			Sends an HTTP POST request to the specified endpoint.
		put(endpoint: str, data=None, params=None, authorized: bool = False) -> Any:
			Sends an HTTP PUT request to the specified endpoint.
		delete(endpoint: str, data=None, params=None, authorized: bool = False) -> Any:
			Sends an HTTP DELETE request to the specified endpoint.
		patch(endpoint: str, data=None, params=None, authorized: bool = False) -> Any:
			Sends an HTTP PATCH request to the specified endpoint.
		options(endpoint: str, data=None, params=None, authorized: bool = False) -> Any:
			Sends an HTTP OPTIONS request to the specified endpoint.
		head(endpoint: str, data=None, params=None, authorized: bool = False) -> Any:
			Sends an HTTP HEAD request to the specified endpoint.
	"""

	auth = AuthConfig('')
	api: str | None = os.environ.get('API', None)
	service: str = NotImplemented
	verbose: bool = False

	def __init__(self, service: str = '', api: str | None = None, verbose: bool = False):
		"""
		Initializes an instance with the specified service, API, and verbosity settings.

		Args:
		    service (str): The name of the service to initialize.
		    api (str | None): The API endpoint or identifier to use. If None, no API is
		        configured.
		    verbose (bool): Flag indicating whether verbose mode is enabled or not.
		"""

		if api is not None:
			self.api = api
		self.service = service
		self.verbose = verbose

	def generateUrl(self, endpoint: str) -> str:
		"""
		Generates a full URL by combining the API base URL, service path, and the provided endpoint.

		This method checks if the given endpoint is already a complete URL. If it is, the method
		returns the endpoint as-is. Otherwise, it constructs the full URL by concatenating the
		API base URL, service path, and the endpoint.

		Args:
		    endpoint (str): The endpoint to generate the full URL for. If the endpoint starts
		        with 'http', it will be returned as-is; otherwise, it will be appended to
		        the API base URL and service path.

		Returns:
		    str: The generated full URL or the input endpoint if it is already a complete URL.
		"""

		if endpoint.startswith('http'):
			return endpoint
		return f'{self.api}{self.service}{endpoint}'

	def _apiReady(self) -> bool:
		"""
		Performs a validation to check the readiness of the API configuration.

		This method ensures that the API is properly configured and meets the
		criteria of being a valid URL, starting with 'http'. If the configuration
		does not meet these requirements, a ValueError is raised.

		Returns:
		    bool: True if the API is configured and valid according to the
		    specified criteria.

		Raises:
		    ValueError: If the API configuration is invalid or not properly set.
		"""

		ready = isinstance(self.api, str) and self.api.startswith('http')
		if not ready:
			raise ValueError(f'API is not configured or not a valid URL: {self.api}')
		return ready

	def _retryLogin(self) -> Result:
		"""
		Attempts to refresh the authentication token by sending a request to the refresh URL
		with the stored refresh token. The refreshed access token is saved if the operation is
		successful.

		In case of failure, logs the error, optionally prints verbose debug information, and
		returns a `Result` object indicating the failure.

		Raises:
		    This method does not explicitly declare the exceptions it may raise during execution.
		    However, exceptions during the HTTP request or other operations may occur.

		Args:
		    This method does not accept any external arguments and operates using class-level
		    attributes and configuration.

		Returns:
		    Result: An instance of the `Result` class representing the outcome of the token
		    refresh operation.
		"""

		if not self._apiReady():
			return Result(
				status=False,
				res=None,
				message='API is not configured or not a valid URL',
				status_code=500,
			)

		try:
			data = dict(refresh=Settings.get('REFRESH_TOKEN', ''))
			refreshUrl = self.generateUrl(self.auth.refreshEndpoint if self.auth.refreshUrl else self.auth.refreshUrl)
			requestMethod = self.auth.refreshMethod.value[1] if self.auth.refreshMethod else requests.post
			Logger.info(f'Refreshing token with {requestMethod.__name__} {refreshUrl}')
			if self.verbose:
				ic(data)
			res = requestMethod(refreshUrl, json=data)
			if res.status_code in range(200, 300):
				accessToken = res.json().get(self.auth.refreshReturnTokenKey)
				Settings.set('ACCESS_TOKEN', accessToken)
				return Result(
					status=True,
					res=res,
					json=res.json(),
					status_code=res.status_code,
					message='Token refreshed successfully',
				)
			else:
				Logger.error(f'Failed to refresh token: {res.status_code} {res.text}')
				if self.verbose:
					ic(f'Failed to refresh token: {res.status_code} {res.text}')
					ic(res.json())
				return Result(
					status=False,
					res=res,
					error=res.json(),
					status_code=res.status_code,
					message=f'Failed to refresh token: {res.status_code} {res.text}',
				)
		except Exception as e:  # noqa: BLE001
			Logger.error(f'Failed to refresh token: {e}')
			if self.verbose:
				ic('Failed to refresh token:')
				ic(e)
			return Result(
				status=False,
				res=None,
				json=None,
				status_code=500,
				message=f'Failed to refresh token: {e}',
			)

	def callApi(
			self, method: Method, endpoint: str, params: dict, data: dict, authorized: bool = False,
			retry: bool = False,
	) -> Result:
		"""
		Makes an API call to a specified endpoint using the provided HTTP method. Handles authorization,
		optional retries for token refresh, and response processing. Logs the API call and its result.

		Args:
		    method (Method): The HTTP method to use for the API call (e.g., GET, POST).
		    endpoint (str): The target API endpoint to be appended to the base URL.
		    params (dict): Query parameters to include in the API call.
		    data (dict): Body data to send in the API call.
		    authorized (bool, optional): Whether the API call requires an authorization token. Defaults to False.
		    retry (bool, optional): Whether to attempt a retry in case of an authorization failure. Defaults to False.

		Returns:
		    Result: A Result object containing the API response and associated metadata.
		"""

		if not self._apiReady():
			return Result(
				status=False,
				res=None,
				message='API is not configured or not a valid URL',
				status_code=500,
			)

		try:
			headers = {}
			if authorized:
				JWTToken = Settings.get('ACCESS_TOKEN', '')
				headers['Authorization'] = f'Bearer {JWTToken}'
			url = self.generateUrl(endpoint)
			Logger.info(f'{method.name} {url}')
			if self.verbose:
				ic(params)
				ic(data)
			res = requests.request(
				method=method.name,
				url=url,
				params=params,
				data=data,
				headers=headers,
				timeout=Settings.get('TIMEOUT', 10),
			)
			if res.status_code in range(200, 300):
				return res.json()
			elif res.status_code == 403 and authorized and retry:
				refreshResult = self._retryLogin()
				if refreshResult.status:
					Logger.info('Retrying request with new token')
					return self.callApi(
						method=method,
						endpoint=endpoint,
						params=params,
						data=data,
						authorized=authorized)
				else:
					Logger.error('Failed to refresh token')
					Logger.error(f'{res.status_code}: {res.json()}')
					return refreshResult
			else:
				if res.headers.get('Content-Type') == 'application/json':
					Logger.error(f'API Error: {res.status_code}: {res.json()}')
					return Result(
						status=False,
						res=res,
						error=res.json(),
						status_code=res.status_code,
					)
				else:
					Logger.error(f'{res.status_code}: {res.text}')
					return Result(
						status=False,
						res=res,
						message=res.text,
						status_code=res.status_code,
					)
		except requests.exceptions.ConnectionError:
			Logger.error('Failed to connect to the API')
			return Result(
				status=False,
				res=None,
				message='Failed to connect to the API',
				status_code=500,
			)

	def get(self, endpoint: str, params=None, authorized: bool = False):
		"""
		Sends an HTTP GET request to a specified API endpoint with optional parameters.

		This method allows for the retrieval of content from a given endpoint. It supports
		optional query parameters and conditional authorization, and it specifies whether
		a retry mechanism should be applied if authorization is required.

		Args:
		    endpoint (str): The API endpoint to which the GET request is sent.
		    params (Optional[dict]): The query parameters to be included in the request.
		        Defaults to an empty dictionary if not provided.
		    authorized (bool): Indicates whether the request requires authorization.
		        Defaults to False.

		Returns:
		    Any: The response object resulting from the API call.

		"""

		if params is None:
			params = dict()
		retry = False
		if authorized:
			retry = True
		return self.callApi(
			method=Method.GET,
			endpoint=endpoint,
			params=params,
			data=dict(),
			authorized=authorized,
			retry=retry,
		)

	def post(self, endpoint: str, data=None, params=None, authorized: bool = False):
		"""
		Sends an HTTP POST request to the specified endpoint using the provided
		data and parameters. Optionally, the request can be made authorized
		and retried based on the flag.

		Args:
		    endpoint (str): The target endpoint for the POST request.
		    data: The payload to include in the body of the POST request.
		    params: Additional parameters to include in the query string.
		    authorized (bool): Indicates whether the request requires
		        authorization. Defaults to False.

		Returns:
		    Any: The response from the API call.

		"""

		if params is None:
			params = {}
		if data is None:
			data = {}
		retry = False
		if authorized:
			retry = True
		return self.callApi(
			method=Method.POST,
			endpoint=endpoint,
			params=params,
			data=data,
			authorized=authorized,
			retry=retry,
		)

	def put(self, endpoint: str, data=None, params=None, authorized: bool = False):
		"""
		Sends an HTTP PUT request to the specified API endpoint with the provided data and parameters. Allows authorized requests
		and retries if authorization is enabled.

		Args:
		    endpoint (str): The API endpoint to which the PUT request will be sent.
		    data (optional): The payload to include in the PUT request. Defaults to an empty dictionary.
		    params (optional): The parameters to include in the query string of the request. Defaults to an empty dictionary.
		    authorized (bool, optional): Determines whether the request requires authorization. If True, a retry mechanism
		        is enabled. Defaults to False.

		Returns:
		    Any: The response from the API as returned by the `callApi` method.
		"""

		if params is None:
			params = {}
		if data is None:
			data = {}
		retry = False
		if authorized:
			retry = True
		return self.callApi(
			method=Method.PUT,
			endpoint=endpoint,
			params=params,
			data=data,
			authorized=authorized,
			retry=retry,
		)

	def delete(self, endpoint: str, data=None, params=None, authorized: bool = False):
		"""
		Sends a DELETE request to the specified API endpoint with optional parameters,
		data, and authorization settings. Handles API interaction using the callApi
		method.

		Args:
		    endpoint (str): The API endpoint to which the DELETE request is sent.
		    data (optional): The payload to be sent with the DELETE request. Default
		        is an empty dictionary.
		    params (optional): The query parameters for the DELETE request. Default
		        is an empty dictionary.
		    authorized (bool): Indicates whether the request requires authorization.
		        Default is False.

		Returns:
		    The response object returned by the callApi method with the DELETE request.
		"""

		if params is None:
			params = {}
		if data is None:
			data = {}
		retry = False
		if authorized:
			retry = True
		return self.callApi(
			method=Method.DELETE,
			endpoint=endpoint,
			params=params,
			data=data,
			authorized=authorized,
			retry=retry,
		)

	def patch(self, endpoint: str, data=None, params=None, authorized: bool = False):
		"""
		Sends an HTTP PATCH request to the specified endpoint.

		This method sends a PATCH request to interact with a remote API. It
		supports passing optional data, query parameters, and an authorization
		flag. The authorization flag can enable retries if necessary.

		Args:
		    endpoint (str): The API endpoint to which the request is sent.
		    data (optional): The payload to include in the request. Defaults to an
		        empty dictionary if not provided.
		    params (optional): The query parameters to include in the request.
		        Defaults to an empty dictionary if not provided.
		    authorized (bool, optional): Indicates whether the request requires
		        authorization. Defaults to False.

		Returns:
		    Any: The response returned by the API.

		"""

		if params is None:
			params = {}
		if data is None:
			data = {}
		retry = False
		if authorized:
			retry = True
		return self.callApi(
			method=Method.PATCH,
			endpoint=endpoint,
			params=params,
			data=data,
			authorized=authorized,
			retry=retry,
		)

	def options(self, endpoint: str, data=None, params=None, authorized: bool = False):
		"""
		Sends an HTTP OPTIONS request to the specified API endpoint with the
		provided data, parameters, and authorization settings.

		This function allows the caller to make an OPTIONS request to retrieve
		information about communication options available at the target resource.
		It optionally includes request data and parameters, and it can be
		configured to use authorization. Retries the request upon failure if
		authorization is enabled.

		Args:
		    endpoint (str): The API endpoint to which the OPTIONS request is made.
		    data: The optional request body to be sent with the request. Defaults
		        to an empty dictionary.
		    params: The optional query parameters to include in the request.
		        Defaults to an empty dictionary.
		    authorized (bool): Indicates whether the request requires authorization.
		        If True, retries the request upon failure; otherwise, does not.
		"""

		if params is None:
			params = {}
		if data is None:
			data = {}
		retry = False
		if authorized:
			retry = True
		return self.callApi(
			method=Method.OPTIONS,
			endpoint=endpoint,
			params=params,
			data=data,
			authorized=authorized,
			retry=retry,
		)

	def head(self, endpoint: str, data=None, params=None, authorized: bool = False):
		"""
		Makes an HTTP HEAD request to the specified API endpoint. This method allows
		clients to retrieve metadata about a resource without fetching the actual data,
		adhering to the semantics of an HTTP HEAD request.

		Args:
		    endpoint (str): The API endpoint to which the request is sent.
		    data: Optional. The payload to include with the request. Defaults to an
		        empty dictionary if not provided.
		    params: Optional. Query parameters to append to the request. Defaults to
		        an empty dictionary if not provided.
		    authorized (bool): Indicates whether the request should include an
		        authorization token. Defaults to False.

		Returns:
		    Any: The response from the API call.

		"""

		if params is None:
			params = {}
		if data is None:
			data = {}
		retry = False
		if authorized:
			retry = True
		return self.callApi(
			method=Method.HEAD,
			endpoint=endpoint,
			params=params,
			data=data,
			authorized=authorized,
			retry=retry,
		)
