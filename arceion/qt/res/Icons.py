import json
import os
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Generic, TypeVar

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QFont, QFontDatabase, QIcon
from PyQt6.QtWidgets import QLabel

__all__ = ["Icons", "SystemIcon", "iconSet"]

iconSet = json.load(open(Path(__file__).parent / "Icons" / "icons.json", encoding="utf-8"))

_root = Path(__file__).parent / "Icons"
_base = "static/MaterialSymbols"

NORMAL = 0
FILLED = 1

_modes = [NORMAL, FILLED]

SHARP = 0
ROUNDED = 1
OUTLINED = 2

_styles = [SHARP, ROUNDED, OUTLINED]

_pts = [0, 28, 36, 48]

ExtraLight = 0
Light = 1
Thin = 2
Regular = 3
Medium = 4
SemiBold = 5
Bold = 6

_weights = [ExtraLight, Light, Thin, Regular, Medium, SemiBold, Bold]

_modesValues = ["", "_Filled"]
_stylesValues = ["Sharp", "Rounded", "Outlined"]
_ptsValues = {0: "", 28: "_28pt", 36: "_36pt", 48: "_48pt"}
_weightsValues = ["ExtraLight", "Light", "Thin", "Regular", "Medium", "SemiBold", "Bold"]

_displayModes = ["", "Filled"]
_displayStyles = ["Sharp", "Rounded", "Outlined"]
_displayPts = ["", "pt28", "pt36", "pt48"]
_displayWeights = ["ExtraLight", "Light", "Thin", "Regular", "Medium", "SemiBold", "Bold"]


IconType = TypeVar("IconType", bound="Icon")
SystemIconType = TypeVar("SystemIconType", bound="SystemIcon")


def _generateFilePath(mode: int = NORMAL, style: int = SHARP, pt: int = 0, weight: int = Regular):
    """
    Generates a file path string based on the specified mode, style, font size, and weight.

    This function validates that the given parameters match predefined sets of values before generating
    a formatted file path string for a font file. The parameters control different aspects of the
    font file selection.

    Args:
        mode (int): The mode identifier. Must be one of the predefined valid mode values.
        style (int): The style identifier. Must be one of the predefined valid style values.
        pt (int): The point size of the font. Must be one of the predefined valid point size values.
        weight (int): The weight of the font. Must be one of the predefined valid weight values.

    Returns:
        str: The generated file path string for the specified font.

    Raises:
        ValueError: If any of the provided parameters do not match their respective valid values.
    """

    if mode not in _modes:
        raise ValueError(f"mode must be one of {_modesValues}")
    if style not in _styles:
        raise ValueError(f"style must be one of {_stylesValues}")
    if pt not in _pts:
        raise ValueError(f"pt must be one of {_ptsValues}")
    if weight not in _weights:
        raise ValueError(f"weight must be one of {_weightsValues}")
    return (
        f"{_root}/{_stylesValues[style]}/{_base}{_stylesValues[style]}{_modesValues[mode]}"
        f"{_ptsValues[pt]}-{_weightsValues[weight]}.ttf"
    )


