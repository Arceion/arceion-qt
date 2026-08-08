from collections.abc import Callable

from PyQt6.QtCore import QRectF, QSize, Qt, QTimer, QUrl
from PyQt6.QtGui import QColor, QDesktopServices, QIcon, QPainter, QPen
from PyQt6.QtWidgets import QSizePolicy, QToolButton

from arceion.qt.contrib.enums import Size
from arceion.qt.contrib.styles.Button import defaultButton, linkButton
from arceion.qt.contrib.widgets.Attr import Padding
from arceion.qt.util import UI, Style

__all__ = ["Button"]


class Button(QToolButton):
    """
    A custom styled button widget based on QToolButton.

    Supports:
    - Applying a Style object or raw QSS string for consistent theming.
    - Customizing text, tooltip, icon, icon size, padding, and layout direction.
    - Handling click and press events with user-defined callbacks.
    - Adjusting its size dynamically based on icon and padding.
    - Icon-only buttons (auto-sized square, no text).
    - A loading spinner state via setLoading().
    - Pill/rounded shape via setRounded() (requires a Style object).
    - RTL layout via `direction`.
    - Hyperlink-style buttons via the `Button.asLink(...)` constructor.
    """

    _onPressCallback: Callable | None = None
    _styleSheet: str = defaultButton.qss

    def __init__(
        self,
        text: str = "",
        tooltip: str = "",
        icon: QIcon | None = None,
        iconSize: QSize | None = None,
        padding: Padding | None = None,
        style: str | Style = defaultButton,
        toolButtonStyle: Qt.ToolButtonStyle = Qt.ToolButtonStyle.ToolButtonTextOnly,
        direction: Qt.LayoutDirection = Qt.LayoutDirection.LeftToRight,
        onClick: Callable | None = None,
        size: Size | None = None,
        spaceBetween: int = 1,
    ):
        """
        Initialize the Button widget.

        Args:
                text (str): Text displayed on the button. Leave empty (with an
                        icon set) for an auto-sized, square icon-only button.
                tooltip (str): Tooltip text shown when hovering.
                icon (QIcon | None): Optional icon for the button.
                iconSize (QSize | None): Size of the icon. Defaults to 16dp.
                padding (Padding | None): Padding around the button content.
                style (str | Style): Style object or raw QSS string applied to the button.
                        Pass a Style object (not a raw string) if you plan to call setRounded().
                toolButtonStyle (Qt.ToolButtonStyle): Layout style for text/icon. Overridden
                        to IconOnly automatically for icon-only buttons.
                direction (Qt.LayoutDirection): Layout direction (LTR or RTL).
                onClick (Callable | None): Callback executed when the button is clicked.
                size (int | None): Optional fixed height.

        Returns:
                None
        """
        super().__init__()

        self._text = text
        self._tooltip = tooltip
        self._icon = icon
        self._iconSize = iconSize if iconSize else QSize(UI.dp(16), UI.dp(16))
        self._padding = padding if padding else Padding(0)
        self._direction = direction
        self._toolButtonStyle = toolButtonStyle
        self._size = size
        self._style = style
        self._spaceBetween = spaceBetween

        # loading spinner state
        self._loading = False
        self._preLoadingText: str = ""
        self._spinnerAngle = 0
        self._spinnerColor = QColor("#FFFFFF")
        self._spinnerTimer = QTimer(self)
        self._spinnerTimer.timeout.connect(self._rotateSpinner)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.setContentsMargins(self._padding)

        self.setToolButtonStyle(toolButtonStyle)
        self.setLayoutDirection(direction)

        self.updateSize()
        self._applyStyle(self._style)
        self.updateTextAndIcon()

        if onClick:
            self.onClick(onClick)

    def updateSize(self):
        iconOnly = not self._text and self._icon
        if self._size == Size.ExtraSmall:
            self._iconSize = UI.size(24, 24)
            if iconOnly:
                self.setFixedSize(self._iconSize)
                self._style = self._style.update(padding=Padding(0).qss)
            if not iconOnly:
                if self._toolButtonStyle != Qt.ToolButtonStyle.ToolButtonTextUnderIcon:
                    self.setFixedHeight(UI.dp(24))
                self._style = self._style.update(padding=Padding(UI.dp(6), UI.dp(0)).qss, fontSize=UI.dp(10))
        if self._size == Size.Small:
            self._iconSize = UI.size(28, 28)
            if iconOnly:
                self.setFixedSize(self._iconSize)
                self._style = self._style.update(padding=Padding(0).qss)
            if not iconOnly:
                if self._toolButtonStyle != Qt.ToolButtonStyle.ToolButtonTextUnderIcon:
                    self.setFixedHeight(UI.dp(28))
                self._style = self._style.update(padding=Padding(UI.dp(7), UI.dp(0)).qss, fontSize=UI.dp(12))
        if self._size == Size.Default:
            self._iconSize = UI.size(32, 32)
            if iconOnly:
                self.setFixedSize(self._iconSize)
                self._style = self._style.update(padding=Padding(0).qss)
            if not iconOnly:
                if self._toolButtonStyle != Qt.ToolButtonStyle.ToolButtonTextUnderIcon:
                    self.setFixedHeight(UI.dp(32))
                self._style = self._style.update(padding=Padding(UI.dp(8), UI.dp(2)).qss, fontSize=UI.dp(14))
        if self._size == Size.Large:
            self._iconSize = UI.size(36, 36)
            if iconOnly:
                self.setFixedSize(self._iconSize)
                self._style = self._style.update(padding=Padding(0).qss)
            if not iconOnly:
                if self._toolButtonStyle != Qt.ToolButtonStyle.ToolButtonTextUnderIcon:
                    self.setFixedHeight(UI.dp(36))
                self._style = self._style.update(padding=Padding(UI.dp(10), UI.dp(4)).qss, fontSize=UI.dp(14))

    def _applyStyle(self, style: str | Style) -> None:
        """
        Resolve and apply a Style object or raw QSS string, tracking the
        Style object (if any) so setRounded() can call `.update()` on it.
        """
        self._appliedStyle = style if isinstance(style, Style) else None
        self._styleSheet = style if isinstance(style, str) else style.qss
        self.setStyleSheet(self._styleSheet)

    def setStyleSheetFromStyle(self, style: str | Style) -> None:
        """
        Apply a new QSS style.

        Args:
                style (str | Style): Style object or raw QSS string.

        Returns:
                None
        """
        self._style = style
        self.updateSize()
        self._applyStyle(self._style)

    def setRounded(self, rounded: bool = True, radius: int | None = None) -> None:
        """
        Toggle a fully pill-shaped border radius (shadcn's `rounded-full`).

        Requires the button's current style to be a Style object (not a
        raw QSS string) since it relies on Style.update(). See also the
        `pill()` helper in ShadcnButtonStyles for a one-shot equivalent.

        Args:
                rounded (bool): Whether to apply the pill radius.
                radius (int | None): Explicit radius to fall back to when
                        `rounded=False`. Defaults to 6dp.

        Returns:
                None
        """
        if self._appliedStyle is None:
            raise TypeError("setRounded requires the button's style to be a Style object, not a raw QSS string")
        newRadius = UI.dp(9999) if rounded else (radius if radius is not None else UI.dp(6))
        self._appliedStyle = self._appliedStyle.update(borderRadius=newRadius)
        self._styleSheet = self._appliedStyle.qss
        self.setStyleSheet(self._styleSheet)

    def updateTextAndIcon(self) -> None:
        """
        Update button text, icon, tooltip, layout direction, and — for
        icon-only buttons (no text, icon set) — enforce a square size.

        Returns:
                None
        """
        if self._tooltip:
            super().setToolTip(self._tooltip)

        self.setLayoutDirection(self._direction)

        if self._icon:
            super().setIcon(self._icon)
            super().setIconSize(self._iconSize)
        if self._text:
            super().setText(
                (
                    " " * self._spaceBetween
                    if self._icon and self._toolButtonStyle != Qt.ToolButtonStyle.ToolButtonTextUnderIcon
                    else ""
                )
                + self._text
            )
        else:
            super().setText("")

        if not self._text and self._icon:
            super().setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        else:
            super().setToolButtonStyle(self._toolButtonStyle)

    def setText(self, text: str) -> None:
        """
        Set the button text and update the UI.

        Args:
                text (str): New text for the button.

        Returns:
                None
        """
        self._text = text
        self.updateTextAndIcon()

    def setToolTip(self, tooltip: str) -> None:
        """
        Set the button tooltip.

        Args:
                tooltip (str): Tooltip text.

        Returns:
                None
        """
        self._tooltip = tooltip
        super().setToolTip(tooltip)

    def setIcon(self, icon: QIcon, iconSize: QSize | None = None) -> None:
        """
        Set the button icon and optional icon size.

        Args:
                icon (QIcon): Icon to display.
                iconSize (QSize | None): Optional size for the icon.

        Returns:
                None
        """
        self._icon = icon
        if iconSize:
            self._iconSize = iconSize
        self.updateTextAndIcon()

    def setIconSize(self, iconSize: QSize) -> None:
        """
        Set the icon size.

        Args:
                iconSize (QSize): New icon size.

        Returns:
                None
        """
        self._iconSize = iconSize
        self.updateTextAndIcon()

    def setPadding(self, padding: Padding) -> None:
        """
        Set the padding for the button.

        Args:
                padding (Padding): Padding object.

        Returns:
                None
        """
        self._padding = padding
        self.setContentsMargins(padding)
        self.adjustSize()

    def setDirection(self, direction: Qt.LayoutDirection) -> None:
        """
        Set the layout direction (LTR/RTL). Flips icon/text order and
        text alignment automatically via Qt's own RTL handling.

        Args:
                direction (Qt.LayoutDirection): LTR or RTL.

        Returns:
                None
        """
        self._direction = direction
        self.setLayoutDirection(direction)
        self.updateTextAndIcon()

    def setLoading(self, loading: bool, spinnerColor: str | None = None) -> None:
        """
        Show/hide a spinning loading indicator in place of the button's
        text, and disable interaction while loading.

        Args:
                loading (bool): Whether the button is in a loading state.
                spinnerColor (str | None): Optional hex color for the spinner
                        (defaults to white, matching most filled variants).

        Returns:
                None
        """
        if loading == self._loading:
            return
        self._loading = loading
        if spinnerColor:
            self._spinnerColor = QColor(spinnerColor)

        if loading:
            self._preLoadingText = self._text
            self.setText("")
            self.setEnabled(False)
            self._spinnerAngle = 0
            self._spinnerTimer.start(16)
        else:
            self._spinnerTimer.stop()
            self.setEnabled(True)
            self.setText(self._preLoadingText)
        self.update()

    def toggleLoading(self, spinnerColor: str | None = None) -> None:
        self.setLoading(not self._loading, spinnerColor)

    def isLoading(self) -> bool:
        """Returns whether the button is currently in its loading state."""
        return self._loading

    def _rotateSpinner(self) -> None:
        self._spinnerAngle = (self._spinnerAngle + 6) % 360
        self.update()

    def paintEvent(self, event) -> None:
        """
        Paint the button normally, then overlay a rotating arc spinner
        centered on the button while `_loading` is True.
        """
        super().paintEvent(event)
        if not self._loading:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        diameter = min(self.width(), self.height()) * 0.5
        rect = QRectF(
            (self.width() - diameter) / 2,
            (self.height() - diameter) / 2,
            diameter,
            diameter,
        )
        pen = QPen(self._spinnerColor, max(2.0, diameter * 0.12))
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawArc(rect, self._spinnerAngle * 16, 270 * 16)
        painter.end()

    @classmethod
    def asLink(
        cls,
        text: str,
        url: str,
        tooltip: str = "",
        style: str | Style | None = None,
        direction: Qt.LayoutDirection = Qt.LayoutDirection.LeftToRight,
        onClick: Callable | None = None,
    ) -> "Button":
        """
        Convenience constructor for a Button that behaves like a
        hyperlink: styled with shadcn's `link` variant by default, and
        opens `url` in the system's default browser when clicked.

        Args:
                text (str): Link text.
                url (str): URL to open on click.
                tooltip (str): Optional tooltip.
                style (str | Style | None): Overrides the default `linkButton` style.
                direction (Qt.LayoutDirection): LTR or RTL.
                onClick (Callable | None): Extra callback run alongside opening the URL.

        Returns:
                Button: A configured, link-styled Button instance.
        """

        def _handleClick():
            QDesktopServices.openUrl(QUrl(url))
            if onClick:
                onClick()

        return cls(
            text=text,
            tooltip=tooltip,
            style=style if style is not None else linkButton,
            direction=direction,
            onClick=_handleClick,
        )

    def onClick(self, action: Callable) -> None:
        """
        Connect a click handler to the button.

        Args:
                action (Callable): Function executed on click.

        Returns:
                None
        """
        self.clicked.connect(action)

    def onPress(self, action: Callable) -> None:
        """
        Connect a press handler to the button.

        Args:
                action (Callable): Function executed on mouse press.

        Returns:
                None
        """
        self._onPressCallback = action

    def mousePressEvent(self, event) -> None:
        """
        Handle mouse press events.

        Args:
                event: Mouse event object.

        Returns:
                None
        """
        if self._loading:
            return
        if self._onPressCallback:
            self._onPressCallback(event)
        else:
            self.clicked.emit()

    def sizeHint(self) -> QSize:
        """
        Provide a custom size hint based on icon size and padding.

        Returns:
                QSize: Suggested size for the button.
        """
        base_size = super().sizeHint()
        return QSize(
            base_size.width() + self._padding.totalHorizontal(),
            max(base_size.height(), self._iconSize.height() + self._padding.totalVertical()),
        )
