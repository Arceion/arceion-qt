import json

from fontTools.ttLib import TTFont

modes = [
	'Outlined', 'Rounded', 'Sharp',
]
pts = [
	'', '_28pt', '_36pt', '_48pt',
]
weights = [
	'ExtraLight', 'Light', 'Thin', 'Regular', 'Medium', 'SemiBold', 'Bold',
]
base = 'static/MaterialSymbols'


def extract(fontPath):
	cmap = TTFont(fontPath)['cmap'].getBestCmap()
	return {value: chr(key) for key, value in cmap.items()}


# for mode in modes:
# 	with open(f'{mode}.json', 'w', encoding='utf-8') as File:
# 		icons = {
# 			'Normal': {},
# 			'Filled': {}
# 		}
# 		for pt in pts:
# 			ptIndex = pt.removeprefix('_').removesuffix('dp') if pt != '' else '0'
# 			icons['Normal'][ptIndex] = {}
# 			icons['Filled'][ptIndex] = {}
# 			for weight in weights:
# 				NormalFile = f'{mode}/{base}{mode}{pt}-{weight}.ttf'
# 				icons['Normal'][ptIndex][weight] = extract(NormalFile)
# 				FilledFile = f'{mode}/{base}{mode}_Filled{pt}-{weight}.ttf'
# 				icons['Filled'][ptIndex][weight] = extract(FilledFile)
# 		json.dump(icons, File, indent=4)
#

with open('../Icons/icons.json', 'w', encoding='utf-8') as File:
	icons = {}
	for mode in modes:
		for pt in pts:
			for weight in weights:
				NormalFile = f'{mode}/{base}{mode}{pt}-{weight}.ttf'
				FilledFile = f'{mode}/{base}{mode}_Filled{pt}-{weight}.ttf'

				NormalIcons = extract(NormalFile)
				for name, icon in NormalIcons.items():
					if name not in icons:
						icons[name] = icon

				FilledIcons = extract(FilledFile)
				for name, icon in FilledIcons.items():
					if name not in icons:
						icons[name] = icon

	json.dump(icons, File, indent=4)
