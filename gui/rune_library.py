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
    Displays all 24 Elder Futhark runes
    inside a scrollable library.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setup_ui()


    # ========================================================
    # BUILD LIBRARY
    # ========================================================

    def setup_ui(self):

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        title = QLabel(
            "Elder Futhark Rune Library"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        title_font = QFont()
        title_font.setPointSize(22)
        title_font.setBold(True)

        title.setFont(
            title_font
        )

        main_layout.addWidget(
            title
        )

        # ----------------------------------------------------
        # DESCRIPTION
        # ----------------------------------------------------

        description = QLabel(
            "Browse all 24 Elder Futhark runes, "
            "their transliterations, and their "
            "modern/common interpretive keywords."
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

        # ----------------------------------------------------
        # SCROLL AREA
        # ----------------------------------------------------

        scroll_area = QScrollArea()

        scroll_area.setWidgetResizable(
            True
        )

        container = QWidget()

        rune_grid = QGridLayout()

        rune_grid.setSpacing(
            12
        )

        # Display four rune cards per row.
        columns = 4

        for index, rune in enumerate(
            ELDER_FUTHARK
        ):

            row = index // columns
            column = index % columns

            card = RuneCard(
                rune,
                index + 1
            )

            rune_grid.addWidget(
                card,
                row,
                column
            )

        container.setLayout(
            rune_grid
        )

        scroll_area.setWidget(
            container
        )

        main_layout.addWidget(
            scroll_area
        )

        self.setLayout(
            main_layout
        )