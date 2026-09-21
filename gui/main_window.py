# gui/main_window.py

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

from gui.rune_card import RuneCard
from utils.formula_manager import FormulaManager


class RuneGeneratorWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Elder Futhark Rune Formula Generator"
        )

        self.resize(
            1100,
            800
        )

        # Currently generated rune formula.
        self.current_runes = []

        # Stores formulas generated during
        # the current application session.
        self.formula_history = []

        self.setup_ui()
        self.apply_styles()


    # ========================================================
    # BUILD USER INTERFACE
    # ========================================================

    def setup_ui(self):

        central_widget = QWidget()

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

        title.setFont(
            title_font
        )

        main_layout.addWidget(
            title
        )

        # ----------------------------------------------------
        # SUBTITLE
        # ----------------------------------------------------

        subtitle = QLabel(
            "Generate unique random formulas using "
            "the 24-rune Elder Futhark."
        )

        subtitle.setAlignment(
            Qt.AlignCenter
        )

        main_layout.addWidget(
            subtitle
        )

        # ----------------------------------------------------
        # FORMULA CONTROLS
        # ----------------------------------------------------

        controls_layout = QHBoxLayout()

        controls_layout.addWidget(
            QLabel("Formula Length:")
        )

        self.rune_count_combo = QComboBox()

        self.rune_count_combo.addItems([
            "5 Runes",
            "7 Runes",
            "9 Runes",
            "15 Runes"
        ])

        controls_layout.addWidget(
            self.rune_count_combo
        )

        controls_layout.addStretch()

        self.generate_button = QPushButton(
            "Generate Formula"
        )

        self.generate_button.clicked.connect(
            self.generate_formula
        )

        controls_layout.addWidget(
            self.generate_button
        )

        main_layout.addLayout(
            controls_layout
        )

        # ----------------------------------------------------
        # SEPARATOR
        # ----------------------------------------------------

        separator = QFrame()

        separator.setFrameShape(
            QFrame.HLine
        )

        main_layout.addWidget(
            separator
        )

        # ----------------------------------------------------
        # CURRENT FORMULA
        # ----------------------------------------------------

        formula_title = QLabel(
            "Current Formula"
        )

        formula_title.setObjectName(
            "sectionTitle"
        )

        main_layout.addWidget(
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

        main_layout.addWidget(
            self.formula_display
        )

        # ----------------------------------------------------
        # FORMULA ACTION BUTTONS
        # ----------------------------------------------------

        action_layout = QHBoxLayout()

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

        action_layout.addWidget(
            copy_button
        )

        action_layout.addWidget(
            regenerate_button
        )

        action_layout.addWidget(
            save_button
        )

        main_layout.addLayout(
            action_layout
        )

        # ----------------------------------------------------
        # RUNE CARDS
        # ----------------------------------------------------

        rune_title = QLabel(
            "Selected Runes"
        )

        rune_title.setObjectName(
            "sectionTitle"
        )

        main_layout.addWidget(
            rune_title
        )

        self.scroll_area = QScrollArea()

        self.scroll_area.setWidgetResizable(
            True
        )

        self.rune_container = QWidget()

        self.rune_grid = QGridLayout()

        self.rune_grid.setSpacing(
            10
        )

        self.rune_container.setLayout(
            self.rune_grid
        )

        self.scroll_area.setWidget(
            self.rune_container
        )

        self.scroll_area.setMinimumHeight(
            260
        )

        main_layout.addWidget(
            self.scroll_area
        )

        # ----------------------------------------------------
        # HISTORY HEADER
        # ----------------------------------------------------

        history_header = QHBoxLayout()

        history_title = QLabel(
            "Formula History"
        )

        history_title.setObjectName(
            "sectionTitle"
        )

        clear_button = QPushButton(
            "Clear History"
        )

        clear_button.clicked.connect(
            self.clear_history
        )

        history_header.addWidget(
            history_title
        )

        history_header.addStretch()

        history_header.addWidget(
            clear_button
        )

        main_layout.addLayout(
            history_header
        )

        # ----------------------------------------------------
        # HISTORY DISPLAY
        # ----------------------------------------------------

        self.history_display = QTextEdit()

        self.history_display.setReadOnly(
            True
        )

        self.history_display.setMaximumHeight(
            150
        )

        main_layout.addWidget(
            self.history_display
        )

        # ----------------------------------------------------
        # SET CENTRAL WIDGET
        # ----------------------------------------------------

        central_widget.setLayout(
            main_layout
        )

        self.setCentralWidget(
            central_widget
        )


    # ========================================================
    # GENERATE FORMULA
    # ========================================================

    def generate_formula(self):

        selected_option = (
            self.rune_count_combo.currentText()
        )

        rune_count = int(
            selected_option.split()[0]
        )

        # FormulaManager performs the random
        # no-repeat selection.
        self.current_runes = (
            FormulaManager.generate_formula(
                rune_count
            )
        )

        formula = (
            FormulaManager.get_formula_string(
                self.current_runes
            )
        )

        self.formula_display.setText(
            formula
        )

        self.display_rune_cards()

        self.add_to_history(
            formula
        )


    # ========================================================
    # DISPLAY RUNE CARDS
    # ========================================================

    def display_rune_cards(self):

        self.clear_rune_cards()

        # Five cards per row.
        columns = 5

        for index, rune in enumerate(
            self.current_runes
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


    # ========================================================
    # CLEAR RUNE CARDS
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

        formula = (
            FormulaManager.get_formula_string(
                self.current_runes
            )
        )

        QApplication.clipboard().setText(
            formula
        )

        QMessageBox.information(
            self,
            "Copied",
            "Rune formula copied to the clipboard."
        )


    # ========================================================
    # SAVE FORMULA
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

        formula = (
            FormulaManager.get_formula_string(
                self.current_runes
            )
        )

        details = (
            FormulaManager.get_formula_details(
                self.current_runes
            )
        )

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
                    formula
                )

                file.write(
                    "\n\nRune Details\n"
                )

                file.write(
                    "--------------------------\n"
                )

                file.write(
                    details
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
    # HISTORY
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


    def update_history_display(self):

        self.history_display.setPlainText(
            "\n".join(
                self.formula_history
            )
        )

        scrollbar = (
            self.history_display.verticalScrollBar()
        )

        scrollbar.setValue(
            scrollbar.maximum()
        )


    def clear_history(self):

        self.formula_history.clear()

        self.history_display.clear()


    # ========================================================
    # APPLICATION STYLE
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