class SystemIcon(QIcon, Generic[SystemIconType]):
    """
    Represents a customizable system icon with attributes such as size, color, and
    background.

    This class extends functionalities of QIcon to allow dynamic updates to icon
    attributes and provides methods to retrieve various representations of the icon
    such as string, pixmap, and text. It is generic and can be used for different
    types of system icons.

    Methods:
            update(size: Optional[int] = None, color: Optional[str] = None, background: Optional[str] = None) -> SystemIconType:
            setSize(size: int) -> SystemIconType: Sets the size of the system icon, updates the size parameter internally, and returns the updated SystemIconType object.
            setColor(color: str) -> SystemIconType: Sets the color of the system icon.
            setBackgroundColor(background: str) -> SystemIconType: Sets the background color for the system icon.
            toStr() -> str: Converts the icon to its string representation.
            toPixmap(mode: QIcon.Mode = QIcon.Mode.Normal, state: QIcon.State = QIcon.State.Off) -> QPixmap: Generates a QPixmap representation of the icon based on the specified mode and state.
            getFont() -> QFont: Retrieves a QFont instance configured based on the icon's settings.
            toText() -> str: Converts the internal icon representation to its corresponding text.
    """

    _icon: IconType  # type: ignore

    def setIcon(self, icon: IconType):
        """
        Sets the icon for the object.

        This method updates the internal icon attribute with the provided icon value.

        Args:
            icon (IconType): The new icon value to set.
        """

        self._icon = icon

    def update(self, size: int | None = None, color: str | None = None, background: str | None = None):
        """
        Updates the icon properties and regenerates the icon with the specified attributes.

        This method allows modifying the size, color, and background of the icon. If no
        value is provided for a specific parameter, the existing value of the icon will
        remain unchanged. It creates a new icon based on the modified attributes and
        returns the updated icon.

        Args:
            size: The size of the icon to be updated. Optional; if not provided, the
                  current size will remain unchanged.
            color: The color of the icon to be updated. Optional; if not provided, the
                   current color will remain unchanged.
            background: The background of the icon to be updated. Optional; if not
                        provided, the current background will remain unchanged.

        Returns:
            A new icon object generated with the updated properties.
        """

        icon = deepcopy(self._icon)
        if size:
            icon.size = size
        if color:
            icon.color = color
        if background:
            icon.backGround = background
        newIcon = icon.generateIcon()
        newIcon.setIcon(icon)
        return newIcon

    def setSize(self, size: int) -> SystemIconType:
        """
        Sets the size of the system icon, updates the size parameter internally,
        and returns the updated SystemIconType object.

        Args:
            size (int): The new size to set for the system icon.

        Returns:
            SystemIconType: The updated system icon with the specified size.
        """

        return self.update(size=size)

    def setColor(self, color: str) -> SystemIconType:
        """
        Sets the color of the system icon.

        This method updates the color of the system icon by accepting a string
        representing the desired color, then applying the update.

        Args:
            color (str): The desired color to set the system icon to.

        Returns:
            SystemIconType: The updated system icon with the specified color.
        """

        return self.update(color=color)

    def setBackgroundColor(self, background: str) -> SystemIconType:
        """
        Sets the background color for the system icon.

        This method updates the background color of the system icon by passing
        the specified color argument. The updated system icon type is returned.

        Args:
            background (str): The background color to be set, specified as a string.

        Returns:
            SystemIconType: The updated system icon type after applying the new
            background color.
        """

        return self.update(background=background)

    def toStr(self):
        """
        Converts the icon to its string representation.

        This method utilizes the `toStr` method of the `_icon` attribute to generate
        a string representation of the icon.

        Returns:
            str: The string representation of the `_icon` attribute.
        """

        return self._icon.toStr()

    def toPixmap(self, mode: QIcon.Mode = QIcon.Mode.Normal, state: QIcon.State = QIcon.State.Off):
        """
        Generates a QPixmap representation of the icon based on the specified mode
        and state.

        Args:
            mode (QIcon.Mode): Specifies the mode for the icon's appearance,
                such as Normal, Disabled, or Active.
            state (QIcon.State): Specifies the state for the icon's appearance,
                such as On or Off.

        Returns:
            QPixmap: The generated pixmap with the appropriate visuals according
            to the provided mode and state.
        """

        return self.pixmap(QSize(self._icon.size, self._icon.size), mode=mode, state=state)

    def getFont(self) -> QFont:
        """
        Retrieves a QFont instance configured based on the icon's settings.

        The font is created using the family, style, size, and weight defined
        in the icon's configuration. The pixel size of the font is set to the
        specific size defined in the icon's attributes.

        Returns:
            QFont: The configured font instance.
        """

        font = QFont(self._icon.iconFamilies[self._icon.style][self._icon.mode][self._icon.pt][self._icon.weight])
        font.setPixelSize(self._icon.size)
        return font

    def toText(self) -> str:
        """
        Converts the internal icon representation to its corresponding text.

        Returns:
            str: The text representation of the icon.
        """

        return iconSet[self._icon.icon]


