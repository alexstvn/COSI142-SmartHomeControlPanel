# COSI142-SmartHomeControlPanel
Smart Home Control Panel (SHCP) is a project that will utilize multiple I/O devices and emulate various smart home devices (motion-activated lights, etc.).

## About the System
- uses Flask / HTTP for connection between devices using web server

## About the Directory
- `device_tests` - contains files related to tested input/output devices like reading air humidity, minifan with button test, etc. These pertain to code that could be used as for reference but does not pertain to the actual system.
- `server.py` - Running Python server using Flask.
- `pico_test.py` - Sends data to/from devices with pico.