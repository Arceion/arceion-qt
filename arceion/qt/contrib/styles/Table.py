from arceion.qt.contrib.enums import BorderStyle
from arceion.qt.contrib.widgets.Attr import Border
from arceion.qt.util import UI, Style

__all__ = ["defaultTable"]

defaultTable = Style(
    """
QTableWidget#Table [
    background-color: {backgroundColor};
    alternate-background-color: {alternateBackgroundColor};
    border: {border};
    border-radius: {borderRadius}px;
    color: {color};
    gridline-color: {gridlineColor};
    selection-background-color: {selectionBackgroundColor};
    selection-color: {selectionColor};
]

QTableWidget#Table::item [
    border-bottom: {rowBorder};
    padding: {cellPadding};
]

QTableWidget#Table::item:selected [
    background-color: {selectionBackgroundColor};
    color: {selectionColor};
]

QHeaderView::section [
    background-color: {headerBackgroundColor};
    border: none;
    border-bottom: {headerBorder};
    color: {headerColor};
    font-weight: {headerFontWeight};
    padding: {headerPadding};
]

""",
    **dict(
        backgroundColor="#FFFFFF",
        alternateBackgroundColor="#FFFFFF",
        border=Border(BorderStyle.NONE).qss,
        borderRadius=UI.dp(12),
        color="#09090B",
        gridlineColor="#E4E4E7",
        selectionBackgroundColor="#F4F4F5",
        selectionColor="#09090B",
        rowBorder=Border("#E4E4E7", BorderStyle.SOLID, 1).qss,
        cellPadding=f"{UI.dp(12)}px {UI.dp(16)}px",
        headerBackgroundColor="#FFFFFF",
        headerBorder=Border("#E4E4E7", BorderStyle.SOLID, 1).qss,
        headerColor="#71717A",
        headerFontWeight="600",
        headerPadding=f"{UI.dp(12)}px {UI.dp(16)}px",
    ),
)
