# main.py

import sys

from pathlib import Path

from PySide6.QtWidgets import QApplication

from gui.main_window import RuneGeneratorWindow


# ============================================================
# RESOURCE PATH
# ============================================================

def resource_path(relative_path):
    """
    Return the correct resource path.

    Works when:
        - Running normally with Python.
        - Running as a PyInstaller executable.
    """

    # PyInstaller stores bundled resources inside
    # a temporary/internal bundle directory.
    if hasattr(sys, "_MEIPASS"):

        base_path = Path(
            sys._MEIPASS
        )

    else:

        # Normal Python development environment.
        base_path = Path(
            __file__
        ).resolve().parent

    return (
        base_path
        / relative_path
    )


# ============================================================
# LOAD STYLESHEET
# ============================================================

def load_styles(app):
    """
    Load the external QSS application stylesheet.
    """

    style_file = resource_path(
        "resources/styles.qss"
    )

    if not style_file.exists():

        print(
            f"Warning: stylesheet not found: "
            f"{style_file}"
        )

        return

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

    # Apply external stylesheet.
    load_styles(
        app
    )

    # Create main window.
    window = RuneGeneratorWindow()

    # Display application.
    window.show()

    # Start Qt event loop.
    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()