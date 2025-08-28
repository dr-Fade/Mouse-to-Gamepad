#!/usr/bin/env python3

import os
import struct
import time
from evdev import UInput, ecodes, InputDevice, list_devices

# Create a uinput device that emulates a gamepad with left stick
def create_gamepad_device():
    # Define capabilities for the virtual gamepad
    events = {
        ecodes.EV_ABS: [
            (ecodes.ABS_X, (0, -32767, 32767, 0, 0, 0)),
            (ecodes.ABS_Y, (0, -32767, 32767, 0, 0, 0)),
        ]
    }

    # Create the uinput device
    device = UInput(
        events=events,
        name="Virtual Gamepad",
        vendor=0x1234,
        product=0x5678,
        version=0x100
    )
    
    return device

# Get mouse device path
def get_mouse_device():
    # Try to find a mouse device
    devices = [InputDevice(path) for path in list_devices()]
    print("\n".join(f"{d.path} - {d.name}" for d in devices))
    for device in devices:
        if "mouse" in device.name.lower() and "keyboard" not in device.name.lower():
            return device.path
    return None

# Main mapping function
def map_mouse_to_gamepad_stick():
    # Create virtual gamepad device
    gamepad = create_gamepad_device()
    
    # Get mouse device path
    mouse_path = get_mouse_device()
    if not mouse_path:
        print("No mouse device found!")
        return
    
    print(f"Using mouse device: {mouse_path}")
    
    # Open the mouse device for reading
    mouse = InputDevice(mouse_path)
    
    # Store previous mouse position
    prev_x, prev_y = 0, 0
    
    try:
        print("Mapping mouse movements to gamepad left stick. Press Ctrl+C to exit.")
        
        # Read events from mouse
        for event in mouse.read_loop():
            if event.type == ecodes.EV_REL and event.code in [ecodes.ABS_X, ecodes.ABS_Y]:
                # Calculate movement delta
                current_x = 500*event.value if event.code == ecodes.ABS_X else prev_x
                current_y = 500*event.value if event.code == ecodes.ABS_Y else prev_y

                # Only send events when there's actual movement
                if event.code == ecodes.ABS_X:
                    prev_x = current_x
                elif event.code == ecodes.ABS_Y:
                    prev_y = current_y

                # Send the gamepad stick position
                print(f"type:{event.type} - code:{event.code} - value:{event.value}")
                print(f"ecodes.EV_ABS, ecodes.ABS_X, {current_x:=} ({prev_x:=})")
                gamepad.write(ecodes.EV_ABS, ecodes.ABS_X, current_x)
                print(f"ecodes.EV_ABS, ecodes.ABS_Y, {current_y:=} ({prev_y:=})")
                gamepad.write(ecodes.EV_ABS, ecodes.ABS_Y, current_y)
                gamepad.syn()

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        # Clean up
        mouse.close()
        gamepad.close()

if __name__ == "__main__":
    map_mouse_to_gamepad_stick()
