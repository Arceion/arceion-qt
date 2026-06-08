# Contributing to Arceion Qt

Thank you for your interest in contributing to Arceion Qt! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Branch Naming Conventions](#branch-naming-conventions)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Development Environment](#development-environment)

## Code of Conduct

By participating in this project, you agree to maintain a respectful, inclusive, and harassment-free environment for all contributors.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended) or pip
- Git

### Setting Up Your Development Environment

1. **Fork the repository** on GitHub

2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/arceion-qt.git
   cd arceion-qt
   ```

3. **Add the upstream repository**:
   ```bash
   git remote add upstream https://github.com/Arceion/arceion-qt.git
   ```

4. **Create a virtual environment and install dependencies**:
   ```bash
   # Using uv (recommended)
   uv sync --dev

   # Or using pip
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e ".[dev]"
   ```

5. **Verify your installation**:
   ```bash
   uv run pytest -v
   uv run ruff check
   ```

## Development Workflow

1. **Sync with upstream** before starting work:
   ```bash
   git checkout dev
   git fetch upstream
   git merge upstream/dev
   ```

2. **Create a feature branch** from `dev`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes** following the coding standards

4. **Run tests and linting**:
   ```bash
   make test
   make lint
   ```

5. **Commit your changes** with descriptive messages

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request** targeting the `dev` branch

## Branch Naming Conventions

Use the following prefixes for branch names:

- `feature/` - New features or enhancements
  - Example: `feature/auth-jwt`, `feature/custom-theme-editor`

- `fix/` - Bug fixes
  - Example: `fix/login-crash`, `fix/memory-leak-worker`

- `docs/` - Documentation changes
  - Example: `docs/readme-update`, `docs/api-examples`

- `refactor/` - Code refactoring without functional changes
  - Example: `refactor/database-layer`, `refactor/simplify-signals`

- `test/` - Adding or updating tests
  - Example: `test/api-controller`, `test/view-lifecycle`

- `chore/` - Maintenance tasks, dependency updates
  - Example: `chore/update-dependencies`, `chore/ci-improvements`

**Format**: `<type>/<short-description-in-kebab-case>`

## Coding Standards

### Python Style

- **Formatter**: Use Ruff formatter (configured in `pyproject.toml`)
- **Line length**: Maximum 120 characters
- **Indentation**: Tabs (4 spaces) for Python files
- **Quotes**: Double quotes for strings
- **Type hints**: Required for all public functions and methods

### Code Quality Rules

- Follow PEP 8 conventions
- Use type hints for function parameters and return values
- Write docstrings for public classes, methods, and functions
- Keep functions focused and small (prefer < 50 lines)
- Avoid deep nesting (max 3-4 levels)
- Use meaningful variable and function names

### Example

```python
from typing import Optional
from arceion.qt.core import View


class ExampleView(View):
	"""
	Example view demonstrating coding standards.

	Attributes:
		_data: Internal data storage
	"""

	def __init__(self, parent: Optional[QWidget] = None) -> None:
		"""Initialize the view with optional parent widget."""
		super().__init__(parent)
		self._data: dict[str, str] = {}

	def onCreate(self) -> None:
		"""Set up the view UI components."""
		# Implementation here
		pass
```

### Architecture Guidelines

- Follow the existing `Window`/`View` architecture pattern
- Use the `ThreadPool` for asynchronous operations
- Leverage the `Controller` class for API interactions
- Keep UI logic separate from business logic
- Use signals for component communication

### Import Organization

Organize imports in the following order:
1. Standard library imports
2. Third-party imports (PyQt6, SQLAlchemy, etc.)
3. Local application imports

Use Ruff's isort integration for automatic import sorting.

## Testing Guidelines

### Writing Tests

- Place tests in the `tests/` directory, mirroring the source structure
- Use `pytest` for all tests
- Use `pytest-qt` for Qt-specific testing
- Aim for meaningful test coverage (not just high percentages)

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
uv run pytest tests/test_specific.py -v

# Run with coverage report
uv run pytest --cov=arceion --cov-report=html
```

### Test Naming

- Test files: `test_<module>.py`
- Test classes: `Test<ClassName>`
- Test functions: `test_<specific_behavior>`

Example:
```python
def test_view_lifecycle_onCreate_called_on_initialization():
	"""Test that onCreate is called when view is initialized."""
	# Test implementation
```

## Pull Request Process

### Before Submitting

Ensure your PR meets these requirements:

- [ ] Code follows the project's coding standards
- [ ] All tests pass (`make test`)
- [ ] Linting passes (`make lint`)
- [ ] Type hints are included where appropriate
- [ ] New code includes appropriate tests
- [ ] Documentation is updated (if applicable)
- [ ] No breaking changes (or clearly documented)
- [ ] Commit messages follow the guidelines

### PR Description Template

When opening a PR, include:

```markdown
## Description
Brief description of what this PR does.

## Motivation
Why is this change needed? What problem does it solve?

## Changes
- Bullet point list of changes

## Testing
How has this been tested?

## Screenshots (if applicable)
Include screenshots for UI changes

## Checklist
- [ ] Tests added/updated
- [ ] Linting passes
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### Review Process

1. A maintainer will review your PR within 3-5 business days
2. Address any feedback or requested changes
3. Once approved, a maintainer will merge your PR into `dev`
4. Your contribution will be included in the next release

## Commit Message Guidelines

### Format

```
<type>: <subject>

<body (optional)>

<footer (optional)>
```

### Types

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```bash
feat: add dark theme support to Window class

fix: resolve memory leak in ThreadPool worker cleanup

docs: update API controller usage examples in README

refactor: simplify View lifecycle management
```

### Best Practices

- Use imperative mood ("add" not "added" or "adds")
- Don't capitalize the first letter
- No period at the end of the subject line
- Keep subject line under 50 characters
- Separate subject from body with a blank line
- Wrap body at 72 characters
- Explain *what* and *why*, not *how*

## Development Environment

### Recommended Tools

- **IDE**: PyCharm, VS Code with Python extension
- **Python Version Manager**: pyenv
- **Package Manager**: uv (recommended) or pip
- **UI design**: Custom development (recommended). Qt Designer(not recommended)

### Pre-commit Checks

Before committing, run:

```bash
# Auto-fix linting issues
make fix

# Check remaining issues
make lint

# Run tests
make test
```

### Useful Commands

```bash
# Install dependencies
uv sync --dev

# Run linter
uv run ruff check

# Auto-fix linting issues
uv run ruff check --fix

# Format code
uv run ruff format

# Run tests with verbose output
uv run pytest -v

# Run tests with coverage
uv run pytest --cov=arceion --cov-report=term-missing
```

## Questions or Need Help?

- **Issues**: Check [existing issues](https://github.com/Arceion/arceion-qt/issues) or open a new one
- **Discussions**: Use GitHub Discussions for general questions
- **Email**: Contact the maintainers at arceionllc@gmail.com

## License

By contributing to Arceion Qt, you agree that your contributions will be licensed under the same license as the project (Proprietary License).

---

Thank you for contributing to Arceion Qt! Your efforts help make this project better for everyone.
