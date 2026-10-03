# gui/saved_formulas.py

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QListWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QScrollArea,
    QMessageBox,
    QSplitter
)

from gui.rune_card import RuneCard
from utils.saved_formula_manager import SavedFormulaManager
from utils.formula_manager import FormulaManager


class SavedFormulasPage(QWidget):
    """
    Page used to browse and manage formulas that
    were permanently saved to formulas.json.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.saved_formula_manager = SavedFormulaManager()

        # Contains the formulas currently loaded from JSON.
        self.saved_formulas = []

        # Currently selected formula index.
        self.selected_index = None

        self.setup_ui()

        # Load saved formulas when the page is created.
        self.refresh_formulas()


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
            "Saved Formulas"
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
            "View and manage rune formulas saved "
            "to your collection."
        )

        description.setAlignment(
            Qt.AlignCenter
        )

        main_layout.addWidget(
            description
        )

        # ====================================================
        # SPLITTER
        # ====================================================

        splitter = QSplitter(
            Qt.Horizontal
        )

        # ====================================================
        # LEFT SIDE - FORMULA LIST
        # ====================================================

        list_container = QWidget()

        list_layout = QVBoxLayout()

        list_title = QLabel(
            "Collection"
        )

        list_title.setObjectName(
            "sectionTitle"
        )

        list_layout.addWidget(
            list_title
        )

        # List containing formula names.
        self.formula_list = QListWidget()

        self.formula_list.setObjectName(
            "formulaList"
        )

        # When the selected formula changes,
        # display its details.
        self.formula_list.currentRowChanged.connect(
            self.display_selected_formula
        )

        list_layout.addWidget(
            self.formula_list
        )

        # ----------------------------------------------------
        # REFRESH BUTTON
        # ----------------------------------------------------

        self.refresh_button = QPushButton(
            "Refresh"
        )

        self.refresh_button.clicked.connect(
            self.refresh_formulas
        )

        list_layout.addWidget(
            self.refresh_button
        )

        list_container.setLayout(
            list_layout
        )

        splitter.addWidget(
            list_container
        )

        # ====================================================
        # RIGHT SIDE - FORMULA DETAILS
        # ====================================================

        detail_container = QWidget()

        detail_layout = QVBoxLayout()

        # Formula name.
        self.formula_name = QLabel(
            "Select a saved formula"
        )

        self.formula_name.setObjectName(
            "savedFormulaTitle"
        )

        self.formula_name.setAlignment(
            Qt.AlignCenter
        )

        detail_layout.addWidget(
            self.formula_name
        )

        # Formula metadata.
        self.formula_information = QLabel(
            ""
        )

        self.formula_information.setAlignment(
            Qt.AlignCenter
        )

        detail_layout.addWidget(
            self.formula_information
        )

        # ----------------------------------------------------
        # FORMULA SYMBOLS
        # ----------------------------------------------------

        self.formula_display = QLabel(
            ""
        )

        self.formula_display.setObjectName(
            "formulaDisplay"
        )

        self.formula_display.setAlignment(
            Qt.AlignCenter
        )

        self.formula_display.setWordWrap(
            True
        )

        formula_font = QFont()
        formula_font.setPointSize(30)

        self.formula_display.setFont(
            formula_font
        )

        detail_layout.addWidget(
            self.formula_display
        )

        # ====================================================
        # RUNE CARDS
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

        detail_layout.addWidget(
            self.scroll_area
        )

        # ====================================================
        # ACTION BUTTONS
        # ====================================================

        action_layout = QHBoxLayout()

        # Delete selected formula.
        self.delete_button = QPushButton(
            "Delete Formula"
        )

        self.delete_button.clicked.connect(
            self.delete_selected_formula
        )

        action_layout.addWidget(
            self.delete_button
        )

        # Clear entire collection.
        self.clear_button = QPushButton(
            "Clear Collection"
        )

        self.clear_button.clicked.connect(
            self.clear_collection
        )

        action_layout.addWidget(
            self.clear_button
        )

        detail_layout.addLayout(
            action_layout
        )

        detail_container.setLayout(
            detail_layout
        )

        splitter.addWidget(
            detail_container
        )

        # Give the details side more space.
        splitter.setStretchFactor(
            0,
            1
        )

        splitter.setStretchFactor(
            1,
            3
        )

        main_layout.addWidget(
            splitter
        )

        self.setLayout(
            main_layout
        )


    # ========================================================
    # REFRESH FORMULAS
    # ========================================================

    def refresh_formulas(self):
        """
        Reload saved formulas from formulas.json.
        """

        self.saved_formulas = (
            self.saved_formula_manager.load_formulas()
        )

        self.formula_list.clear()

        # Add each saved formula to the list.
        for formula in self.saved_formulas:

            name = formula.get(
                "name",
                "Unnamed Formula"
            )

            rune_count = formula.get(
                "rune_count",
                0
            )

            self.formula_list.addItem(
                f"{name} ({rune_count} Runes)"
            )

        # Reset selected formula.
        self.selected_index = None

        self.clear_formula_display()


    # ========================================================
    # DISPLAY SELECTED FORMULA
    # ========================================================

    def display_selected_formula(
        self,
        index
    ):
        """
        Display the formula selected in the collection.
        """

        if (
            index < 0
            or index >= len(self.saved_formulas)
        ):
            return

        self.selected_index = index

        formula_data = (
            self.saved_formulas[index]
        )

        name = formula_data.get(
            "name",
            "Unnamed Formula"
        )

        created = formula_data.get(
            "created",
            "Unknown"
        )

        runes = formula_data.get(
            "runes",
            []
        )

        # ----------------------------------------------------
        # DISPLAY NAME
        # ----------------------------------------------------

        self.formula_name.setText(
            name
        )

        # ----------------------------------------------------
        # DISPLAY METADATA
        # ----------------------------------------------------

        self.formula_information.setText(
            f"Created: {created}  |  "
            f"Runes: {len(runes)}"
        )

        # ----------------------------------------------------
        # DISPLAY FORMULA
        # ----------------------------------------------------

        formula_string = (
            FormulaManager.get_formula_string(
                runes
            )
        )

        self.formula_display.setText(
            formula_string
        )

        # ----------------------------------------------------
        # DISPLAY RUNE CARDS
        # ----------------------------------------------------

        self.display_rune_cards(
            runes
        )


    # ========================================================
    # DISPLAY RUNE CARDS
    # ========================================================

    def display_rune_cards(
        self,
        runes
    ):
        """
        Display rune cards belonging to the
        selected saved formula.
        """

        self.clear_rune_cards()

        columns = 4

        for index, rune in enumerate(
            runes
        ):

            row = index // columns
            column = index % columns

            card = RuneCard(
                rune,
                index + 1
            )

            self.rune_grid.addWidget(
                card,
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

            if widget is not None:
                widget.deleteLater()


    # ========================================================
    # CLEAR FORMULA DISPLAY
    # ========================================================

    def clear_formula_display(self):

        self.formula_name.setText(
            "Select a saved formula"
        )

        self.formula_information.clear()

        self.formula_display.clear()

        self.clear_rune_cards()


    # ========================================================
    # DELETE SELECTED FORMULA
    # ========================================================

    def delete_selected_formula(self):
        """
        Delete the currently selected formula.
        """

        if self.selected_index is None:

            QMessageBox.information(
                self,
                "No Formula Selected",
                "Select a saved formula first."
            )

            return

        formula = (
            self.saved_formulas[
                self.selected_index
            ]
        )

        name = formula.get(
            "name",
            "Unnamed Formula"
        )

        # Ask before permanently deleting.
        response = QMessageBox.question(
            self,
            "Delete Formula",
            f'Delete "{name}"?',
            QMessageBox.Yes
            | QMessageBox.No,
            QMessageBox.No
        )

        if response != QMessageBox.Yes:
            return

        success = (
            self.saved_formula_manager.delete_formula(
                self.selected_index
            )
        )

        if success:

            self.refresh_formulas()

            QMessageBox.information(
                self,
                "Formula Deleted",
                f'"{name}" was deleted.'
            )


    # ========================================================
    # CLEAR COLLECTION
    # ========================================================

    def clear_collection(self):
        """
        Permanently remove all saved formulas.
        """

        if not self.saved_formulas:

            QMessageBox.information(
                self,
                "Collection Empty",
                "There are no saved formulas to delete."
            )

            return

        response = QMessageBox.question(
            self,
            "Clear Collection",
            "Delete all saved formulas?\n\n"
            "This cannot be undone.",
            QMessageBox.Yes
            | QMessageBox.No,
            QMessageBox.No
        )

        if response != QMessageBox.Yes:
            return

        self.saved_formula_manager.clear_formulas()

        self.refresh_formulas()

        QMessageBox.information(
            self,
            "Collection Cleared",
            "All saved formulas were deleted."
        )