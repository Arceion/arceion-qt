from enum import Enum

__all__ = ["Size"]


class Size(Enum):
    """Enumeration representing various size options.

    This class defines different size categories that can be used to represent or
    categorize the size of an object or entity. Each size option is represented
    with a string value for easier identification and usage.

    Attributes:
        ExtraSmall (str): Represents an extra small size category.
        Small (str): Represents a small size category.
        Default (str): Represents the default size category.
        Large (str): Represents a large size category.
    """

    ExtraSmall = "ExtraSmall"
    Small = "Small"
    Default = "Default"
    Large = "Large"
