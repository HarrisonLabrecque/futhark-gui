# gui/generator_page.py

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
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
    QInputDialog,
    QFrame
)

from gui.rune_card import RuneCard

from utils.formula_manager import FormulaManager
from utils.history_manager import HistoryManager
from utils.saved_formula_manager import SavedFormulaManager


class GeneratorPage(QWidget):
    """
    Main rune formula generator page.

    Handles:
        - Formula generation
        - Rune card display
        - Copying formulas
        - TXT export
        - Saving formulas
        - Session history
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Currently generated runes.
        self.current_runes = []

        # Manager for session history.
        self.history_manager = HistoryManager()

        # Manager for permanent JSON storage.
        self.saved_formula_manager = SavedFormulaManager()

        # Build the page.
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

        # ====================================================
        # SUBTITLE
        # ====================================================

        subtitle = QLabel(
            "Generate unique random formulas using "
            "the 24-rune Elder Futhark."
        )

        subtitle.setAlignment(
            Qt.AlignCenter
        )

        subtitle.setWordWrap(
            True
        )

        main_layout.addWidget(
            subtitle
        )

        # ====================================================
        # FORMULA CONTROLS
        # ====================================================

        controls_layout = QHBoxLayout()

        formula_length_label = QLabel(
            "Formula Length:"
        )

        controls_layout.addWidget(
            formula_length_label
        )

        # Formula size selection.
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

        # Generate button.
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

        # ====================================================
        # SEPARATOR
        # ====================================================

        separator = QFrame()

        separator.setFrameShape(
            QFrame.HLine
        )

        separator.setFrameShadow(
            QFrame.Sunken
        )

        main_layout.addWidget(
            separator
        )

        # ====================================================
        # CURRENT FORMULA
        # ====================================================

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

        # ====================================================
        # FORMULA ACTIONS
        # ====================================================

        action_layout = QHBoxLayout()

        # Copy formula.
        self.copy_button = QPushButton(
            "Copy Formula"
        )

        self.copy_button.clicked.connect(
            self.copy_formula
        )

        action_layout.addWidget(
            self.copy_button
        )

        # Regenerate formula.
        self.regenerate_button = QPushButton(
            "Regenerate"
        )

        self.regenerate_button.clicked.connect(
            self.generate_formula
        )

        action_layout.addWidget(
            self.regenerate_button
        )

        # Export formula.
        self.export_button = QPushButton(
            "Export to TXT"
        )

        self.export_button.clicked.connect(
            self.export_formula
        )

        action_layout.addWidget(
            self.export_button
        )

        # Save formula permanently.
        self.save_collection_button = QPushButton(
            "Save to Collection"
        )

        self.save_collection_button.clicked.connect(
            self.save_to_collection
        )

        action_layout.addWidget(
            self.save_collection_button
        )

        main_layout.addLayout(
            action_layout
        )

        # ====================================================
        # SELECTED RUNES
        # ====================================================

        rune_title = QLabel(
            "Selected Runes"
        )

        rune_title.setObjectName(
            "sectionTitle"
        )

        main_layout.addWidget(
            rune_title
        )

        # ====================================================
        # RUNE CARD AREA
        # ====================================================

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

        # ====================================================
        # HISTORY
        # ====================================================

        history_header = QHBoxLayout()

        history_title = QLabel(
            "Session History"
        )

        history_title.setObjectName(
            "sectionTitle"
        )

        history_header.addWidget(
            history_title
        )

        history_header.addStretch()

        self.clear_history_button = QPushButton(
            "Clear History"
        )

        self.clear_history_button.clicked.connect(
            self.clear_history
        )

        history_header.addWidget(
            self.clear_history_button
        )

        main_layout.addLayout(
            history_header
        )

        # History text display.
        self.history_display = QTextEdit()

        self.history_display.setReadOnly(
            True
        )

        self.history_display.setPlaceholderText(
            "Generated formulas will appear here..."
        )

        self.history_display.setMaximumHeight(
            150
        )

        main_layout.addWidget(
            self.history_display
        )

        # Apply layout to this page.
        self.setLayout(
            main_layout
        )


    # ========================================================
    # GENERATE FORMULA
    # ========================================================

    def generate_formula(self):
        """
        Generate a new random rune formula.
        """

        selected_option = (
            self.rune_count_combo.currentText()
        )

        # Example:
        # "5 Runes" -> 5
        rune_count = int(
            selected_option.split()[0]
        )

        try:

            # FormulaManager uses random.sample(),
            # preventing duplicate runes.
            self.current_runes = (
                FormulaManager.generate_formula(
                    rune_count
                )
            )

        except ValueError as error:

            QMessageBox.critical(
                self,
                "Generation Error",
                str(error)
            )

            return

        # Convert selected runes into a display string.
        formula = (
            FormulaManager.get_formula_string(
                self.current_runes
            )
        )

        self.formula_display.setText(
            formula
        )

        # Update visual rune cards.
        self.display_rune_cards()

        # Store in session history.
        self.add_to_history(
            formula
        )


    # ========================================================
    # DISPLAY RUNE CARDS
    # ========================================================

    def display_rune_cards(self):
        """
        Display the generated runes using RuneCard widgets.
        """

        self.clear_rune_cards()

        # Five rune cards per row.
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
        """
        Remove all displayed rune cards.
        """

        while self.rune_grid.count():

            item = self.rune_grid.takeAt(
                0
            )

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()


    # ========================================================
    # COPY FORMULA
    # ========================================================

    def copy_formula(self):
        """
        Copy the current formula to the clipboard.
        """

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
    # EXPORT FORMULA
    # ========================================================

    def export_formula(self):
        """
        Export the current formula to a TXT file.
        """

        if not self.current_runes:

            QMessageBox.information(
                self,
                "No Formula",
                "Generate a rune formula first."
            )

            return

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Rune Formula",
            "rune_formula.txt",
            "Text Files (*.txt)"
        )

        # User cancelled the file dialog.
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
                    "\n\n"
                )

                file.write(
                    f"Rune Count: "
                    f"{len(self.current_runes)}\n"
                )

                file.write(
                    "\nRune Details\n"
                )

                file.write(
                    "--------------------------\n"
                )

                file.write(
                    details
                )

            QMessageBox.information(
                self,
                "Export Complete",
                "The formula was exported successfully."
            )

        except OSError as error:

            QMessageBox.critical(
                self,
                "Export Error",
                str(error)
            )


    # ========================================================
    # SAVE TO COLLECTION
    # ========================================================

    def save_to_collection(self):
        """
        Save the current formula permanently to
        saved/formulas.json.
        """

        if not self.current_runes:

            QMessageBox.information(
                self,
                "No Formula",
                "Generate a rune formula first."
            )

            return

        # Ask user to name the formula.
        name, accepted = QInputDialog.getText(
            self,
            "Save Formula",
            "Formula name:"
        )

        # User pressed Cancel.
        if not accepted:
            return

        name = name.strip()

        # Give unnamed formulas a default name.
        if not name:
            name = "Unnamed Formula"

        try:

            self.saved_formula_manager.save_formula(
                name,
                self.current_runes
            )

            QMessageBox.information(
                self,
                "Formula Saved",
                f'"{name}" was added to your '
                f"saved formula collection."
            )

        except OSError as error:

            QMessageBox.critical(
                self,
                "Save Error",
                str(error)
            )


    # ========================================================
    # ADD TO HISTORY
    # ========================================================

    def add_to_history(self, formula):
        """
        Add the current formula to session history.
        """

        self.history_manager.add_formula(
            self.current_runes,
            formula
        )

        self.update_history_display()


    # ========================================================
    # UPDATE HISTORY
    # ========================================================

    def update_history_display(self):
        """
        Display formatted session history.
        """

        history_text = (
            self.history_manager.get_formatted_history()
        )

        self.history_display.setPlainText(
            history_text
        )

        # Scroll to newest entry.
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
        """
        Clear all session history.
        """

        self.history_manager.clear_history()

        self.history_display.clear()