"""
Management commands for Arceion Qt
"""

import shutil
import sys
from pathlib import Path

from .templates import (
	APP_PY,
	APP_THEME,
	ENUMS_INIT,
	ENV_PY,
	HOME_VIEW,
	LOCALE_EN_US,
	LOCALE_ENUM,
	LOCALE_SI_LK,
	MAIN_PY,
	PYPROJECT_TOML,
	RES_INIT,
	THEME_ENUM,
	VIEWS_INIT,
)

__all__ = ["startproject"]


def _to_pascal_case(name: str) -> str:
	"""Convert a string to PascalCase for class names"""
	# Remove special characters and split by space, dash, underscore
	parts = name.replace("-", " ").replace("_", " ").split()
	return "".join(word.capitalize() for word in parts if word)


def _get_arceion_static_path() -> Path:
	"""Get the path to arceion.qt static resources"""
	try:
		import arceion.qt

		arceion_path = Path(arceion.qt.__file__).parent
		static_path = arceion_path / "static"
		if static_path.exists():
			return static_path
	except ImportError:
		pass
	return None


def startproject(project_name: str | None = None, target_dir: str | None = "."):
	"""
	Create a new Arceion Qt project structure

	Args:
		project_name: Name of the project (optional, defaults to directory name)
		target_dir: Target directory for the project (default: current directory)
	"""
	# Determine target directory
	target_path = Path(target_dir).resolve()

	# If target is '.', use current directory
	if target_dir == ".":
		target_path = Path.cwd()

	print("Starting Arceion Qt project")

	# Determine project name
	if project_name is None:
		print("Please provide a project name:")
		project_name = input().strip()

	# Validate project name
	if not project_name or not project_name.replace(" ", "").replace("-", "").replace("_", "").isalnum():
		print(f"Error: Invalid project name '{project_name}'")
		print("Project name should contain only alphanumeric characters, hyphens, or underscores")
		sys.exit(1)

	# Create app class name
	app_class = _to_pascal_case(project_name)
	if not app_class:
		app_class = "App"

	print(f"Creating Arceion Qt project '{project_name}' in {target_path}")

	# Create directory structure
	directories = [
		target_path,
		target_path / "components",
		target_path / "enums",
		target_path / "models",
		target_path / "views",
		target_path / "services",
		target_path / "res",
		target_path / "res" / "locale",
		target_path / "res" / "images",
		target_path / "res" / "images" / "light",
		target_path / "res" / "images" / "dark",
		target_path / "res" / "fonts",
		target_path / "res" / "qss",
		target_path / "payload",
		target_path / "payload" / "requests",
		target_path / "payload" / "responses",
	]

	for directory in directories:
		directory.mkdir(parents=True, exist_ok=True)
		print(f"  Created directory: {directory.relative_to(target_path.parent)}")

	# Create main files
	files = {
		"main.py": MAIN_PY.format(project_name=project_name, app_class=app_class),
		f"{app_class}.py": APP_PY.format(project_name=project_name, app_class=app_class),
		"env.py": ENV_PY,
		"pyproject.toml": PYPROJECT_TOML.format(project_name=project_name),
	}

	for filename, content in files.items():
		file_path = target_path / filename
		file_path.write_text(content, encoding="utf-8")
		print(f"  Created file: {file_path.relative_to(target_path.parent)}")

	# Create enums
	enums_files = {
		"enums/__init__.py": ENUMS_INIT,
		"enums/Theme.py": THEME_ENUM,
		"enums/Locale.py": LOCALE_ENUM,
	}

	for filename, content in enums_files.items():
		file_path = target_path / filename
		file_path.write_text(content, encoding="utf-8")
		print(f"  Created file: {file_path.relative_to(target_path.parent)}")

	# Create views
	views_files = {
		"views/__init__.py": VIEWS_INIT,
		"views/HomeView.py": HOME_VIEW,
	}

	for filename, content in views_files.items():
		file_path = target_path / filename
		file_path.write_text(content, encoding="utf-8")
		print(f"  Created file: {file_path.relative_to(target_path.parent)}")

	# Create res files
	res_files = {
		"res/__init__.py": RES_INIT,
		"res/AppTheme.py": APP_THEME,
		"res/locale/enUS.json": LOCALE_EN_US,
		"res/locale/siLK.json": LOCALE_SI_LK,
	}

	for filename, content in res_files.items():
		file_path = target_path / filename
		file_path.write_text(content, encoding="utf-8")
		print(f"  Created file: {file_path.relative_to(target_path.parent)}")

	# Create empty __init__.py files
	init_files = [
		"models/__init__.py",
		"services/__init__.py",
		"payload/__init__.py",
		"payload/requests/__init__.py",
		"payload/responses/__init__.py",
		"res/qss/__init__.py",
		"components/__init__.py"
	]

	for filename in init_files:
		file_path = target_path / filename
		file_path.write_text("", encoding="utf-8")
		print(f"  Created file: {file_path.relative_to(target_path.parent)}")

	# Copy logo images from arceion.qt static directory
	static_path = _get_arceion_static_path()
	if static_path and (static_path / "img").exists():
		img_source = static_path / "img"

		# Copy logos to light theme directory
		logo_files = [
			"Arceion Logo 1024X1024 Transparent Round.png",
			"Arceion Logo 1024X1024 White Round.png",
		]

		for logo_file in logo_files:
			source_file = img_source / logo_file
			if source_file.exists():
				dest_file = target_path / "res" / "images" / "light" / logo_file
				shutil.copy2(source_file, dest_file)
				print(f"  Copied logo: {dest_file.relative_to(target_path.parent)}")
	else:
		print("  Warning: Could not find arceion.qt static images. Logo files not copied.")
		print("  You can manually copy logos to res/images/light/ directory.")

	# Create README
	readme_content = f"""# {project_name}

A desktop application built with Arceion Qt.

## Getting Started

### Installation

```bash
pip install -r requirements.txt
```
or

```bash
uv sync
```

### Running the Application

```bash
python main.py
```

or

```bash
uv run python main.py
```

## Project Structure

- `main.py` - Application entry point
- `{app_class}.py` - Main window class
- `env.py` - Environment configuration
- `components/` - Reusable UI components
- `enums/` - Enum definitions (Theme, Locale, etc.)
- `models/` - Data models
- `views/` - Application views
- `services/` - Business logic and services
- `res/` - Resources (themes, images, localization)
- `payload/` - API request/response models

## Development

- Add new views in the `views/` directory
- Configure your theme in `res/AppTheme.py`
- Add localization strings in `res/locale/`
- Define models in the `models/` directory

## Built with Arceion Qt

[Arceion Qt](https://github.com/Arceion/arceion-qt) - A modern Python Qt framework
"""

	readme_path = target_path / "README.md"
	readme_path.write_text(readme_content, encoding="utf-8")
	print(f"  Created file: {readme_path.relative_to(target_path.parent)}")

	print(f"\nSuccessfully created project '{project_name}'!")
	print("\nNext steps:")
	print(f"  1. cd {target_path if target_dir != '.' else project_name}")
	print("  2. Install dependencies: pip install arceion-qt")
	print("  3. Run your application: python main.py")
	print("\nHappy coding!")
