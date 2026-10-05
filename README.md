# Elder Futhark Rune Generator

A desktop application for generating, exploring, and saving Elder Futhark rune formulas.

The application is written in **Python** using **PySide6** and provides a graphical interface for generating unique rune combinations from the 24-character Elder Futhark alphabet.

## Features

- Generate random rune formulas containing:
  - 5 runes
  - 7 runes
  - 9 runes
  - 15 runes
- No duplicate runes within a generated formula
- Browse all 24 Elder Futhark runes in the Rune Library
- View rune names, transliterations, and interpretive keywords
- Save generated formulas to a persistent collection
- Browse previously saved formulas
- Delete individual saved formulas
- Clear the saved formula collection
- Session-based formula history
- Copy generated formulas to the clipboard
- Export formulas and rune information to TXT files
- Dark-themed PySide6 interface
- Windows standalone distribution using PyInstaller

## Current Version

**Version 2.4**

Version 2.4 is the first distribution-ready release of the application.

## Screens

The application currently contains three main sections:

### Generator

Generate a random formula using 5, 7, 9, or 15 unique Elder Futhark runes.

### Rune Library

Browse all 24 Elder Futhark runes and view their names, transliterations, and interpretive keywords.

### Saved Formulas

View and manage formulas that have been permanently saved to your collection.

## Project Structure

```text
elder-futhark-generator/
├── data/
│   ├── __init__.py
│   └── runes.py
│
├── gui/
│   ├── __init__.py
│   ├── generator_page.py
│   ├── main_window.py
│   ├── rune_card.py
│   ├── rune_library.py
│   └── saved_formulas.py
│
├── resources/
│   └── styles.qss
│
├── utils/
│   ├── __init__.py
│   ├── formula_manager.py
│   ├── history_manager.py
│   └── saved_formula_manager.py
│
├── main.py
├── elder_futhark.spec
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## Requirements

For running the application from source:

- Python 3
- PySide6

Install the required Python packages with:

```bash
pip install -r requirements.txt
```

Then run:

```bash
python main.py
```

## Windows Distribution

The application can be packaged as a standalone Windows application using **PyInstaller**.

Users of the packaged version do not need to install Python or PySide6 separately.

Application data for saved formulas is stored in the user's home directory:

```text
.elder_futhark_generator/formulas.json
```

This allows saved formulas to remain separate from the application installation.

## Rune Generation

Rune formulas are generated from the complete 24-rune Elder Futhark set.

Python's random selection without replacement is used so that a rune cannot occur more than once within the same generated formula.

## Historical Note

The Elder Futhark is an early runic writing system historically used by Germanic peoples.

The rune keywords and interpretations presented by this application are intended as general modern/common interpretive references. They should not be understood as establishing a single historically documented Elder Futhark divination system.

## Future Development

Potential future development may include:

- Runic divination features
- Additional rune spreads
- Expanded rune reference information
- Saved readings
- Additional export options
- UI and accessibility improvements

These features are not part of the current v2.4 release.

## Building with PyInstaller

The repository includes a PyInstaller specification file.

With PyInstaller installed, the application can be built using:

```bash
pyinstaller elder_futhark.spec
```

Generated build files are placed in the `build/` and `dist/` directories.

These directories are intentionally excluded from version control.

## License

This project is licensed under the MIT License.

See `LICENSE` for details.