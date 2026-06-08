import platform

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QSizePolicy

__all__ = ["UI"]


class UIFactory:
    """
    Handles the creation of scalable UI components, such as icons, pixmaps, sizes, and color codes,
    while maintaining consistency across different resolutions and platforms.

    The UIFactory class provides methods to generate scalable images, icons, and sizes tailored for
    device-independent pixels. It also supports color conversion and DPI-specific scaling calculations.

    Properties:
            logicalDpi (int): Logical dots-per-inch (DPI) value used for resolution scaling.

    Methods:
            pixmap(file_name: str, width: Optional[int] = None, height: Optional[int] = None,
                    aspect_ratio_mode: Qt.AspectRatioMode = Qt.AspectRatioMode.IgnoreAspectRatio,
                    transform_mode: Qt.TransformationMode = Qt.TransformationMode.FastTransformation) -> QPixmap:
                    Creates a QPixmap object from an image file and scales it to the desired dimensions.
            icon(file_name: str, width: Optional[int] = None, height: Optional[int] = None,
                    aspect_ratio_mode: Qt.AspectRatioMode = Qt.AspectRatioMode.IgnoreAspectRatio,
                    transform_mode: Qt.TransformationMode = Qt.TransformationMode.FastTransformation) -> QIcon:
                    Creates an icon using a pixmap with optional resizing and aspect ratio control.
            setLogicalDpi(dpi: int) -> None:
                    Sets the logical dots-per-inch (DPI) value, which determines the resolution for rendering
            dpiFactor() -> float:
                    Calculates the DPI factor based on the system's DPI and platform.
            dp(unit: int) -> int:
                    Converts the given unit to a value scaled by the DPI (Dots Per Inch) factor.
            sp(unit: int) -> int:
                    Calculates a scaled value based on the input unit and the scaling factor.
            colorHex(color: tuple) -> str:
                    Converts an RGB color tuple to its corresponding hexadecimal color code string.
            sizePolicy(horizontal: QSizePolicy.Policy, vertical: QSizePolicy.Policy) -> QSizePolicy:
                    Creates and returns a QSizePolicy object based on the provided horizontal and vertical policies.
            size(width: int, height: int) -> QSize:
                    Calculates and returns a QSize object based on the provided width and height after applying a device-independent pixel transformation.
    """

    _logicalDpi: int = 96

    @staticmethod
    def pixmap(
        file_name: str,
        width: int | None = None,
        height: int | None = None,
        aspect_ratio_mode: Qt.AspectRatioMode = Qt.AspectRatioMode.IgnoreAspectRatio,
        transform_mode: Qt.TransformationMode = Qt.TransformationMode.FastTransformation,
    ) -> QPixmap:
        """
        Creates a QPixmap object from an image file and scales it to the desired dimensions.

        Uses the provided file path to load an image into a QPixmap object. If width and/or
        height are specified, the pixmap is scaled accordingly using the specified aspect
        ratio and transformation modes. If width is not provided but height is specified,
        a RuntimeError will occur since scaling requires both dimensions.

        Args:
                file_name: Path to the image file.
                width: The desired width of the scaled pixmap. Optional.
                height: The desired height of the scaled pixmap. Optional.
                aspect_ratio_mode: Mode that determines how the aspect ratio is handled during
                        scaling. Defaults to Qt.AspectRatioMode.IgnoreAspectRatio.
                transform_mode: Mode that determines how the pixmap should transform during
                        scaling. Defaults to Qt.TransformationMode.FastTransformation.

        Returns:
                QPixmap: Loaded and optionally scaled pixmap.

        Raises:
                RuntimeError: If width is None and height is provided, as scaling requires both
                        dimensions or neither to be specified.
        """

        pixmap = QPixmap()
        pixmap.load(file_name)
        if width is None and height is not None:
            pixmap.scaled(width, height, aspect_ratio_mode, transform_mode)
        return pixmap

    @staticmethod
    def icon(
        file_name: str,
        width: int | None = None,
        height: int | None = None,
        aspect_ratio_mode: Qt.AspectRatioMode = Qt.AspectRatioMode.IgnoreAspectRatio,
        transform_mode: Qt.TransformationMode = Qt.TransformationMode.FastTransformation,
    ) -> QIcon:
        """
        Creates an icon using a pixmap with optional resizing and aspect ratio control.

        This method generates a QIcon object based on a pixmap loaded from the
        specified file. It provides options to resize the pixmap to a specific width or
        height, and allows adjusting the aspect ratio or transformation mode during
        resizing.

        Args:
                file_name: Path to the image file to load the pixmap from.
                width: Optional width to resize the pixmap to. If None, no resizing is applied.
                height: Optional height to resize the pixmap to. If None, no resizing is applied.
                aspect_ratio_mode: Specifies how the aspect ratio should be controlled
                        during resizing. Default is Qt.AspectRatioMode.IgnoreAspectRatio.
                transform_mode: Specifies how the pixmap should be transformed during
                        resizing. Default is Qt.TransformationMode.FastTransformation.

        Returns:
                QIcon: An icon created from the processed pixmap.

        """

        return QIcon(UI.pixmap(file_name, width, height, aspect_ratio_mode, transform_mode))

    def setLogicalDpi(self, dpi: int):
        """
        Sets the logical dots-per-inch (DPI) value, which determines the resolution for rendering.

        Args:
                dpi (int): The logical DPI value to set.
        """

        self._logicalDpi = dpi

    @property
    def dpiFactor(self) -> float:
        """
        Calculates the DPI factor based on the system's DPI and platform.

        The DPI factor is computed using the logical DPI of the system. For macOS
        platforms, the logical DPI is divided by 72, while for other platforms,
        it is divided by 96. This factor is useful for scaling graphical elements
        appropriately across different operating systems.

        Returns:
                float: The calculated DPI factor specific to the system's platform.
        """

        return self._logicalDpi / (72 if platform.system() == "Darwin" else 96)

    def dp(self, unit: int) -> int:
        """
        Converts the given unit to a value scaled by the DPI (Dots Per Inch) factor.

        This function scales the input unit by the `dpiFactor` to adjust for different
        display resolutions, ensuring consistent sizing across devices.

        Args:
                unit (int): The measurement unit to be scaled by the DPI factor.

        Returns:
                int: The scaled value of the input unit based on the DPI factor.
        """

        return int(unit * self.dpiFactor)

    def sp(self, unit: int) -> int:
        """
        Calculates a scaled value based on the input unit and the scaling factor.

        This method scales the given unit value by the object's `dpiFactor` attribute
        to produce a scaled integer value.

        Args:
                unit (int): The value to be scaled.

        Returns:
                int: The scaled integer value.
        """

        return int(unit * self.dpiFactor)

    @staticmethod
    def colorHex(color: tuple) -> str:
        """
        Converts an RGB color tuple to its corresponding hexadecimal color code string.

        This method takes a tuple representing an RGB color, where each value in the tuple
        represents the intensity of red, green, and blue on a scale of 0 to 255. It converts
        this tuple into a hexadecimal color code string, commonly used in web development
        and digital design contexts.

        Args:
                color (tuple): A tuple containing three integers representing the RGB values.
                        Each integer should be between 0 and 255, inclusive.

        Returns:
                str: A string representing the hexadecimal color code, prefixed with '#'.
        """

        return "#{:02x}{:02x}{:02x}".format(*color)

    @staticmethod
    def sizePolicy(horizontal: QSizePolicy.Policy, vertical: QSizePolicy.Policy) -> QSizePolicy:
        """
        Creates and returns a QSizePolicy object based on the provided horizontal and vertical policies.

        Args:
                horizontal: The horizontal QSizePolicy.Policy to be applied to the QSizePolicy object.
                vertical: The vertical QSizePolicy.Policy to be applied to the QSizePolicy object.

        Returns:
                QSizePolicy: A QSizePolicy object with the specified horizontal and vertical policies.
        """

        return QSizePolicy(horizontal, vertical)

    def size(self, width: int, height: int) -> QSize:
        """
        Calculates and returns a QSize object based on the provided width and
        height after applying a device-independent pixel transformation.

        Args:
                width: The width in pixels before transformation.
                height: The height in pixels before transformation.

        Returns:
                QSize: A QSize object with the transformed width and height.
        """

        return QSize(self.dp(width), self.dp(height))


UI = UIFactory()
