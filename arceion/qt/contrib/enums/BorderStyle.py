from enum import Enum

__all__ = ['BorderStyle']


class BorderStyle(Enum):
	"""
	Represents different border styles for UI elements or graphical rendering.

	This enumeration class is used to define various border styles that can be
	applied to graphical elements or components. Each style corresponds to a
	specific border appearance, such as solid or dashed, which can be used to
	customize the visual representation of borders in an application.

	Attributes:
	    SOLID: Solid border without breaks or gaps.
	    DASHED: Border consisting of dashes.
	    DOTTED: Border consisting of dots.
	    DOUBLE: Border with two parallel lines.
	    GROOVE: Border giving the appearance of being carved or grooved.
	    RIDGE: Border giving the appearance of being raised or ridged.
	    INSET: Border giving the appearance of being inset into the surface.
	    OUTSET: Border giving the appearance of being outset from the surface.
	    NONE: No border.
	"""

	SOLID = 'solid'
	DASHED = 'dashed'
	DOTTED = 'dotted'
	DOUBLE = 'double'
	GROOVE = 'groove'
	RIDGE = 'ridge'
	INSET = 'inset'
	OUTSET = 'outset'
	NONE = 'none'
