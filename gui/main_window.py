# gui/main_window.py

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
    QInputDialog,
    QFrame
)

# Import our custom GUI component.
from gui.rune_card import RuneCard

# Import application managers.
from utils.formula_manager import FormulaManager
from utils.history_manager import HistoryManager
from utils.saved_formula_manager import SavedFormulaManager


class RuneGeneratorWindow(QMainWindow):
    """
    Main window for the Elder Futhark Rune Formula Generator.

    Responsibilities:
        - Display the GUI.
        - Generate rune formulas.
        - Display rune cards.
        - Copy formulas.
        - Export formulas to TXT files.
        - Save formulas permanently to JSON.
        - Display session history.
    """

    def __init__(self):
        super().__init__()

        # ----------------------------------------------------
        # WINDOW SETTINGS
        # ----------------------------------------------------

        self.setWindowTitle(
            "Elder Futhark Rune Formula Generator"
        )

        self.resize(
            1100,
            800
        )

        # ----------------------------------------------------
        # CURRENT FORMULA
        # ----------------------------------------------------

        # Stores the currently generated runes.
        self.current_runes = []

        # ----------------------------------------------------
        # MANAGERS
        # ----------------------------------------------------

        # Handles formulas generated during this session.
        self.history_manager = HistoryManager()

        # Handles formulas permanently stored in JSON.
        self.saved_formula_manager = SavedFormulaManager()

        # Build the interface.
        self.setup_ui()


    # ========================================================
    # BUILD USER INTERFACE
    # ========================================================

    def setup_ui(self):

        # Central widget required by QMainWindow.
        central_widget = QWidget()

        # Main vertical layout.
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

        # Dropdown for choosing the number of runes.
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

        # Push the Generate button to the right.
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
        # CURRENT FORMULA TITLE
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

        # ====================================================
        # CURRENT FORMULA DISPLAY
        # ====================================================

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

        # Used by styles.qss.
        self.formula_display.setObjectName(
            "formulaDisplay"
        )

        main_layout.addWidget(
            self.formula_display
        )

        # ====================================================
        # FORMULA ACTION BUTTONS
        # ====================================================

        action_layout = QHBoxLayout()

        # ----------------------------------------------------
        # COPY
        # ----------------------------------------------------

        self.copy_button = QPushButton(
            "Copy Formula"
        )

        self.copy_button.clicked.connect(
            self.copy_formula
        )

        action_layout.addWidget(
            self.copy_button
        )

        # ----------------------------------------------------
        # REGENERATE
        # ----------------------------------------------------

        self.regenerate_button = QPushButton(
            "Regenerate"
        )

        self.regenerate_button.clicked.connect(
            self.generate_formula
        )

        action_layout.addWidget(
            self.regenerate_button
        )

        # ----------------------------------------------------
        # EXPORT TO TXT
        # ----------------------------------------------------

        self.export_button = QPushButton(
            "Export to TXT"
        )

        self.export_button.clicked.connect(
            self.export_formula
        )

        action_layout.addWidget(
            self.export_button
        )

        # ----------------------------------------------------
        # SAVE TO COLLECTION
        # ----------------------------------------------------

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
        # SELECTED RUNES TITLE
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
        # RUNE CARD SCROLL AREA
        # ====================================================

        self.scroll_area = QScrollArea()

        self.scroll_area.setWidgetResizable(
            True
        )

        # Container holds the rune cards.
        self.rune_container = QWidget()

        # Grid organizes the rune cards.
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
        # HISTORY HEADER
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

        # Clear history button.
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

        # ====================================================
        # HISTORY DISPLAY
        # ====================================================

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

        # ====================================================
        # FINISH CENTRAL WIDGET
        # ====================================================

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
        """
        Generate a new random formula using the
        selected number of runes.
        """

        # Example:
        #
        # "5 Runes" -> 5
        # "15 Runes" -> 15

        selected_option = (
            self.rune_count_combo.currentText()
        )

        rune_count = int(
            selected_option.split()[0]
        )

        try:

            # FormulaManager uses random.sample(),
            # which prevents duplicate runes.
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

        # Convert rune dictionaries into a
        # displayable formula string.
        formula = (
            FormulaManager.get_formula_string(
                self.current_runes
            )
        )

        # Display the formula.
        self.formula_display.setText(
            formula
        )

        # Create visual cards.
        self.display_rune_cards()

        # Add formula to session history.
        self.add_to_history(
            formula
        )


    # ========================================================
    # DISPLAY RUNE CARDS
    # ========================================================

    def display_rune_cards(self):
        """
        Display each generated rune using the
        reusable RuneCard widget.
        """

        # Remove old cards first.
        self.clear_rune_cards()

        # Display five rune cards per row.
        columns = 5

        for index, rune in enumerate(
            self.current_runes
        ):

            # Determine the grid position.
            row = index // columns
            column = index % columns

            # Create a RuneCard.
            rune_card = RuneCard(
                rune,
                index + 1
            )

            # Add the card to the grid.
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
        Remove all currently displayed RuneCard widgets.
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
        Copy the current rune formula to the
        operating system clipboard.
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
    # EXPORT FORMULA TO TXT
    # ========================================================

    def export_formula(self):
        """
        Export the current formula and its rune
        information to a normal text file.
        """

        if not self.current_runes:

            QMessageBox.information(
                self,
                "No Formula",
                "Generate a rune formula first."
            )

            return

        # Ask where the text file should be saved.
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Rune Formula",
            "rune_formula.txt",
            "Text Files (*.txt)"
        )

        # User cancelled.
        if not filename:
            return

        # Get formula string.
        formula = (
            FormulaManager.get_formula_string(
                self.current_runes
            )
        )

        # Get formatted rune information.
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
    # SAVE FORMULA TO COLLECTION
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

        # Ask the user to give the formula a name.
        name, accepted = QInputDialog.getText(
            self,
            "Save Formula",
            "Formula name:"
        )

        # User pressed Cancel.
        if not accepted:
            return

        # Remove whitespace from beginning/end.
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
    # ADD TO SESSION HISTORY
    # ========================================================

    def add_to_history(self, formula):
        """
        Send the generated formula to HistoryManager.
        """

        self.history_manager.add_formula(
            self.current_runes,
            formula
        )

        self.update_history_display()


    # ========================================================
    # UPDATE HISTORY DISPLAY
    # ========================================================

    def update_history_display(self):
        """
        Retrieve formatted history from HistoryManager
        and display it.
        """

        history_text = (
            self.history_manager.get_formatted_history()
        )

        self.history_display.setPlainText(
            history_text
        )

        # Automatically scroll to the newest entry.
        scrollbar = (
            self.history_display.verticalScrollBar()
        )

        scrollbar.setValue(
            scrollbar.maximum()
        )


    # ========================================================
    # CLEAR SESSION HISTORY
    # ========================================================

    def clear_history(self):
        """
        Remove all formula history from the
        current application session.
        """

        self.history_manager.clear_history()

        self.history_display.clear()