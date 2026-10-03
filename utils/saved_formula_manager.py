# utils/saved_formula_manager.py

import json

from datetime import datetime
from pathlib import Path


class SavedFormulaManager:
    """
    Handles permanently saved rune formulas.

    User data is stored outside the application directory
    so that it continues working when the program is
    packaged with PyInstaller.

    Windows example:

        C:\\Users\\Username\\.elder_futhark_generator\\formulas.json
    """

    def __init__(self):

        # ----------------------------------------------------
        # USER DATA DIRECTORY
        # ----------------------------------------------------
        #
        # Path.home() returns the current user's home folder.
        #
        # Example:
        #
        # C:\Users\Harrison
        #
        # The program will create:
        #
        # C:\Users\Harrison\.elder_futhark_generator
        #
        # This allows saved formulas to remain available
        # even after the application is packaged.
        # ----------------------------------------------------

        self.save_directory = (
            Path.home()
            / ".elder_futhark_generator"
        )

        # JSON file containing permanently saved formulas.
        self.save_file = (
            self.save_directory
            / "formulas.json"
        )

        # Make sure the storage directory and JSON file exist.
        self.create_storage()


    # ========================================================
    # CREATE STORAGE
    # ========================================================

    def create_storage(self):
        """
        Create the application's user data directory and
        formulas.json file if they do not already exist.
        """

        # Create directory if necessary.
        self.save_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        # Create an empty JSON database if one
        # does not already exist.
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
        Load all saved formulas from formulas.json.

        Returns an empty list if the file cannot be read
        or contains invalid JSON.
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

                # Make sure the JSON database contains
                # the expected list structure.
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

    def write_formulas(
        self,
        formulas
    ):
        """
        Write the complete formula collection
        to formulas.json.
        """

        # Make sure the storage directory still exists.
        self.save_directory.mkdir(
            parents=True,
            exist_ok=True
        )

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
        Save a new rune formula permanently.

        Parameters:

            name:
                User-provided name for the formula.

            runes:
                List containing the rune dictionaries.
        """

        # Load existing formulas.
        formulas = self.load_formulas()

        # Build the new saved formula.
        formula = {

            "name": name,

            "created": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "rune_count": len(
                runes
            ),

            "runes": runes
        }

        # Add new formula to collection.
        formulas.append(
            formula
        )

        # Save updated collection.
        self.write_formulas(
            formulas
        )

        return formula


    # ========================================================
    # DELETE FORMULA
    # ========================================================

    def delete_formula(
        self,
        index
    ):
        """
        Delete one formula using its collection index.

        Returns True if the formula was deleted.
        Returns False if the index was invalid.
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
    # CLEAR FORMULAS
    # ========================================================

    def clear_formulas(self):
        """
        Permanently remove every saved formula
        from the collection.
        """

        self.write_formulas(
            []
        )


    # ========================================================
    # GET STORAGE PATH
    # ========================================================

    def get_storage_path(self):
        """
        Return the location of formulas.json.

        This can later be useful for an About,
        Settings, or Debug page.
        """

        return self.save_file