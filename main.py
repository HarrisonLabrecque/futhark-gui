# main.py

import sys

from pathlib import Path

from PySide6.QtWidgets import QApplication

from gui.main_window import RuneGeneratorWindow


# ============================================================
# LOAD APPLICATION STYLES
# ============================================================

def load_styles(app):

    # Find project directory.
    project_root = Path(__file__).resolve().parent

    # Find QSS stylesheet.
    style_file = (
        project_root
        / "resources"
        / "styles.qss"
    )

    # Make sure the stylesheet exists.
    if not style_file.exists():

        print(
            "Warning: styles.qss was not found."
        )

        return

    # Read stylesheet.
    with open(
        style_file,
        "r",
        encoding="utf-8"
    ) as file:

        app.setStyleSheet(
            file.read()
        )


# ============================================================
# MAIN
# ============================================================

def main():

    # Create Qt application.
    app = QApplication(
        sys.argv
    )

    # Apply external QSS styling.
    load_styles(
        app
    )

    # Create main window.
    window = RuneGeneratorWindow()

    # Display main window.
    window.show()

    # Start Qt event loop.
    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()