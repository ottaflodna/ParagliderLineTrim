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
bin\ParagliderLineTrim.bat

# On Linux/Mac
bin/ParagliderLineTrim
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
├── hardware/              # Hardware integration
│   └── leica_disto/      # Leica DISTO device connection
│       ├── connect.py    # Bluetooth connection script
│       └── scan.py       # Device discovery utility
├── resources/             # Application resources
│   ├── images/           # Icons and images
│   ├── profiles/         # Wing profiles
│   └── sounds/           # Audio feedback files
├── data/                  # Data files
│   └── gliders/          # Glider specifications
├── projects/             # User project files (.ltf)
│   └── autosave/         # Auto-saved projects
├── reports/              # Generated PDF reports
├── bin/                  # Launch scripts
│   ├── ParagliderLineTrim.bat  # Windows launcher
│   └── ParagliderLineTrim      # Linux/Mac launcher
├── docs/                 # Documentation
└── tests/                # Unit tests
```

## Features

- Load and manage paraglider line length specifications
- Measure actual line lengths with keyboard input or Leica DISTO
- Visual comparison between theoretical and measured values
- Automatic deviation calculation with color-coded feedback
- Export measurement reports to PDF
- Project save/load functionality
- Audio feedback for measurements (optional)

## Hardware Integration

### Leica DISTO Support

The application supports Bluetooth integration with Leica DISTO distance meters:

1. **Automatic Connection**: The launch scripts automatically start the Bluetooth connection service
2. **Measurement Input**: Distance measurements are sent directly as keyboard input
3. **Setup**: Ensure your Leica DISTO is paired via Bluetooth before launching

The hardware integration code is located in `hardware/leica_disto/`:
- `connect.py` - Main Bluetooth connection handler
- `scan.py` - Device discovery utility

## Dependencies

- PyQt5 >= 5.9.2
- matplotlib >= 3.0.0
- numpy >= 1.18.0
- bleak (for Bluetooth LE support)
- pynput (for keyboard input simulation)

## Usage

1. **Load Line Length Data**: File → Load line length
2. **Select Measurement Point**: Use dropdowns to select Row, Number, and Side
3. **Enter Measurements**: Type measurement value and press Enter (or use Leica DISTO)
4. **Navigate**: Choose direction (Center to tip, Leading to trailing, etc.)
5. **Review Deviations**: Color-coded values show measurement accuracy
6. **Export Report**: File → Export PDF report

## File Formats

- **`.ltf`**: LineTrim project files (pickled Python dictionaries)
- **`.txt`**: Glider specification files (plain text with row markers)

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

