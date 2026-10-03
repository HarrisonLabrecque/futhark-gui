# gui/main_window.py

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget
)

from gui.generator_page import GeneratorPage
from gui.rune_library import RuneLibrary


class RuneGeneratorWindow(QMainWindow):
    """
    Main application window.

    Handles navigation between the different
    application pages.
    """

    def __init__(self):
        super().__init__()

        # ----------------------------------------------------
        # WINDOW SETTINGS
        # ----------------------------------------------------

        self.setWindowTitle(
            "Elder Futhark Rune Generator"
        )

        self.resize(
            1200,
            850
        )

        self.setup_ui()


    # ========================================================
    # BUILD USER INTERFACE
    # ========================================================

    def setup_ui(self):

        # Main central widget.
        central_widget = QWidget()

        # Main horizontal layout.
        #
        # Sidebar goes on the left.
        # Pages go on the right.
        main_layout = QHBoxLayout()

        main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        main_layout.setSpacing(
            0
        )

        # ====================================================
        # SIDEBAR
        # ====================================================

        sidebar = QWidget()

        sidebar.setObjectName(
            "sidebar"
        )

        sidebar.setFixedWidth(
            200
        )

        sidebar_layout = QVBoxLayout()

        sidebar_layout.setContentsMargins(
            15,
            25,
            15,
            25
        )

        sidebar_layout.setSpacing(
            10
        )

        # ----------------------------------------------------
        # GENERATOR BUTTON
        # ----------------------------------------------------

        self.generator_button = QPushButton(
            "Generator"
        )

        self.generator_button.setObjectName(
            "navigationButton"
        )

        self.generator_button.clicked.connect(
            self.show_generator
        )

        sidebar_layout.addWidget(
            self.generator_button
        )

        # ----------------------------------------------------
        # RUNE LIBRARY BUTTON
        # ----------------------------------------------------

        self.library_button = QPushButton(
            "Rune Library"
        )

        self.library_button.setObjectName(
            "navigationButton"
        )

        self.library_button.clicked.connect(
            self.show_rune_library
        )

        sidebar_layout.addWidget(
            self.library_button
        )

        # Push navigation buttons toward the top.
        sidebar_layout.addStretch()

        sidebar.setLayout(
            sidebar_layout
        )

        # Add sidebar to main window.
        main_layout.addWidget(
            sidebar
        )

        # ====================================================
        # PAGE SYSTEM
        # ====================================================

        self.page_stack = QStackedWidget()

        # ----------------------------------------------------
        # GENERATOR PAGE
        # ----------------------------------------------------

        self.generator_page = GeneratorPage()

        self.page_stack.addWidget(
            self.generator_page
        )

        # ----------------------------------------------------
        # RUNE LIBRARY PAGE
        # ----------------------------------------------------

        self.rune_library_page = RuneLibrary()

        self.page_stack.addWidget(
            self.rune_library_page
        )

        # Display Generator by default.
        self.page_stack.setCurrentWidget(
            self.generator_page
        )

        main_layout.addWidget(
            self.page_stack
        )

        # ====================================================
        # FINISH WINDOW
        # ====================================================

        central_widget.setLayout(
            main_layout
        )

        self.setCentralWidget(
            central_widget
        )


    # ========================================================
    # SHOW GENERATOR
    # ========================================================

    def show_generator(self):
        """
        Switch to the Rune Generator page.
        """

        self.page_stack.setCurrentWidget(
            self.generator_page
        )


    # ========================================================
    # SHOW RUNE LIBRARY
    # ========================================================

    def show_rune_library(self):
        """
        Switch to the Rune Library page.
        """

        self.page_stack.setCurrentWidget(
            self.rune_library_page
        )