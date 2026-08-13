from enum import Enum

from arceion.qt.res import ColorTheme
from arceion.qt.res import Theme as ThemeMeta

__all__ = ["Theme", "AppTheme"]


class Theme(Enum):
    LIGHT = "light"
    DARK = "dark"


class AppTheme(ThemeMeta):
    colorTheme = Theme.DARK
    colorPalette = {
        Theme.LIGHT.value: ColorTheme(
            background="#F8F8F8",
            text="#000000",
            primary="#000000",
            color="#FFFFFF",
            hoverPrimary="#333333",
            borderColor="#E5E5E5",
            hoverBorderColor="#E5E5E5",
            hoverGhost="#F5F5F5",
            secondary="#F5F5F5",
            hoverSecondary="#E5E5E5",
            destructive="#FDE6E7",
            hoverDestructive="#FACCCE",
            colorDestructive="#FF6467",
        ),
        Theme.DARK.value: ColorTheme(
            background="#1E1E1E",
            text="#FFFFFF",
            primary="#FFFFFF",
            color="#000000",
            hoverPrimary="#E9E9E9",
            borderColor="#2F2F2F",
            hoverBorderColor="#2F2F2F",
            hoverGhost="#1C1C1C",
            secondary="#262626",
            hoverSecondary="#2F2F2F",
            destructive="#3B1C1C",
            hoverDestructive="#542526",
            colorDestructive="#FF6467",
        ),
    }
    colors = colorPalette[colorTheme.value]
