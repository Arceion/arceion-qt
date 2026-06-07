import sys

if __name__ == "__main__":
	args = sys.argv

	# Handle management commands
	if len(args) >= 2:
		command = args[1]

		# startproject command
		if command == 'startproject':
			from arceion.qt.management import startproject

			# Parse arguments
			project_name = None
			target_dir = '.'

			if len(args) >= 3:
				# Check if it's a directory path or project name
				arg = args[2]
				if arg == '.' or arg.startswith('./') or arg.startswith('.\\') or '/' in arg or '\\' in arg:
					target_dir = arg
				else:
					project_name = arg

			if len(args) >= 4:
				target_dir = args[3]

			startproject(project_name, target_dir)
			sys.exit(0)

		# icons command (existing)
		elif command == 'icons':
			from PyQt6.QtWidgets import QApplication
			app = QApplication(sys.argv)
			from arceion.qt.res.IconExplorer import IconsExplorer
			from arceion.qt.res.Icons import iconSet
			window = IconsExplorer(iconSet)
			window.show()
			sys.exit(app.exec())

	# Show help if no valid command
	print("Arceion Qt Management Commands")
	print("\nUsage:")
	print("  python -m arceion.qt <command> [options]")
	print("\nAvailable commands:")
	print("  startproject [name] [directory]  Create a new Arceion Qt project")
	print("  icons                            Open the icon explorer")
	print("\nExamples:")
	print("  python -m arceion.qt startproject .              # Create project in current directory")
	print("  python -m arceion.qt startproject myapp          # Create project named 'myapp'")
	print("  python -m arceion.qt startproject myapp ./src    # Create project in specific directory")
	print("  python -m arceion.qt icons                       # Open icon explorer")
	sys.exit(0)
