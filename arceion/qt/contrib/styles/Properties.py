from arceion.qt.util import Style

__all__ = ["bg", "bgPrimary", "bgTransparent"]

bg = Style(
    """
QWidget [
	background-color: {bgColor};
]
""",
    **dict(bgColor="transparent"),
)

bgPrimary = bg.update(**dict(bgColor="#242424"))
bgTransparent = bg.update(**dict(bgColor="transparent"))
