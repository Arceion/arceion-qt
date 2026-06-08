from .Env import Env
from .EnvMode import EnvMode

__all__ = ["EnvManager"]


class EnvManager:
    """
    Manages application environments and configurations.

    This class provides methods for managing different application environments, including
    setting, retrieving, and initializing environment configurations. It supports defining
    multiple environments and switching between them as needed. The environment configurations
    are designed to be accessed at both the class level (global configuration) and instance level
    (specific configurations).

    Attributes:
        envs (Dict[EnvMode, Env]): A mapping of environment modes to their corresponding
            environment objects.
        current_env (Env): The currently active environment object for the instance.

    Methods:
            set_env(env: Env): Sets the environment for the class.
            get_env() -> Env: Retrieves the environment configuration set for the application.
            get(key: str) -> str: Fetches the value associated with the provided key from the environment configuration.
            current() -> Env: Returns the current environment associated with the instance.
            init(): Initializes the current environment.
    """

    _env = None

    @classmethod
    def set_env(cls, env: Env):
        """
        Sets the environment for the class.

        This method allows defining or updating the environment configuration used by the class.
        This operation is implemented at the class level and affects all instances if applicable.

        Args:
            env (Env): The environment object to be set for the class.
        """

        cls._env = env

    @classmethod
    def get_env(cls) -> Env:
        """
        Retrieves the environment configuration set for the application.

        Raises:
            ValueError: If the environment has not been set prior to calling this
                method.

        Returns:
            Env: The environment configuration associated with the class.
        """

        if cls._env is None:
            raise ValueError("Environment not set")
        return cls._env

    @classmethod
    def get(cls, key: str):
        """
        Fetches the value associated with the provided key from the environment configuration.

        This class method retrieves a value by its key from the environment configuration
        using the `get` method of the class's environment object.

        Args:
            key (str): The key for which the corresponding value should be retrieved.

        Returns:
            str: The value associated with the given key in the environment configuration.
            If the key does not exist, returns `None`.
        """

        return cls.get_env().get(key)

    def __init__(self, envs: list[Env] | None = None, default=EnvMode.DEBUG):
        """
        Initializes the environment configuration with given or default environments.

        This constructor allows configuration of multiple environments and sets the
        initial environment to a default or supplied value. If no environments are
        provided, it initializes with predetermined debug and release environments.

        Args:
            envs (List[Env] | None): A list of predefined environments to load. If
                None, default environments for debugging and release will be
                created and loaded.
            default (EnvMode): The default environment to set upon initialization.
        """

        if envs is None:
            envs = [
                Env(EnvMode.DEBUG),
                Env(EnvMode.RELEASE),
            ]
        self.envs = {env.mode: env for env in envs}
        self.current_env = self.envs[default]
        self.set_env(self.current_env)

    def current(self) -> Env:
        """
        Returns the current environment associated with the instance.

        This method retrieves the environment currently in use by the instance.
        The returned environment could represent any contextual setting, such
        as configuration or runtime states required by the application.

        Returns:
            Env: The current environment object associated with the instance.
        """

        return self.current_env

    def init(self):
        """
        Initializes the current environment.

        This method is used to initialize the environment associated with the
        instance. It ensures that all necessary preparations are made for the
        environment to commence its operations.

        Returns:
            None
        """

        self.current_env.init()
