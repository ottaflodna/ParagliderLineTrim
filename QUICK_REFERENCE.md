# Quick Reference Guide

## Running the Application

### Windows
```cmd
bin\ParagliderLineTrim.bat
```

### Linux/Mac
```bash
bin/ParagliderLineTrim
```

## Project Structure

```
src/              → Python source code
  main.py         → Main application entry point
  ui/             → User interface components
  core/           → Business logic modules
hardware/         → Hardware device integrations
  leica_disto/    → Leica DISTO Bluetooth connection
resources/        → Application resources (non-code)
  images/         → UI icons and images
  sounds/         → Audio feedback files
  profiles/       → Wing profile data
data/             → Static data files
  gliders/        → Glider line length specifications
projects/         → User project files (.ltf)
  autosave/       → Automatically saved projects
reports/          → Generated PDF reports
bin/              → Launch scripts
docs/             → Documentation
tests/            → Unit tests
```

## Key Files

### Application Core
- `src/main.py` - Main application entry point and LineTrim class
- `src/ui/line_trim_ui.py` - UI layout (generated from Qt Designer)
- `src/ui/figure_widget.py` - Matplotlib figure display widget

### Hardware Integration
- `hardware/leica_disto/connect.py` - Bluetooth connection to Leica DISTO
- `hardware/leica_disto/scan.py` - Scan for Bluetooth devices

### Configuration
- `requirements.txt` - Python dependencies
- `setup.py` - Installation script

### Launch Scripts
- `bin/ParagliderLineTrim.bat` - Windows launcher (starts DISTO service + app)
- `bin/ParagliderLineTrim` - Linux/Mac launcher (starts DISTO service + app)

## Dependencies

Install with:
```bash
pip install -r requirements.txt
```

Required packages:
- **PyQt5** >= 5.9.2 - GUI framework
- **matplotlib** >= 3.0.0 - Plotting and visualization
- **numpy** >= 1.18.0 - Numerical operations
- **bleak** - Bluetooth Low Energy library (for Leica DISTO)
- **pynput** - Keyboard input simulation (for Leica DISTO)

## Hardware Setup

### Leica DISTO Configuration

1. **Pair Device**: Pair your Leica DISTO with your computer via Bluetooth
2. **Launch Application**: The launcher scripts automatically start the connection service
3. **Take Measurements**: Press the MEASURE button on the DISTO - values are automatically entered
4. **Troubleshooting**: Run `hardware/leica_disto/scan.py` to find your device

### Manual Measurement

If not using a Leica DISTO:
1. Type the measurement value in millimeters
2. Press Enter to record

## Development

### Project Architecture

- **Separation of Concerns**: UI code (`src/ui/`) separate from business logic (`src/core/`)
- **Hardware Abstraction**: Device-specific code isolated in `hardware/`
- **Resource Management**: All assets centralized in `resources/`

### Adding Features

#### Adding a New Hardware Device
1. Create folder: `hardware/your_device/`
2. Implement connection script with keyboard input simulation
3. Update launch scripts in `bin/`

#### Adding Tests
Place test files in the `tests/` directory.

#### Adding Documentation
Place documentation in the `docs/` directory.

#### Adding Glider Data
Place glider specification files (.txt) in `data/gliders/`.

Format:
```
*RowName
length1
length2
*NextRow
length1
```

#### Adding Resources
- Icons/Images: `resources/images/`
- Audio files: `resources/sounds/`
- Wing profiles: `resources/profiles/`

## Installation as Package

To install as a Python package:
```bash
pip install -e .
```

Then run from anywhere:
```bash
linetrim
```

## File Formats

### Project Files (.ltf)
Binary format (pickled dict) containing:
- `line_length` - Theoretical line lengths
- `measured_line_length` - Measured values
- `row_size` - Lines per row
- `row_names` - Row identifiers
- `identification` - Project metadata

### Glider Specification Files (.txt)
Plain text format with rows marked by `*RowName` and line lengths in mm.

## Troubleshooting

### Leica DISTO Not Connecting
```bash
# Check paired devices
python hardware/leica_disto/scan.py

# Verify device name in connect.py matches your DISTO model
```

### Application Won't Start
```bash
# Check Python version (3.6+)
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Measurements Not Registering
- Ensure focus is on the measurement input field
- Check Bluetooth connection if using Leica DISTO
- Verify keyboard input permissions (for pynput)
