from PyQt6.QtCore import QMargins

__all__ = ['Padding']


class Padding(QMargins):
	"""
	Padding(int)
	Padding(vertical: int = None, horizontal: int = None)
	Padding(left: int, top: int, right: int, bottom: int)
	"""

	def __init__(self, *__args, **__kwargs):
		super().__init__()

		left: int
		top: int
		right: int
		bottom: int

		if len(__args) == 1 and isinstance(__args[0], int):
			a0 = __args[0]
			left, top, right, bottom = a0, a0, a0, a0
		elif len(__args) == 2 and isinstance(__args[0], int) and isinstance(__args[1], int):
			left, right = __args[0], __args[0]
			top, bottom = __args[1], __args[1]
		elif len(__args) == 4 and all(isinstance(i, int) for i in __args):
			left, top, right, bottom = __args
		elif 0 < len(__kwargs.keys()) <= 2:
			horizontal = __kwargs[
				'horizontal'] if 'horizontal' in __kwargs else 0
			vertical = __kwargs['vertical'] if 'vertical' in __kwargs else 0
			left, right = horizontal, horizontal
			top, bottom = vertical, vertical
		else:
			left = __kwargs['left'] if 'left' in __kwargs else 0
			top = __kwargs['top'] if 'top' in __kwargs else 0
			right = __kwargs['right'] if 'right' in __kwargs else 0
			bottom = __kwargs['bottom'] if 'bottom' in __kwargs else 0

		self.setLeft(left)
		self.setTop(top)
		self.setRight(right)
		self.setBottom(bottom)

	@property
	def qss(self):
		if self.totalHorizontal() == 0 and self.totalVertical() == 0:
			return '0'
		return f'{self.toPx(self.top())} {self.toPx(self.right())} {self.toPx(self.bottom())} {self.toPx(self.left())}'

	@staticmethod
	def toPx(value) -> str:
		return f'{value}px' if value != 0 else '0'

	def totalHorizontal(self):
		return self.left() + self.right()

	def totalVertical(self):
		return self.top() + self.bottom()
