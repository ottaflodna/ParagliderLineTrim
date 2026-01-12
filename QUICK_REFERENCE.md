# Quick Reference Guide

## Running the Application

### Windows
```cmd
bin\LineTrim.bat
```

### Linux/Mac
```bash
bin/LineTrim
```

## Project Structure

```
src/              → Python source code
resources/        → Images, sounds, and other resources
  images/         → UI icons and images
  sounds/         → Audio files (when added)
data/             → Data files
  gliders/        → Glider specifications
  profiles/       → Wing profiles
projects/         → User project files (.ltf)
reports/          → Generated PDF reports
bin/              → Launch scripts
docs/             → Documentation
tests/            → Unit tests (to be added)
```

## Key Files

- `src/main.py` - Main application entry point
- `src/ui/line_trim_ui.py` - UI layout
- `src/ui/figure_widget.py` - Figure display widget
- `requirements.txt` - Python dependencies
- `setup.py` - Installation script

## Dependencies

Install with:
```bash
pip install -r requirements.txt
```

Required packages:
- PyQt5 >= 5.9.2
- matplotlib >= 3.0.0
- numpy >= 1.18.0

## Development

### Adding Tests
Place test files in the `tests/` directory.

### Adding Documentation
Place documentation in the `docs/` directory.

### Adding Glider Data
Place glider specification files (.txt) in `data/gliders/`.

### Adding Resources
- Images: `resources/images/`
- Sounds: `resources/sounds/`

## Installation as Package

To install as a Python package:
```bash
pip install -e .
```

Then run from anywhere:
```bash
linetrim
```
