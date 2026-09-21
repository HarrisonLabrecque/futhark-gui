import sys
import random
from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QScrollArea,
    QTextEdit,
    QFileDialog,
    QMessageBox,
    QFrame
)


# ============================================================
# ELDER FUTHARK DATA
# ============================================================
#
# symbol         = Unicode rune
# name           = Common modern rune name
# transliteration = Approximate Latin-letter value
# meaning        = Short modern/common interpretive keywords
#
# Elder Futhark contains 24 runes.
# ============================================================

ELDER_FUTHARK = [
    {
        "symbol": "ᚠ",
        "name": "Fehu",
        "transliteration": "F",
        "meaning": "wealth, resources, prosperity"
    },
    {
        "symbol": "ᚢ",
        "name": "Uruz",
        "transliteration": "U",
        "meaning": "strength, vitality, endurance"
    },
    {
        "symbol": "ᚦ",
        "name": "Thurisaz",
        "transliteration": "TH",
        "meaning": "force, challenge, defense"
    },
    {
        "symbol": "ᚨ",
        "name": "Ansuz",
        "transliteration": "A",
        "meaning": "communication, wisdom, inspiration"
    },
    {
        "symbol": "ᚱ",
        "name": "Raidho",
        "transliteration": "R",
        "meaning": "journey, movement, direction"
    },
    {
        "symbol": "ᚲ",
        "name": "Kenaz",
        "transliteration": "K",
        "meaning": "knowledge, illumination, creativity"
    },
    {
        "symbol": "ᚷ",
        "name": "Gebo",
        "transliteration": "G",
        "meaning": "gift, exchange, partnership"
    },
    {
        "symbol": "ᚹ",
        "name": "Wunjo",
        "transliteration": "W",
        "meaning": "joy, harmony, success"
    },
    {
        "symbol": "ᚺ",
        "name": "Hagalaz",
        "transliteration": "H",
        "meaning": "disruption, transformation, change"
    },
    {
        "symbol": "ᚾ",
        "name": "Nauthiz",
        "transliteration": "N",
        "meaning": "need, endurance, constraint"
    },
    {
        "symbol": "ᛁ",
        "name": "Isa",
        "transliteration": "I",
        "meaning": "stillness, focus, patience"
    },
    {
        "symbol": "ᛃ",
        "name": "Jera",
        "transliteration": "J/Y",
        "meaning": "harvest, cycles, reward"
    },
    {
        "symbol": "ᛇ",
        "name": "Eihwaz",
        "transliteration": "EI",
        "meaning": "resilience, transition, protection"
    },
    {
        "symbol": "ᛈ",
        "name": "Perthro",
        "transliteration": "P",
        "meaning": "mystery, chance, hidden things"
    },
    {
        "symbol": "ᛉ",
        "name": "Algiz",
        "transliteration": "Z",
        "meaning": "protection, awareness, defense"
    },
    {
        "symbol": "ᛊ",
        "name": "Sowilo",
        "transliteration": "S",
        "meaning": "sun, success, vitality"
    },
    {
        "symbol": "ᛏ",
        "name": "Tiwaz",
        "transliteration": "T",
        "meaning": "justice, courage, honor"
    },
    {
        "symbol": "ᛒ",
        "name": "Berkano",
        "transliteration": "B",
        "meaning": "growth, renewal, beginnings"
    },
    {
        "symbol": "ᛖ",
        "name": "Ehwaz",
        "transliteration": "E",
        "meaning": "movement, cooperation, progress"
    },
    {
        "symbol": "ᛗ",
        "name": "Mannaz",
        "transliteration": "M",
        "meaning": "humanity, community, cooperation"
    },
    {
        "symbol": "ᛚ",
        "name": "Laguz",
        "transliteration": "L",
        "meaning": "water, intuition, flow"
    },
    {
        "symbol": "ᛜ",
        "name": "Ingwaz",
        "transliteration": "NG",
        "meaning": "potential, completion, fertility"
    },
    {
        "symbol": "ᛞ",
        "name": "Dagaz",
        "transliteration": "D",
        "meaning": "daylight, breakthrough, transformation"
    },
    {
        "symbol": "ᛟ",
        "name": "Othala",
        "transliteration": "O",
        "meaning": "heritage, home, inheritance"
    }
]


# ============================================================
# MAIN APPLICATION WINDOW
# ============================================================

