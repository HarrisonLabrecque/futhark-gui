# utils/saved_formula_manager.py

import json

from datetime import datetime
from pathlib import Path


class SavedFormulaManager:
    """
    Handles permanently saved rune formulas.

    Saved formulas are stored inside:
        saved/formulas.json
    """

    def __init__(self):

        # Find the root project directory.
        self.project_root = (
            Path(__file__).resolve().parent.parent
        )

        # Saved data directory.
        self.save_directory = (
            self.project_root / "saved"
        )

        # JSON database file.
        self.save_file = (
            self.save_directory / "formulas.json"
        )

        # Make sure the directory/file exists.
        self.create_storage()


    # ========================================================
    # CREATE STORAGE
    # ========================================================

    def create_storage(self):
        """
        Create the saved directory and JSON file
        if they do not already exist.
        """

        self.save_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.save_file.exists():

            with open(
                self.save_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    [],
                    file,
                    indent=4,
                    ensure_ascii=False
                )


    # ========================================================
    # LOAD FORMULAS
    # ========================================================

    def load_formulas(self):
        """
        Load all saved formulas from JSON.
        """

        try:

            with open(
                self.save_file,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(
                    file
                )

                if isinstance(data, list):
                    return data

                return []

        except (
            json.JSONDecodeError,
            OSError
        ):

            return []


    # ========================================================
    # WRITE FORMULAS
    # ========================================================

    def write_formulas(self, formulas):
        """
        Write the complete formula list to JSON.
        """

        with open(
            self.save_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                formulas,
                file,
                indent=4,
                ensure_ascii=False
            )


    # ========================================================
    # SAVE FORMULA
    # ========================================================

    def save_formula(
        self,
        name,
        runes
    ):
        """
        Permanently save a rune formula.
        """

        formulas = self.load_formulas()

        formula = {
            "name": name,

            "created": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "rune_count": len(runes),

            "runes": runes
        }

        formulas.append(
            formula
        )

        self.write_formulas(
            formulas
        )

        return formula


    # ========================================================
    # DELETE FORMULA
    # ========================================================

    def delete_formula(self, index):
        """
        Delete a saved formula using its list index.
        """

        formulas = self.load_formulas()

        if 0 <= index < len(formulas):

            formulas.pop(
                index
            )

            self.write_formulas(
                formulas
            )

            return True

        return False


    # ========================================================
    # CLEAR SAVED FORMULAS
    # ========================================================

    def clear_formulas(self):
        """
        Delete all permanently saved formulas.
        """

        self.write_formulas(
            []
        )