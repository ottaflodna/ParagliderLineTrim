# Leica Disto D1 Setup Guide

This guide explains how to connect and use a Leica Disto D1 laser distance meter with the ParagliderLineTrim application for accurate line length measurements.

## Hardware Requirements

- Leica Disto D1 laser distance meter
- Computer with Bluetooth capability
- Linux/Windows operating system

## Linux Setup

### 1. Enable Bluetooth on Disto D1

Press and hold the Bluetooth button on the Disto D1 until the Bluetooth LED starts flashing.

### 2. Pair the Device

Open a terminal and use `bluetoothctl`:

```bash
bluetoothctl
power on
agent on
scan on
```

Look for a device named "DISTO D1" or similar. Note its MAC address (format: XX:XX:XX:XX:XX:XX).

```bash
pair XX:XX:XX:XX:XX:XX
trust XX:XX:XX:XX:XX:XX
connect XX:XX:XX:XX:XX:XX
quit
```

### 3. Bind to Serial Port

```bash
sudo rfcomm bind /dev/rfcomm0 XX:XX:XX:XX:XX:XX
```

To make this permanent, add to `/etc/bluetooth/rfcomm.conf`:

```
rfcomm0 {
    bind yes;
    device XX:XX:XX:XX:XX:XX;
    channel 1;
    comment "Leica Disto D1";
}
```

### 4. Test Connection

```bash
# Check if device appears
ls -l /dev/rfcomm0

# Test with screen or picocom
sudo picocom /dev/rfcomm0 -b 9600
```

## Windows Setup

### 1. Enable Bluetooth on Disto D1

Press and hold the Bluetooth button on the Disto D1 until the Bluetooth LED starts flashing.

### 2. Pair the Device

1. Go to Settings → Devices → Bluetooth & other devices
2. Click "Add Bluetooth or other device"
3. Select "Bluetooth"
4. Choose "DISTO D1" from the list
5. Complete pairing (may require PIN: usually 0000 or 1234)

### 3. Find COM Port

1. Open Device Manager
2. Expand "Ports (COM & LPT)"
3. Look for "Standard Serial over Bluetooth link" or similar
4. Note the COM port number (e.g., COM3, COM5)

## Python Usage

### Basic Usage

```python
from src.leica_disto_d1 import LeicaDistoD1

# Auto-detect port
disto = LeicaDistoD1()
disto.connect()

# Wait for measurement
distance = disto.wait_for_measurement()
print(f"Measured: {distance:.4f} m")

disto.disconnect()
```

### With Context Manager

```python
from src.leica_disto_d1 import LeicaDistoD1

with LeicaDistoD1(port='/dev/rfcomm0') as disto:
    distance = disto.wait_for_measurement()
    print(f"Measured: {distance:.4f} m")
```

### Multiple Measurements

```python
from src.leica_disto_d1 import LeicaDistoD1

with LeicaDistoD1() as disto:
    measurements = []
    for i in range(5):
        print(f"Measurement {i+1}/5 - Press button on Disto...")
        distance = disto.wait_for_measurement(timeout=30)
        if distance:
            measurements.append(distance)
            print(f"  → {distance:.4f} m")
    
    print(f"\nAverage: {sum(measurements)/len(measurements):.4f} m")
```

## Command Line Usage

Run the standalone script:

```bash
# Auto-detect port
python src/leica_disto_d1.py

# Specify port manually (Linux)
python src/leica_disto_d1.py /dev/rfcomm0

# Specify port manually (Windows)
python src/leica_disto_d1.py COM3
```

## Troubleshooting

### Device Not Found

- Ensure Disto D1 Bluetooth is enabled (LED flashing)
- Check device is paired in system Bluetooth settings
- Try re-pairing the device

### Connection Failed

**Linux:**
```bash
# Check Bluetooth service is running
sudo systemctl status bluetooth

# Check rfcomm device exists
ls -l /dev/rfcomm*

# Unbind and rebind
sudo rfcomm release /dev/rfcomm0
sudo rfcomm bind /dev/rfcomm0 XX:XX:XX:XX:XX:XX
```

**Windows:**
- Check Device Manager for COM port
- Try different COM port numbers
- Re-pair the device

### Permission Denied (Linux)

```bash
# Add user to dialout group
sudo usermod -a -G dialout $USER

# Or run with sudo (not recommended for regular use)
sudo python src/leica_disto_d1.py
```

Log out and back in for group changes to take effect.

### No Measurements Received

- Ensure you're pressing the measurement button on the Disto (not just Bluetooth button)
- Check battery level on Disto D1
- Verify the device is actually connected (LED solid, not flashing)
- Try reconnecting the Bluetooth connection

## Integration with ParagliderLineTrim

The Disto D1 can be integrated into the line trim workflow for accurate measurements:

1. Measure each line length with the Disto D1
2. Record measurements automatically
3. Compare with target lengths from glider specifications
4. Generate trim reports

See the main application documentation for integration details.

## Technical Notes

- **Protocol**: The Disto D1 uses a simple serial protocol over Bluetooth SPP (Serial Port Profile)
- **Baud Rate**: 9600 bps (default)
- **Data Format**: Measurements are sent as ASCII text when the button is pressed
- **Range**: 0.05 m to 200 m (typical)
- **Accuracy**: ±1.5 mm (typical)

## References

- Leica Disto D1 User Manual
- PySerial Documentation: https://pyserial.readthedocs.io/
- Bluetooth Serial Port Profile (SPP) Specification
