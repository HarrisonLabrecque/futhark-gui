# gui/main_window.py

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget
)

from gui.generator_page import GeneratorPage
from gui.rune_library import RuneLibrary
from gui.saved_formulas import SavedFormulasPage


class RuneGeneratorWindow(QMainWindow):
    """
    Main application window.

    Controls navigation between:
        - Generator
        - Rune Library
        - Saved Formulas
    """

    def __init__(self):
        super().__init__()

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

        central_widget = QWidget()

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
            210
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
        # APPLICATION TITLE
        # ----------------------------------------------------

        sidebar_title = QLabel(
            "Elder Futhark"
        )

        sidebar_title.setObjectName(
            "sidebarTitle"
        )

        sidebar_layout.addWidget(
            sidebar_title
        )

        # ----------------------------------------------------
        # GENERATOR
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
        # RUNE LIBRARY
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

        # ----------------------------------------------------
        # SAVED FORMULAS
        # ----------------------------------------------------

        self.saved_button = QPushButton(
            "Saved Formulas"
        )

        self.saved_button.setObjectName(
            "navigationButton"
        )

        self.saved_button.clicked.connect(
            self.show_saved_formulas
        )

        sidebar_layout.addWidget(
            self.saved_button
        )

        sidebar_layout.addStretch()

        sidebar.setLayout(
            sidebar_layout
        )

        main_layout.addWidget(
            sidebar
        )

        # ====================================================
        # PAGE STACK
        # ====================================================

        self.page_stack = QStackedWidget()

        # Generator page.
        self.generator_page = GeneratorPage()

        self.page_stack.addWidget(
            self.generator_page
        )

        # Rune Library page.
        self.rune_library_page = RuneLibrary()

        self.page_stack.addWidget(
            self.rune_library_page
        )

        # Saved Formulas page.
        self.saved_formulas_page = (
            SavedFormulasPage()
        )

        self.page_stack.addWidget(
            self.saved_formulas_page
        )

        # Generator is the default page.
        self.page_stack.setCurrentWidget(
            self.generator_page
        )

        main_layout.addWidget(
            self.page_stack
        )

        central_widget.setLayout(
            main_layout
        )

        self.setCentralWidget(
            central_widget
        )


    # ========================================================
    # GENERATOR PAGE
    # ========================================================

    def show_generator(self):

        self.page_stack.setCurrentWidget(
            self.generator_page
        )


    # ========================================================
    # RUNE LIBRARY PAGE
    # ========================================================

    def show_rune_library(self):

        self.page_stack.setCurrentWidget(
            self.rune_library_page
        )


    # ========================================================
    # SAVED FORMULAS PAGE
    # ========================================================

    def show_saved_formulas(self):

        # Refresh first so formulas saved from the
        # Generator page immediately appear.
        self.saved_formulas_page.refresh_formulas()

        self.page_stack.setCurrentWidget(
            self.saved_formulas_page
        )