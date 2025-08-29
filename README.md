# Mouse to Gamepad

A barebones Python application that creates a virtual gamepad device using the `evdev` library and converts mouse movements and actions into ones of the gamepad.

## Features

- Creates a virtual gamepad device with standard gamepad buttons and analog sticks
- Configurable through JSON configuration files

## Requirements

- Python 3.7+
- `evdev` library (version 1.9.2 or higher)
- Linux system with uinput support

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure your system has uinput support enabled and you have appropriate permissions to create virtual devices.

## Usage

### Configuration

Use the `config.py` script to generate a config file with the following structure:


```json
{
    "mouse_device": "/dev/input/event0",
    "gamepad_name": "My Virtual Gamepad",
    "sensitivity": 0.5,
    "vendor": 4660,
    "product": 22136,
    "version": 256
}
```

### Running the Application

```bash
python main.py
```

## Configuration Options

| Field           | Description                              | Default Value   |
|-----------------|------------------------------------------|-----------------|
| `mouse_device`  | Path to the mouse input device            | (required)      |
| `gamepad_name`  | Name of the virtual gamepad device      | "Virtual Gamepad" |
| `sensitivity`   | Sensitivity multiplier for input        | 0.5             |
| `vendor`        | USB vendor ID                            | 0x1234          |
| `product`       | USB product ID                           | 0x5678          |
| `version`       | USB version                              | 0x100           |

## Device Capabilities

The virtual gamepad supports:
- Analog sticks (ABS_X, ABS_Y)
- Buttons (A, B)