@dataclass
class Icon(Generic[IconType]):
    """
    Represents an Icon configuration and generation class.

    This class is designed to facilitate the creation and management of system icons
    by defining their properties such as mode, style, size, background, color, and
    more. It provides mechanisms to generate icons and construct a human-readable
    string representation of the icon's configuration. The class leverages predefined
    icon families and configurations for consistent icon generation across different
    styles and modes.

    Attributes:
        mode (int): A predefined mode identifier for the icon.
        style (Optional[int]): The style attribute of the icon. Defaults to None.
        pt (Optional[int]): The point size for the icon's font. Defaults to None.
        weight (Optional[int]): The font weight for the icon. Defaults to None.
        icon (Optional[str]): The identifier for the desired icon. Defaults to None.
        size (int): The display size of the icon in pixels. Defaults to 24.
        backGround (str): The background color of the icon. Defaults to 'transparent'.
        color (str): The text color of the icon. Defaults to 'black'.

    Methods:
            generateIcon() -> SystemIcon: Generates a system icon with the specified attributes.
            toStr() -> str: Generates a human-readable string representation of the icon's configuration.
    """

    mode: int = NotImplemented
    style: int | None = None
    pt: int | None = None
    weight: int | None = None
    icon: str | None = None
    size: int = 24
    backGround: str = "transparent"
    color: str = "black"

    iconFamilies: ClassVar[dict] = {}
    for style in _styles:
        iconFamilies[style] = {}
        for mode in _modes:
            iconFamilies[style][mode] = {}
            for pt in _pts:
                iconFamilies[style][mode][pt] = {}
                for weight in _weights:
                    filePath = _generateFilePath(mode, style, pt, weight)
                    if os.path.exists(filePath):
                        fontId = QFontDatabase.addApplicationFont(filePath)
                        family = QFontDatabase.applicationFontFamilies(fontId)[0]
                        iconFamilies[style][mode][pt][weight] = family

    def generateIcon(self):
        """
        Generates a system icon with the given attributes.

        This function is responsible for generating a system icon using pre-defined font styles, modes, icon sets,
        and other related attributes. The generated icon will reflect the specified configurations for font, size,
        background color, and text color. It ensures that all attributes are valid before proceeding with the creation
        of the icon.

        Raises:
            ValueError: If the mode, style, point size (pt), or weight attributes are invalid.
            ValueError: If the specified icon is not found in the icon set.

        Returns:
            SystemIcon: A system icon object configured with the specified attributes.
        """

        if self.mode not in _modes or self.style not in _styles or self.pt not in _pts or self.weight not in _weights:
            raise ValueError("Invalid attribute")
        if self.icon not in iconSet:
            raise ValueError("Invalid icon")
        font = QFont(self.iconFamilies[self.style][self.mode][self.pt][self.weight])
        font.setPixelSize(self.size)

        label = QLabel()
        label.setFont(font)
        label.setText(iconSet[self.icon])
        label.setStyleSheet(f"background-color: {self.backGround}; color: {self.color};")
        icon = SystemIcon(label.grab())
        icon.setIcon(self)
        return icon

    def toStr(self):
        """
        Generates a string representation of an object's display configuration.

        This method constructs a string representation based on the object's display
        properties such as mode, style, point size, weight, and icon. It utilizes
        predefined mappings to determine human-readable values for each property.

        Returns:
            str: A human-readable string representation of the display configuration.
        """

        return (
            f"{_displayModes[self.mode]}{f' {_displayStyles[self.style]}' if self.style is not None else ''}"
            f"{f' {_displayPts[self.pt]}' if self.pt is not None else ''}"
            f"{f' {_displayWeights[self.weight]}' if self.weight is not None else ''}"
            f" {self.icon}"
        )


