# LineTrim Documentation

Comprehensive documentation for the ParagliderLineTrim project.

## Contents

- [User Guide](#user-guide)
- [Developer Guide](#developer-guide)
- [Architecture](#architecture)
- [Hardware Integration](#hardware-integration)

## User Guide

### Getting Started

1. **Installation**
   - Install Python 3.6 or higher
   - Run: `pip install -r requirements.txt`
   - Launch: `bin/ParagliderLineTrim.bat` (Windows) or `bin/ParagliderLineTrim` (Linux/Mac)

2. **Loading Glider Data**
   - Go to: File → Load line length
   - Select a glider specification file from `data/gliders/`
   - The application will initialize with theoretical line lengths

3. **Taking Measurements**
   - Select Row, Number, and Side from dropdowns
   - **Manual**: Type measurement in mm and press Enter
   - **Leica DISTO**: Press MEASURE button (automatic entry)
   - Navigate using Direction dropdown or let it auto-advance

4. **Reviewing Results**
   - **Green values**: Within tolerance
   - **Red values**: Outside tolerance
   - Offset shown at bottom of screen

5. **Saving Work**
   - File → Save project (or Ctrl+S)
   - Projects saved as `.ltf` files in `projects/`
   - Auto-save feature saves to `projects/autosave/`

6. **Generating Reports**
   - File → Export PDF report
   - PDF saved to `reports/`

### Keyboard Shortcuts

- **Enter**: Record measurement and advance
- **Ctrl+S**: Save project
- **Esc**: Cancel current measurement

### Audio Feedback

Toggle: File → Sound On/Off
- Success sound: Valid measurement recorded
- Error sound: Invalid measurement
- Back sound: Cancelled previous measurement

## Developer Guide

### Architecture Overview

The application follows a Model-View-Controller pattern:

```
┌─────────────────┐
│   UI Layer      │  src/ui/
│  (PyQt5 Views)  │
└────────┬────────┘
         │
┌────────▼────────┐
│  Application    │  src/main.py
│   Controller    │  (LineTrim class)
└────────┬────────┘
         │
┌────────▼────────┐
│  Business Logic │  src/core/
│   (Data Models) │
└─────────────────┘

External:
┌─────────────────┐
│   Hardware      │  hardware/leica_disto/
│   Integration   │  (Bluetooth services)
└─────────────────┘
```

### Code Organization

#### `src/main.py`
Main application controller containing the `LineTrim` class:
- Inherits from `Ui_LineTrim`
- Manages application state
- Handles user interactions
- Coordinates measurements and calculations

Key methods:
- `setLineLength()` - Load glider specifications
- `updateMeasurement()` - Process measurement input
- `computeDeviation()` - Calculate deviations from theoretical
- `updateView()` - Refresh visual display
- `exportPDFReport()` - Generate PDF output

#### `src/ui/`
User interface components:
- `line_trim_ui.py` - Generated from Qt Designer
- `figure_widget.py` - Matplotlib integration

#### `src/core/`
Business logic modules (to be expanded):
- Data models
- Calculation algorithms
- Validation logic

#### `hardware/leica_disto/`
Hardware device integration:
- `connect.py` - Bluetooth connection service
- `scan.py` - Device discovery utility

### Data Flow

```
User Input → LineTrim Controller → Data Validation
                 ↓
         State Update (measured_line_length)
                 ↓
         Deviation Calculation (computeDeviation)
                 ↓
         Visual Update (updateView)
                 ↓
         Auto-Save (saveProject)
```

### Hardware Integration

#### Leica DISTO Connection

The Leica DISTO integration uses Bluetooth Low Energy (BLE):

1. **Discovery**: `scan.py` finds nearby devices
2. **Connection**: `connect.py` establishes BLE connection
3. **Data Reception**: Subscribes to measurement notifications
4. **Input Simulation**: Converts measurements to keyboard input using `pynput`

**Key Components**:
```python
# hardware/leica_disto/connect.py
async def on_measure(sender, data):
    """Callback when measurement received"""
    val_mm = int(round(struct.unpack('<f', data)[0] * 1000))
    # Simulate keyboard input
    keyboard.type(str(val_mm))
    keyboard.press(Key.enter)
```

**Adding New Hardware**:
1. Create `hardware/your_device/` folder
2. Implement connection script with same keyboard simulation pattern
3. Update launcher scripts to start your service

### File Format Specifications

#### Project Files (.ltf)
Pickled Python dictionary:
```python
{
    'line_length': dict,         # Theoretical lengths
    'measured_line_length': dict, # Measured values
    'row_size': list,            # Lines per row
    'row_names': list,           # Row identifiers
    'identification': str        # Project metadata
}
```

#### Glider Specification Files (.txt)
```
*RowA
7858
7758
*RowB
7767
7665
```

### Testing

(To be implemented in `tests/`)

Planned test coverage:
- Unit tests for calculation functions
- Integration tests for file I/O
- UI tests for user interactions
- Hardware mock tests

### Contributing

1. Follow existing code structure
2. Document functions with docstrings
3. Add type hints where applicable
4. Update relevant `.md` files
5. Test hardware integrations thoroughly

### Dependencies Management

Core dependencies in `requirements.txt`:
```
PyQt5>=5.9.2        # GUI framework
matplotlib>=3.0.0    # Visualization
numpy>=1.18.0       # Numerical computation
bleak               # Bluetooth LE
pynput              # Keyboard simulation
```

### Building and Distribution

Using `setup.py`:
```bash
# Development installation
pip install -e .

# Build distribution
python setup.py sdist bdist_wheel
```

## Architecture

### Design Principles

1. **Separation of Concerns**: UI, business logic, and hardware code are isolated
2. **Modularity**: Hardware integrations are plug-and-play
3. **Extensibility**: Easy to add new glider models, devices, or features
4. **User-Friendly**: Automatic save, audio feedback, visual guidance

### Technology Stack

- **GUI**: PyQt5 (cross-platform Qt bindings)
- **Visualization**: Matplotlib (embedded in Qt)
- **Data**: NumPy (efficient numerical operations)
- **Hardware**: Bleak (cross-platform Bluetooth LE)
- **I/O**: Pickle (project serialization)

### Future Enhancements

- Database backend for glider specifications
- Cloud sync for projects
- Multiple measurement device support
- Statistical analysis tools
- Batch processing capabilities

## Hardware Integration

### Supported Devices

#### Leica DISTO (Bluetooth LE)
- **Location**: `hardware/leica_disto/`
- **Protocol**: Bluetooth Low Energy
- **Data Format**: 32-bit float (meters)
- **Status**: Fully implemented

### Adding New Devices

Template structure:
```
hardware/
└── your_device/
    ├── __init__.py
    ├── connect.py      # Main connection handler
    ├── scan.py         # Device discovery
    └── README.md       # Device-specific docs
```

See `hardware/leica_disto/` as reference implementation.

---

For questions or issues, please refer to the main README.md or create an issue in the repository.
