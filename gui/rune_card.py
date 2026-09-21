# gui/rune_card.py

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout
)


class RuneCard(QFrame):
    """
    Visual widget used to display information
    about one Elder Futhark rune.
    """

    def __init__(
        self,
        rune,
        number,
        parent=None
    ):
        super().__init__(parent)

        self.rune = rune
        self.number = number

        self.setObjectName(
            "runeCard"
        )

        self.setup_ui()


    def setup_ui(self):

        layout = QVBoxLayout()

        # ----------------------------------------------------
        # RUNE NUMBER
        # ----------------------------------------------------

        number_label = QLabel(
            f"Rune {self.number}"
        )

        number_label.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            number_label
        )

        # ----------------------------------------------------
        # RUNE SYMBOL
        # ----------------------------------------------------

        symbol_label = QLabel(
            self.rune["symbol"]
        )

        symbol_label.setAlignment(
            Qt.AlignCenter
        )

        symbol_font = QFont()
        symbol_font.setPointSize(38)

        symbol_label.setFont(
            symbol_font
        )

        layout.addWidget(
            symbol_label
        )

        # ----------------------------------------------------
        # RUNE NAME
        # ----------------------------------------------------

        name_label = QLabel(
            self.rune["name"]
        )

        name_label.setAlignment(
            Qt.AlignCenter
        )

        name_font = QFont()
        name_font.setPointSize(13)
        name_font.setBold(True)

        name_label.setFont(
            name_font
        )

        layout.addWidget(
            name_label
        )

        # ----------------------------------------------------
        # TRANSLITERATION
        # ----------------------------------------------------

        transliteration_label = QLabel(
            f"Sound: "
            f"{self.rune['transliteration']}"
        )

        transliteration_label.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            transliteration_label
        )

        # ----------------------------------------------------
        # MEANING
        # ----------------------------------------------------

        meaning_label = QLabel(
            self.rune["meaning"]
        )

        meaning_label.setAlignment(
            Qt.AlignCenter
        )

        meaning_label.setWordWrap(
            True
        )

        layout.addWidget(
            meaning_label
        )

        self.setLayout(
            layout
        )