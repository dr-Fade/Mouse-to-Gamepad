import argparse
from pathlib import Path

from evdev import InputDevice, UInput, ecodes

from config import Config


ABS_BOUNDARY = 32767


def create_gamepad_device(config: Config) -> None:
    """Create a uinput device that emulates a gamepad with left stick"""
    events = {
        ecodes.EV_ABS: [
            (ecodes.ABS_X, (0, -ABS_BOUNDARY, ABS_BOUNDARY, 0, 0, 0)),
            (ecodes.ABS_Y, (0, -ABS_BOUNDARY, ABS_BOUNDARY, 0, 0, 0)),
        ],
        ecodes.EV_KEY: [
            ecodes.BTN_A,
            ecodes.BTN_B,
            ecodes.BTN_X,
            ecodes.BTN_Y,
            ecodes.BTN_TL,
            ecodes.BTN_TR,
            ecodes.BTN_SELECT,
            ecodes.BTN_START,
            ecodes.BTN_THUMBL,
            ecodes.BTN_THUMBR,
        ]
    }

    device = UInput(
        events=events,
        name=config.gamepad_name,
        vendor=config.vendor,
        product=config.product,
        version=config.version
    )

    return device


def map_mouse_to_gamepad_stick(config: Config):
    """Main mapping function with configurable parameters"""
    # Create virtual gamepad device
    gamepad = create_gamepad_device(config)

    # Open the mouse device for reading
    mouse = InputDevice(config.mouse_device)

    # set sensitivity and adjust the scale
    sensitivity: float = config.sensitivity * ABS_BOUNDARY / 50

    # Store previous mouse position
    prev_x, prev_y = 0, 0

    try:
        # Read events from mouse
        for event in mouse.read_loop():
            if event.type == ecodes.EV_REL and event.code in [ecodes.ABS_X, ecodes.ABS_Y]:
                # Calculate movement delta with sensitivity
                if event.code == ecodes.ABS_X:
                    current_x = int(event.value * sensitivity)
                    prev_x = current_x
                else:
                    current_x = prev_x

                if event.code == ecodes.ABS_Y:
                    current_y = int(event.value * sensitivity)
                    prev_y = current_y
                else:
                    current_y = prev_y

                # Send the gamepad stick position
                print(
                    f"type:{event.type} - code:{event.code} - value:{event.value}")
                print(
                    f"ecodes.EV_ABS, ecodes.ABS_X, {current_x:=} ({prev_x:=})")
                print(
                    f"ecodes.EV_ABS, ecodes.ABS_Y, {current_y:=} ({prev_y:=})")
                gamepad.write(ecodes.EV_ABS, ecodes.ABS_X, current_x)
                gamepad.write(ecodes.EV_ABS, ecodes.ABS_Y, current_y)
                gamepad.syn()

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        # Clean up
        mouse.close()
        gamepad.close()


def main():
    parser = argparse.ArgumentParser(
        description="Map mouse movements to a virtual gamepad")
    parser.add_argument("config", help="Path to configuration file")

    args = parser.parse_args()

    config = Config.from_file(Path(args.config))

    map_mouse_to_gamepad_stick(config)


if __name__ == "__main__":
    main()