class Nested:
    icon: Icon

    def __init__(self, icon: Icon):
        """
        Initializes an object with the specified icon.

        Args:
            icon (Icon): The icon to be associated with the object.
        """

        self.icon = icon

    def __getattr__(self, name):
        """
        Handles dynamic access to attributes and assigns corresponding styles, points, weights, or icons
        to the `icon` object. The method evaluates the attribute name and modifies the icon's properties
        based on predefined mappings or sets default values where applicable. If no matching icon is
        found, an AttributeError is raised.

        Args:
            name (str): The name of the attribute being accessed dynamically.

        Returns:
            Any: Depending on the context, returns a `Nested` instance or the result of
            `icon.generateIcon()`.

        Raises:
            AttributeError: If the `name` does not correspond to a valid icon.
        """

        icon = self.icon

        if self.icon.style is None:
            if name in _displayStyles:
                icon.style = _displayStyles.index(name)
                return Nested(icon)
            icon.style = 0
            return getattr(Nested(icon), name)

        if self.icon.pt is None:
            if name in _displayPts:
                icon.pt = list(_ptsValues.keys())[_displayPts.index(name)]
                return Nested(icon)
            icon.pt = 0
            return getattr(Nested(icon), name)

        if self.icon.weight is None:
            if name in _displayWeights:
                icon.weight = _displayWeights.index(name)
                return Nested(icon)
            icon.weight = 3
            return getattr(Nested(icon), name)

        if self.icon.icon is None:
            if name in iconSet:
                icon.icon = name
                return icon.generateIcon()

        raise AttributeError(f"Icon {name} not found")


class IconsManager:
    """
    Manages dynamic access to nested display modes and default instances.

    The `icons` class is responsible for providing dynamic access to predefined display
    modes as instances of a nested `Icon` class. If an attribute corresponding to a
    specific display mode is accessed, the method dynamically creates and returns the
    appropriate `Nested(Icon)` instance. If the attribute does not match the predefined
    display modes, it delegates the access to a default `Nested(Icon)` instance.

    Attributes:
        No public attributes are exposed in this class. All logic is handled dynamically
        through the `__getattr__` method.

    Usage:
            >>> Icons.IconName
            >>> Icons.Filled.IconName
            >>> Icons.Filled.Sharp.IconName
            >>> Icons.Filled.Sharp.pt28.IconName
            >>> Icons.Filled.Sharp.pt28.ExtraLight.IconName
            >>> icon = Icons.Filled.Sharp.pt28.ExtraLight.IconName
            >>> icon = icon.update(size=24, color='red')
            >>> icon = icon.setColor('red')
            >>> icon = icon.setBackgroundColor('red')
            >>> icon_as_a_string = icon.toStr()
    """

    def __getattr__(self, name):
        """
        Handles attribute access dynamically to return an instance tied to specific
        display modes or delegates attribute access to a default instance.

        The method dynamically evaluates the requested attribute (`name`) to determine
        if it corresponds to one of the predefined display modes. It returns an instance
        of the `Nested` class containing an `Icon` object initialized with specific
        parameters. If the attribute does not match a predefined display mode, it falls
        back to accessing the attribute on a default instance of `Nested(Icon)`.

        Args:
            name (str): The name of the attribute being accessed. Can correspond to
                specific display modes or other attributes.

        Returns:
            Any: An instance of `Nested` containing an `Icon` object if the attribute
            matches a predefined display mode; otherwise, the attribute value from a
            default instance of `Nested(Icon)`.
        """

        if name == _displayModes[1]:
            return Nested(
                Icon(
                    mode=1,
                    style=None,
                    pt=None,
                    weight=None,
                    icon=None,
                )
            )
        if name == _displayModes[0]:
            return Nested(
                Icon(
                    mode=0,
                    style=None,
                    pt=None,
                    weight=None,
                    icon=None,
                )
            )

        return getattr(
            Nested(
                Icon(
                    mode=0,
                    style=None,
                    pt=None,
                    weight=None,
                    icon=None,
                )
            ),
            name,
        )


Icons = IconsManager()
