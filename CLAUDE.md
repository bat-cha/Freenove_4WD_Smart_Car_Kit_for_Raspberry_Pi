# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Freenove 4WD Smart Car Kit for Raspberry Pi - a Python-based robotic car system with PyQt5 GUI client/server architecture. The car supports remote control, video streaming, autonomous modes, and various sensors.

## Architecture

### Client-Server Model
- **Server (Raspberry Pi)**: Runs on the car, controls hardware components
  - `Code/Server/main.py`: PyQt5 GUI server application
  - `Code/Server/main_headless.py`: Headless server for systemd service
  - `Code/Server/server.py`: Core TCP server handling commands and video streaming
- **Client (Remote)**: PyQt5 GUI application for remote control
  - `Code/Client/Main.py`: Main client application with full GUI controls

### Hardware Control Modules
Each hardware component has its own module in `Code/Server/`:
- `Motor.py`: 4WD motor control via PCA9685 PWM driver
- `servo.py`: Camera servo control (pan/tilt)
- `Led.py`: WS2812 RGB LED strip control
- `Ultrasonic.py`: Distance sensor
- `Light.py`: Light sensors (left/right)
- `Line_Tracking.py`: Infrared line tracking sensors
- `Buzzer.py`: Sound effects
- `ADC.py`: Analog-to-digital conversion for sensors

### Command Protocol
- Commands defined in `Code/Server/Command.py` and `Code/Client/Command.py`
- TCP communication with structured command format using '#' delimiters and '\n' terminators
- Separate data and video streaming sockets (ports 5000 and 8000)

## Running the System

### Server Setup (Raspberry Pi)
```bash
# Install dependencies
cd Code
python3 setup_windows.py  # or setup_macos.py on macOS

# Run server with GUI
cd Server
python3 main.py

# Run headless server
python3 main_headless.py

# Run as systemd service
sudo systemctl enable freenove-server.service
sudo systemctl start freenove-server.service
```

### Client Setup
```bash
cd Code/Client
python3 Main.py
```

### Command Line Options
- Server: `python3 main.py -t` (auto-start TCP server), `-n` (no UI)

## Dependencies
Required Python packages (installed via setup scripts):
- PyQt5, pyqt5-tools
- opencv-python, numpy, Pillow
- picamera (Raspberry Pi only)

## Operating Modes
1. **M-Free**: Manual remote control
2. **M-Light**: Light-following autonomous mode
3. **M-Sonic**: Ultrasonic obstacle avoidance
4. **M-Line**: Line tracking mode

## Key Features
- Real-time video streaming with face tracking
- Individual RGB LED control
- Servo camera control (pan/tilt)
- Multiple autonomous driving modes
- Battery voltage monitoring
- Keyboard shortcuts for all functions

## Network Configuration
- Server auto-detects IP on wlan0 interface
- Default ports: 5000 (commands), 8000 (video)
- Client connects via IP address input in GUI