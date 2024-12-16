# COSI142-SmartHomeControlPanel
Smart Home Control Panel (SHCP) is a project that utilizes multiple I/O devices to emulate various smart home devices, such as motion-activated lights, air quality monitoring, and more. The project demonstrates the integration of hardware and software to create a connected and functional smart home environment.

## About the System
- Uses Flask/HTTP for communication between devices via a web server.
- Supports various smart devices, such as motion sensors, LEDs, temperature and humidity sensors, and more.
- Implements device scheduling and automation capabilities.

## About the Directory
### Core Files
- `server.py`: Main Python script running the Flask web server, acting as the control hub for the system.
- `tests/pico_test.py`: Tests the data exchange between the Raspberry Pi Pico and connected devices.

### Device Tests
Located in the `device_tests` directory, this contains scripts for testing various I/O devices. These files serve as references for individual device functionality but are not part of the main system. Key tests include:
- `air-humidity-lcd-display.py`: Displays air humidity on an LCD.
- `motion_led_detection_test.py`: Tests motion detection and triggers LEDs.
- `smoke_sensor.py`: Tests the smoke sensor's functionality.
- Other files demonstrate tests for mini fans, RGB LEDs, and more.

### Helper Modules
Located in `helper` directory:
- ip.py: Handles IP-related utilities for networking.
- `kasa_helper.py`: Provides integration for Kasa smart devices.
- `scheduler.py`: Automates device actions through scheduling

### Pico Modules
Located in `pico\` directory and is used to run the devices as part of the system:
- `led.py`: Manages LED strips and individual LEDs.
- `motion_sensor.py`: Handles motion detection events.
- `temp_humidity.py`: Reads data from temperature and humidity sensors.
- `utils.py`: Provides utility functions for Pico-specific tasks.

### Raspberry Pi Modules
Located in the `raspberry/` directory:
- `smoke_sensor_pi.py`: Interfaces with the smoke sensor on the Raspberry Pi.
- `utils_pi.py`: General utility functions for Raspberry Pi operations.

### Static and Template Files
- `static/`: Contains assets such as CSS files (`layout.css`, `led.css`) and images (e.g., device icons and member photos).
- `templates/`: Includes HTML templates for the Flask web interface, such as:
    - `index.html`: Main dashboard.
    - `devices.html`: Lists and manages connected devices.
    - `about.html`: Information about the project and team.
    - `led.html`: LED control interface.