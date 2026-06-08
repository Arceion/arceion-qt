from enum import Enum
from typing import Any

from arceion.qt.logger import Logger

from .ColorTheme import ColorTheme
from .Images import Images
from .LocaleBuilder import LocaleBuilder

__all__ = ["Theme"]


class Theme:
    """
    Represents the application theme, including color and image themes.
    This class manages the color palette and image resources based on the selected themes.
    It allows setting the color theme and image theme, and provides access to the corresponding
    color palette and images.

    Attributes:
            colorTheme (Enum): The current color theme.
            imageTheme (Enum): The current image theme.
            colorPalette (Dict[Any, ColorTheme]): A dictionary mapping color themes to their respective ColorTheme objects.
            images (Images): An instance of the Images class for managing image resources.
            locale (LocaleBuilder): An instance of LocaleBuilder for managing localization.

    Methods:
            colors (ColorTheme): Returns the ColorTheme corresponding to the current color theme.

    Raises:
            TypeError: If the image theme is not an instance of Enum.
            ValueError: If the color theme is not recognized.
    """

    colorTheme: Enum
    imageTheme: Enum

    colorPalette: dict[Any, ColorTheme]
    images: Images
    colors: ColorTheme
    locale: LocaleBuilder

    def __setattr__(self, key, value) -> None:
        """
        Sets attributes for the Theme class with specific type validation for `imageTheme`
        and `colorTheme`. Ensures the correct handling when these attributes are updated by
        performing validation checks and calling relevant methods for processing.

        Args:
                key (str): The name of the attribute being set.
                value: The new value being assigned to the attribute. Must adhere to specific
                        type constraints for certain attributes.

        Raises:
                TypeError: If `imageTheme` is not an instance of `Enum`.
                ValueError: If `colorTheme` is not an instance of `Enum`.

        """

        if key == "imageTheme":
            if not isinstance(value, Enum):
                raise TypeError(f"Image theme must be an instance of Enum, got {type(value)}")
            self.images.setTheme(value)
        if key == "colorTheme":
            if not isinstance(value, Enum):
                raise ValueError(f"Color theme must be an instance of Enum, got {type(value)}")
            if colorTheme := self.colorPalette.get(value):
                self.colors = colorTheme
        super().__setattr__(key, value)

    @classmethod
    def setColorTheme(cls, theme: Enum):
        """
        Sets the color theme for the application.

        Updates the current color theme and associated colors from the predefined color
        palette. The method will raise a ValueError if the provided theme is not
        recognized.

        Args:
                theme (Enum): The desired color theme. Must be present in the class's
                        predefined color palette.

        Raises:
                ValueError: If the specified theme is not recognized.

        """

        if theme.value not in cls.colorPalette:
            raise ValueError(f"Color theme {theme} is not recognized.")
        cls.colorTheme = theme
        cls.colors = cls.colorPalette[theme.value]
        Logger.info(f"Setting color theme to {theme}")
