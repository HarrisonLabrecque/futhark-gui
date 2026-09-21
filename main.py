# main.py

import sys

from PySide6.QtWidgets import QApplication

from gui.main_window import RuneGeneratorWindow


def main():

    # Create Qt application.
    app = QApplication(
        sys.argv
    )

    # Create the main application window.
    window = RuneGeneratorWindow()

    # Display the GUI.
    window.show()

    # Start the Qt event loop.
    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()