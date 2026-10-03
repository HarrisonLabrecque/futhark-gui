# gui/rune_library.py

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QGridLayout,
    QScrollArea
)

from data.runes import ELDER_FUTHARK
from gui.rune_card import RuneCard


class RuneLibrary(QWidget):
    """
    Rune Library page.

    Displays all 24 Elder Futhark runes using
    reusable RuneCard widgets.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setup_ui()


    # ========================================================
    # BUILD USER INTERFACE
    # ========================================================

    def setup_ui(self):

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            25,
            25,
            25,
            25
        )

        main_layout.setSpacing(
            15
        )

        # ====================================================
        # TITLE
        # ====================================================

        title = QLabel(
            "Elder Futhark Rune Library"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        title_font = QFont()
        title_font.setPointSize(25)
        title_font.setBold(True)

        title.setFont(
            title_font
        )

        main_layout.addWidget(
            title
        )

        # ====================================================
        # DESCRIPTION
        # ====================================================

        description = QLabel(
            "Browse all 24 Elder Futhark runes, "
            "their transliterations, and modern/common "
            "interpretive keywords."
        )

        description.setAlignment(
            Qt.AlignCenter
        )

        description.setWordWrap(
            True
        )

        main_layout.addWidget(
            description
        )

        # ====================================================
        # SCROLL AREA
        # ====================================================

        self.scroll_area = QScrollArea()

        self.scroll_area.setWidgetResizable(
            True
        )

        self.rune_container = QWidget()

        self.rune_grid = QGridLayout()

        self.rune_grid.setSpacing(
            12
        )

        # Four rune cards per row.
        columns = 4

        # Create a card for all 24 runes.
        for index, rune in enumerate(
            ELDER_FUTHARK
        ):

            row = index // columns
            column = index % columns

            rune_card = RuneCard(
                rune,
                index + 1
            )

            self.rune_grid.addWidget(
                rune_card,
                row,
                column
            )

        self.rune_container.setLayout(
            self.rune_grid
        )

        self.scroll_area.setWidget(
            self.rune_container
        )

        main_layout.addWidget(
            self.scroll_area
        )

        self.setLayout(
            main_layout
        )