"""
Leica Disto D1 Interface
Connects to a Leica Disto D1 laser distance meter via Bluetooth
and reads measurements for paraglider line length measurement.
"""

import serial
import serial.tools.list_ports
import time
import subprocess
import re


class LeicaDistoD1:
    """Interface for Leica Disto D1 laser distance meter."""
    
    def __init__(self, port=None, baudrate=9600, timeout=2):
        """
        Initialize connection to Leica Disto D1.
        
        Args:
            port: Serial port (e.g., '/dev/rfcomm0' on Linux, 'COM3' on Windows)
                  If None, will attempt to auto-detect
            baudrate: Communication speed (default 9600)
            timeout: Read timeout in seconds
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = None
        
    def find_disto_port(self):
        """
        Attempt to find the Disto D1 on available serial ports.
        
        Returns:
            str: Port name if found, None otherwise
        """
        ports = serial.tools.list_ports.comports()
        
        # Look for Bluetooth serial ports or devices with "Disto" in description
        for port in ports:
            port_name = port.device.lower()
            description = port.description.lower()
            
            if 'disto' in description or 'rfcomm' in port_name or 'bluetooth' in description:
                print(f"Found potential Disto device: {port.device} - {port.description}")
                return port.device
        
        # On Linux, check common rfcomm devices
        import os
        for i in range(10):
            rfcomm_port = f'/dev/rfcomm{i}'
            if os.path.exists(rfcomm_port):
                print(f"Found rfcomm device: {rfcomm_port}")
                return rfcomm_port
        
        return None
    
    def connect(self):
        """
        Establish connection to the Disto D1.
        
        Returns:
            bool: True if connection successful
        """
        if self.port is None:
            self.port = self.find_disto_port()
            
        if self.port is None:
            print("Could not find Disto D1. Please specify port manually.")
            return False
        
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE
            )
            print(f"Connected to Disto D1 on {self.port}")
            time.sleep(0.5)  # Give device time to initialize
            return True
        except serial.SerialException as e:
            print(f"Failed to connect: {e}")
            return False
    
    def disconnect(self):
        """Close the serial connection."""
        if self.serial and self.serial.is_open:
            self.serial.close()
            print("Disconnected from Disto D1")
    
    def send_command(self, command):
        """
        Send a command to the Disto D1.
        
        Args:
            command: Command string to send
        """
        if not self.serial or not self.serial.is_open:
            raise Exception("Not connected to Disto D1")
        
        # Ensure command ends with carriage return
        if not command.endswith('\r'):
            command += '\r'
        
        self.serial.write(command.encode('ascii'))
        time.sleep(0.1)
    
    def read_response(self):
        """
        Read response from the Disto D1.
        
        Returns:
            str: Response string
        """
        if not self.serial or not self.serial.is_open:
            raise Exception("Not connected to Disto D1")
        
        response = b''
        while self.serial.in_waiting > 0:
            response += self.serial.read(self.serial.in_waiting)
            time.sleep(0.1)
        
        return response.decode('ascii', errors='ignore').strip()
    
    def get_measurement(self):
        """
        Request and retrieve a distance measurement.
        
        The Disto D1 may automatically send measurements when the button is pressed,
        or you can trigger a measurement programmatically if supported.
        
        Returns:
            float: Distance in meters, or None if no measurement available
        """
        # Try to read any available data (measurement from button press)
        response = self.read_response()
        
        if response:
            # Parse the measurement from the response
            # Disto D1 typically sends format like "31.0123" or similar
            distance = self.parse_measurement(response)
            if distance is not None:
                return distance
        
        return None
    
    def parse_measurement(self, response):
        """
        Parse a distance measurement from the Disto response.
        
        Args:
            response: Raw response string
            
        Returns:
            float: Distance in meters, or None if parsing failed
        """
        # Try to find a number that looks like a distance measurement
        # Typically in format: X.XXXX or XX.XXXX (meters)
        patterns = [
            r'(\d+\.\d+)',  # Match decimal number
            r'(\d+)',       # Match integer
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response)
            if match:
                try:
                    distance = float(match.group(1))
                    # Sanity check: reasonable range for paraglider lines (0.1m to 50m)
                    if 0.01 <= distance <= 100:
                        return distance
                except ValueError:
                    continue
        
        return None
    
    def wait_for_measurement(self, timeout=30):
        """
        Wait for a measurement to be taken (button press on Disto).
        
        Args:
            timeout: Maximum time to wait in seconds
            
        Returns:
            float: Distance in meters, or None if timeout
        """
        print("Waiting for measurement... (press the button on Disto D1)")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            measurement = self.get_measurement()
            if measurement is not None:
                return measurement
            time.sleep(0.1)
        
        print("Timeout waiting for measurement")
        return None
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()


def main():
    """
    Example usage of the Leica Disto D1 interface.
    """
    import sys
    
    print("Leica Disto D1 Interface")
    print("-" * 40)
    
    # Allow user to specify port as command line argument
    port = sys.argv[1] if len(sys.argv) > 1 else None
    
    # Create and connect to Disto
    disto = LeicaDistoD1(port=port)
    
    if not disto.connect():
        print("\nTroubleshooting tips:")
        print("1. Make sure Disto D1 Bluetooth is enabled (hold BT button)")
        print("2. Pair the device using system Bluetooth settings")
        print("3. On Linux, bind to rfcomm: sudo rfcomm bind /dev/rfcomm0 <MAC_ADDRESS>")
        print("4. Specify port manually: python leica_disto_d1.py /dev/rfcomm0")
        return
    
    try:
        print("\nReady to measure!")
        print("Press the measurement button on the Disto D1")
        print("Press Ctrl+C to exit\n")
        
        measurement_count = 0
        
        while True:
            distance = disto.wait_for_measurement(timeout=60)
            
            if distance is not None:
                measurement_count += 1
                print(f"Measurement #{measurement_count}: {distance:.4f} m ({distance*100:.2f} cm)")
            else:
                print("No measurement received. Exiting.")
                break
                
    except KeyboardInterrupt:
        print("\n\nMeasurement session ended.")
    finally:
        disto.disconnect()


if __name__ == "__main__":
    main()
