# ParagliderLineTrim
Python app dedicated to trimming of paraglider line length

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
# On Windows
bin\LineTrim.bat

# On Linux/Mac
bin/LineTrim
```

## Project Structure

```
ParagliderLineTrim/
├── src/                    # Source code
│   ├── main.py            # Main application entry point
│   ├── ui/                # User interface components
│   │   ├── line_trim_ui.py
│   │   └── figure_widget.py
│   └── core/              # Business logic
├── resources/             # Application resources
│   └── images/           # Icons and images
├── data/                  # Data files
│   ├── gliders/          # Glider specifications
│   └── profiles/         # Wing profiles
├── projects/             # User project files
├── reports/              # Generated reports
├── bin/                  # Launch scripts
├── docs/                 # Documentation
└── tests/                # Unit tests
```

## Dependencies

- PyQt5 >= 5.9.2
- matplotlib >= 3.0.0
- numpy >= 1.18.0

## License

See LICENSE file for details.

