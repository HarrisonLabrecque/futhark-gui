# utils/formula_manager.py

import random

from data.runes import ELDER_FUTHARK


class FormulaManager:
    """
    Handles rune formula generation and formatting.
    """

    @staticmethod
    def generate_formula(rune_count):
        """
        Generate a random rune formula.

        random.sample() selects without replacement,
        so no rune can appear twice in the formula.
        """

        if rune_count > len(ELDER_FUTHARK):
            raise ValueError(
                "Rune count cannot exceed the number "
                "of Elder Futhark runes."
            )

        return random.sample(
            ELDER_FUTHARK,
            rune_count
        )


    @staticmethod
    def get_formula_string(runes):
        """
        Convert a list of rune dictionaries into
        a displayable string.
        """

        symbols = [
            rune["symbol"]
            for rune in runes
        ]

        return "  ".join(symbols)


    @staticmethod
    def get_formula_details(runes):
        """
        Convert rune information into text that can
        be saved to a file.
        """

        details = []

        for index, rune in enumerate(
            runes,
            start=1
        ):
            details.append(
                f"{index}. "
                f"{rune['symbol']} "
                f"{rune['name']}"
            )

            details.append(
                f"   Transliteration: "
                f"{rune['transliteration']}"
            )

            details.append(
                f"   Keywords: "
                f"{rune['meaning']}"
            )

            details.append("")

        return "\n".join(details)