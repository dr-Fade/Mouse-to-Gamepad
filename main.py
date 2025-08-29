import argparse
from pathlib import Path

from evdev import InputDevice, UInput, ecodes

from config import Config


ABS_BOUNDARY = 32767
SENSITIVITY_SCALING = 1 / 50


def create_gamepad_device(config: Config) -> None:
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


def map_mouse_to_gamepad_stick(config: Config) -> None:
    gamepad = create_gamepad_device(config)
    mouse = InputDevice(config.mouse_device)

    sensitivity: float = config.sensitivity * ABS_BOUNDARY * SENSITIVITY_SCALING

    x, y = 0, 0

    try:
        for event in mouse.read_loop():
            if event.type == ecodes.EV_REL:
                if event.code == ecodes.ABS_X:
                    x = int(event.value * sensitivity)
                elif event.code == ecodes.ABS_Y:
                    y = int(event.value * sensitivity)
                else:
                    continue

                gamepad.write(ecodes.EV_ABS, ecodes.ABS_X, x)
                gamepad.write(ecodes.EV_ABS, ecodes.ABS_Y, y)
                gamepad.syn()

            if event.type == ecodes.EV_KEY:
                if event.code == ecodes.BTN_LEFT:
                    key = ecodes.BTN_A
                elif event.code == ecodes.BTN_RIGHT:
                    key = ecodes.BTN_B
                else:
                    continue

                gamepad.write(ecodes.EV_KEY, key, event.value)
                gamepad.syn()

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
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