class RuneGenerator(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Elder Futhark Rune Formula Generator - Version 2"
        )

        self.resize(1100, 800)

        # Contains the currently generated runes.
        self.current_runes = []

        # Stores formulas generated during this session.
        self.formula_history = []

        self.setup_ui()
        self.apply_styles()


    # ========================================================
    # BUILD USER INTERFACE
    # ========================================================

    def setup_ui(self):

        central_widget = QWidget()

        self.main_layout = QVBoxLayout()

        self.main_layout.setContentsMargins(
            25,
            25,
            25,
            25
        )

        self.main_layout.setSpacing(15)

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        title = QLabel(
            "Elder Futhark Rune Formula Generator"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        title_font = QFont()
        title_font.setPointSize(25)
        title_font.setBold(True)

        title.setFont(title_font)

        self.main_layout.addWidget(title)

        subtitle = QLabel(
            "Generate unique random formulas using the "
            "24-rune Elder Futhark."
        )

        subtitle.setAlignment(
            Qt.AlignCenter
        )

        self.main_layout.addWidget(subtitle)

        # ----------------------------------------------------
        # TOP CONTROLS
        # ----------------------------------------------------

        controls = QHBoxLayout()

        formula_label = QLabel(
            "Formula Length:"
        )

        self.rune_count_combo = QComboBox()

        self.rune_count_combo.addItems([
            "5 Runes",
            "7 Runes",
            "9 Runes",
            "15 Runes"
        ])

        controls.addWidget(
            formula_label
        )

        controls.addWidget(
            self.rune_count_combo
        )

        controls.addStretch()

        # Generate button
        self.generate_button = QPushButton(
            "Generate Formula"
        )

        self.generate_button.clicked.connect(
            self.generate_formula
        )

        controls.addWidget(
            self.generate_button
        )

        self.main_layout.addLayout(
            controls
        )

        # ----------------------------------------------------
        # SEPARATOR
        # ----------------------------------------------------

        separator = QFrame()

        separator.setFrameShape(
            QFrame.HLine
        )

        self.main_layout.addWidget(
            separator
        )

        # ----------------------------------------------------
        # FORMULA DISPLAY
        # ----------------------------------------------------

        formula_title = QLabel(
            "Current Formula"
        )

        formula_title.setObjectName(
            "sectionTitle"
        )

        self.main_layout.addWidget(
            formula_title
        )

        self.formula_display = QLabel(
            "Generate a formula to begin"
        )

        self.formula_display.setAlignment(
            Qt.AlignCenter
        )

        self.formula_display.setWordWrap(
            True
        )

        formula_font = QFont()
        formula_font.setPointSize(34)

        self.formula_display.setFont(
            formula_font
        )

        self.formula_display.setMinimumHeight(
            90
        )

        self.formula_display.setObjectName(
            "formulaDisplay"
        )

        self.main_layout.addWidget(
            self.formula_display
        )

        # ----------------------------------------------------
        # FORMULA BUTTONS
        # ----------------------------------------------------

        formula_buttons = QHBoxLayout()

        copy_button = QPushButton(
            "Copy Formula"
        )

        copy_button.clicked.connect(
            self.copy_formula
        )

        regenerate_button = QPushButton(
            "Regenerate"
        )

        regenerate_button.clicked.connect(
            self.generate_formula
        )

        save_button = QPushButton(
            "Save Formula"
        )

        save_button.clicked.connect(
            self.save_formula
        )

        formula_buttons.addWidget(
            copy_button
        )

        formula_buttons.addWidget(
            regenerate_button
        )

        formula_buttons.addWidget(
            save_button
        )

        self.main_layout.addLayout(
            formula_buttons
        )

        # ----------------------------------------------------
        # RUNE CARD AREA
        # ----------------------------------------------------

        rune_section_title = QLabel(
            "Selected Runes"
        )

        rune_section_title.setObjectName(
            "sectionTitle"
        )

        self.main_layout.addWidget(
            rune_section_title
        )

        # Scroll area allows 15 rune cards to fit comfortably.
        self.scroll_area = QScrollArea()

        self.scroll_area.setWidgetResizable(
            True
        )

        self.rune_card_container = QWidget()

        self.rune_grid = QGridLayout()

        self.rune_grid.setSpacing(
            10
        )

        self.rune_card_container.setLayout(
            self.rune_grid
        )

        self.scroll_area.setWidget(
            self.rune_card_container
        )

        self.scroll_area.setMinimumHeight(
            260
        )

        self.main_layout.addWidget(
            self.scroll_area
        )

        # ----------------------------------------------------
        # HISTORY
        # ----------------------------------------------------

        history_header = QHBoxLayout()

        history_title = QLabel(
            "Formula History"
        )

        history_title.setObjectName(
            "sectionTitle"
        )

        clear_history_button = QPushButton(
            "Clear History"
        )

        clear_history_button.clicked.connect(
            self.clear_history
        )

        history_header.addWidget(
            history_title
        )

        history_header.addStretch()

        history_header.addWidget(
            clear_history_button
        )

        self.main_layout.addLayout(
            history_header
        )

        self.history_display = QTextEdit()

        self.history_display.setReadOnly(
            True
        )

        self.history_display.setMaximumHeight(
            150
        )

        self.main_layout.addWidget(
            self.history_display
        )

        central_widget.setLayout(
            self.main_layout
        )

        self.setCentralWidget(
            central_widget
        )


    # ========================================================
    # GENERATE RANDOM FORMULA
    # ========================================================

    def generate_formula(self):

        selected_option = (
            self.rune_count_combo.currentText()
        )

        rune_count = int(
            selected_option.split()[0]
        )

        # random.sample selects elements WITHOUT replacement.
        #
        # This guarantees that there will be no duplicated
        # rune inside the current formula.
        self.current_runes = random.sample(
            ELDER_FUTHARK,
            rune_count
        )

        formula = self.get_formula_string()

        self.formula_display.setText(
            formula
        )

        self.display_rune_cards()

        self.add_to_history(
            formula
        )


    # ========================================================
    # CREATE FORMULA STRING
    # ========================================================

    def get_formula_string(self):

        symbols = [
            rune["symbol"]
            for rune in self.current_runes
        ]

        return "  ".join(
            symbols
        )


    # ========================================================
    # DISPLAY RUNE CARDS
    # ========================================================

    def display_rune_cards(self):

        # Delete existing cards first.
        self.clear_rune_cards()

        # Number of rune cards displayed per row.
        columns = 5

        for index, rune in enumerate(
            self.current_runes
        ):

            row = index // columns
            column = index % columns

            card = self.create_rune_card(
                rune,
                index + 1
            )

            self.rune_grid.addWidget(
                card,
                row,
                column
            )


    # ========================================================
    # CREATE AN INDIVIDUAL RUNE CARD
    # ========================================================

    def create_rune_card(
        self,
        rune,
        number
    ):

        card = QFrame()

        card.setObjectName(
            "runeCard"
        )

        layout = QVBoxLayout()

        # Rune number
        number_label = QLabel(
            f"Rune {number}"
        )

        number_label.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            number_label
        )

        # Rune symbol
        symbol = QLabel(
            rune["symbol"]
        )

        symbol.setAlignment(
            Qt.AlignCenter
        )

        symbol_font = QFont()
        symbol_font.setPointSize(38)

        symbol.setFont(
            symbol_font
        )

        layout.addWidget(
            symbol
        )

        # Rune name
        name = QLabel(
            rune["name"]
        )

        name.setAlignment(
            Qt.AlignCenter
        )

        name_font = QFont()
        name_font.setBold(True)
        name_font.setPointSize(13)

        name.setFont(
            name_font
        )

        layout.addWidget(
            name
        )

        # Transliteration
        transliteration = QLabel(
            f"Sound: {rune['transliteration']}"
        )

        transliteration.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            transliteration
        )

        # Meaning
        meaning = QLabel(
            rune["meaning"]
        )

        meaning.setAlignment(
            Qt.AlignCenter
        )

        meaning.setWordWrap(
            True
        )

        layout.addWidget(
            meaning
        )

        card.setLayout(
            layout
        )

        return card


    # ========================================================
    # CLEAR EXISTING RUNE CARDS
    # ========================================================

    def clear_rune_cards(self):

        while self.rune_grid.count():

            item = self.rune_grid.takeAt(
                0
            )

            widget = item.widget()

            if widget:
                widget.deleteLater()


    # ========================================================
    # COPY FORMULA
    # ========================================================

    def copy_formula(self):

        if not self.current_runes:

            QMessageBox.information(
                self,
                "No Formula",
                "Generate a rune formula first."
            )

            return

        formula = self.get_formula_string()

        clipboard = (
            QApplication.clipboard()
        )

        clipboard.setText(
            formula
        )

        QMessageBox.information(
            self,
            "Copied",
            "Rune formula copied to the clipboard."
        )


    # ========================================================
    # SAVE FORMULA TO TEXT FILE
    # ========================================================

    def save_formula(self):

        if not self.current_runes:

            QMessageBox.information(
                self,
                "No Formula",
                "Generate a rune formula first."
            )

            return

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Rune Formula",
            "rune_formula.txt",
            "Text Files (*.txt)"
        )

        if not filename:
            return

        try:

            with open(
                filename,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(
                    "Elder Futhark Rune Formula\n"
                )

                file.write(
                    "==========================\n\n"
                )

                file.write(
                    self.get_formula_string()
                )

                file.write(
                    "\n\nRune Details\n"
                )

                file.write(
                    "--------------------------\n"
                )

                for index, rune in enumerate(
                    self.current_runes,
                    start=1
                ):

                    file.write(
                        f"{index}. "
                        f"{rune['symbol']} "
                        f"{rune['name']}\n"
                    )

                    file.write(
                        f"   Transliteration: "
                        f"{rune['transliteration']}\n"
                    )

                    file.write(
                        f"   Keywords: "
                        f"{rune['meaning']}\n\n"
                    )

            QMessageBox.information(
                self,
                "Saved",
                "Formula saved successfully."
            )

        except OSError as error:

            QMessageBox.critical(
                self,
                "Save Error",
                str(error)
            )


    # ========================================================
    # ADD FORMULA TO HISTORY
    # ========================================================

    def add_to_history(
        self,
        formula
    ):

        current_time = datetime.now().strftime(
            "%H:%M:%S"
        )

        history_entry = (
            f"[{current_time}] "
            f"{len(self.current_runes)} Runes: "
            f"{formula}"
        )

        self.formula_history.append(
            history_entry
        )

        self.update_history_display()


    # ========================================================
    # UPDATE HISTORY DISPLAY
    # ========================================================

    def update_history_display(self):

        self.history_display.setPlainText(
            "\n".join(
                self.formula_history
            )
        )

        # Automatically move to most recent history item.
        scrollbar = (
            self.history_display.verticalScrollBar()
        )

        scrollbar.setValue(
            scrollbar.maximum()
        )


    # ========================================================
    # CLEAR HISTORY
    # ========================================================

    def clear_history(self):

        self.formula_history.clear()

        self.history_display.clear()


    # ========================================================
    # APPLICATION STYLING
    # ========================================================

    def apply_styles(self):

        self.setStyleSheet(
            """

            QMainWindow {
                background-color: #141414;
            }

            QWidget {
                color: #eeeeee;
                font-size: 15px;
            }

            QLabel#sectionTitle {
                font-size: 18px;
                font-weight: bold;
            }

            QLabel#formulaDisplay {
                background-color: #202020;
                border: 1px solid #505050;
                border-radius: 10px;
                padding: 15px;
            }

            QComboBox {
                background-color: #282828;
                border: 1px solid #555555;
                border-radius: 6px;
                padding: 8px;
                min-width: 140px;
            }

            QComboBox:hover {
                border: 1px solid #888888;
            }

            QPushButton {
                background-color: #303030;
                border: 1px solid #555555;
                border-radius: 7px;
                padding: 9px 15px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #424242;
                border: 1px solid #888888;
            }

            QPushButton:pressed {
                background-color: #202020;
            }

            QTextEdit {
                background-color: #202020;
                border: 1px solid #505050;
                border-radius: 8px;
                padding: 8px;
            }

            QScrollArea {
                background-color: transparent;
                border: none;
            }

            QWidget#qt_scrollarea_viewport {
                background-color: #141414;
            }

            QFrame#runeCard {
                background-color: #242424;
                border: 1px solid #505050;
                border-radius: 10px;
                min-width: 150px;
                min-height: 180px;
            }

            QFrame#runeCard:hover {
                background-color: #303030;
                border: 1px solid #888888;
            }

            """
        )


# ============================================================
# MAIN
# ============================================================

def main():

    app = QApplication(
        sys.argv
    )

    window = RuneGenerator()

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()