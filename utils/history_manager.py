# utils/history_manager.py

from datetime import datetime


class HistoryManager:
    """
    Manages rune formulas generated during the
    current application session.
    """

    def __init__(self):

        # Stores history entries.
        self.history = []


    # ========================================================
    # ADD FORMULA
    # ========================================================

    def add_formula(self, runes, formula):
        """
        Add a generated formula to the history.

        runes:
            List containing the selected rune dictionaries.

        formula:
            String containing the displayed rune symbols.
        """

        current_time = datetime.now().strftime(
            "%H:%M:%S"
        )

        entry = {
            "time": current_time,
            "count": len(runes),
            "formula": formula
        }

        self.history.append(
            entry
        )


    # ========================================================
    # GET HISTORY
    # ========================================================

    def get_history(self):
        """
        Return all history entries.
        """

        return self.history


    # ========================================================
    # GET FORMATTED HISTORY
    # ========================================================

    def get_formatted_history(self):
        """
        Convert the history list into text that can
        be displayed inside the GUI.
        """

        history_lines = []

        for entry in self.history:

            line = (
                f"[{entry['time']}] "
                f"{entry['count']} Runes: "
                f"{entry['formula']}"
            )

            history_lines.append(
                line
            )

        return "\n".join(
            history_lines
        )


    # ========================================================
    # CLEAR HISTORY
    # ========================================================

    def clear_history(self):
        """
        Delete all session history.
        """

        self.history.clear()


    # ========================================================
    # HISTORY COUNT
    # ========================================================

    def get_history_count(self):
        """
        Return the number of formulas generated
        during the current session.
        """

        return len(
            self.history
        )