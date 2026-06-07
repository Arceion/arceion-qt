from PyQt6.QtGui import QColor

__all__ = ['ColorTheme']


class ColorTheme:
    """
    Represents a dynamic color theme with attributes as QColor objects.

    The ColorTheme class provides functionality for dynamically adding and retrieving color
    attributes. Each attribute corresponds to a `QColor` object, enabling flexible color
    management. Attributes can be dynamically set using keyword arguments during initialization
    or through the `addColor` method.

    This class is used to create a color theme for the application. This class provides the basic structure
    for the color theme. You can initialize color theme like this:
    ColorTheme(
        background="#FFFFFF",
        foreground="#000000",
        primary="#FF5733",
        secondary="#33FF57",
        accent="#3357FF"
    )

    Attributes:
        **kwargs: Arbitrary keyword arguments dynamically assigned as QColor attributes during
            initialization.

    Methods:
        addColor(self, name: str, color: str) -> None: Adds a color attribute to the theme object.
        getColor(self, name: str) -> QColor: Retrieves the color associated with a given name.
    """

    def __setattr__(self, key, value):
        """
        Sets an attribute as a QColor object if both the attribute name and the value
        are valid. The attribute name must be a valid Python identifier, and the value
        must be a valid color string accepted by QColor.

        Args:
            key: Name of the attribute to set.
            value: Color value to associate with the attribute. Must be a valid string
                recognizable by QColor.

        Raises:
            ValueError: If the attribute name is not a valid Python identifier.
            ValueError: If the color value is not valid.
        """

        if not key.isidentifier():
            raise ValueError(f'Invalid attribute name: {key}')
        if not isinstance(value, str) or not QColor(value).isValid():
            raise ValueError(f'Invalid color value for {key}')
        super().__setattr__(key, QColor(value))

    def __getattr__(self, item):
        """
        Retrieves the value of the specified attribute. The method is called when
        an attempt to access an attribute that does not exist or is inaccessible
        occurs. It acts as a fallback mechanism. Delegates to the superclass's
        `__getattribute__` for attribute resolution.

        Args:
            item: The name of the attribute being accessed.

        Returns:
            Any: The value of the requested attribute.

        Raises:
            AttributeError: If the attribute does not exist.
        """

        return super().__getattribute__(item)

    def __init__(self, **kwargs):
        """
        Represents a color theme model allowing dynamic assignment of attributes
        through keyword arguments.

        Attributes:
            **kwargs: Arbitrary keyword arguments used to dynamically set instance
                attributes upon initialization.
        """

        super().__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def addColor(self, name: str, color: str) -> None:
        """
        Adds a color attribute to the object with the specified name and color value.

        This method dynamically creates an attribute on the object with a given name
        and assigns the provided color value to it.

        Args:
            name (str): The name of the attribute to be added.
            color (str): The color value to assign to the attribute.

        """

        setattr(self, name, color)

    def getColor(self, name: str) -> QColor:
        """
        Retrieves the color associated with a given name from the theme object.

        This method looks up the color attribute in the current theme object based on
        the provided name. It ensures the given name is valid and corresponds to an
        existing color attribute within the object.

        Args:
            name (str): The name of the color attribute to retrieve. It must be a valid
                identifier, and the attribute must exist within the theme object.

        Returns:
            QColor: The color associated with the specified name.

        Raises:
            ValueError: If the given name is not a valid identifier.
            AttributeError: If the specified name does not correspond to an existing
                attribute in the theme object.
        """

        if not name.isidentifier():
            raise ValueError('Invalid name')
        if not hasattr(self, name):
            raise AttributeError('Color is not defined in the theme')
        return getattr(self, name)
