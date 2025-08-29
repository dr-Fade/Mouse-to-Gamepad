#!/usr/bin/env python3

import argparse
from pathlib import Path
import json
from dataclasses import dataclass, field, asdict
from evdev import list_devices, InputDevice


DEFAULT_CONFIG_FILE = Path(__file__).parent.absolute() / "config.json"


@dataclass
class Config:
    mouse_device: str = field()
    gamepad_name: str = field(default="Virtual Gamepad")
    sensitivity: float = field(default=0.5)
    vendor: int = field(default=0x1234)
    product: int = field(default=0x5678)
    version: int = field(default=0x100)

    @classmethod
    def from_file(cls, file: Path):
        return cls.from_json(file.read_text())

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls(**data)
    
    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=4)


def pick_mouse_device() -> str:
    devices = (InputDevice(dev) for dev in list_devices())
    mouse_devices = [dev for dev in devices if "mouse" in dev.name.lower()]

    for i, dev in enumerate(mouse_devices):
        print(f"{i}: {dev.name}")

    choice = int(input("Select the mouse device: "))
    selected_device = mouse_devices[choice]

    return selected_device.path


def pick_virtual_gamepad_name() -> str:
    return str(input("Enter the new gamepad name: "))


def pick_sensitivity() -> float:
    return float(input("Enter the sensitivity of the gamepad sticks [0-1]: ") or 0.5)


def main():
    parser = argparse.ArgumentParser(
        description="Create config file for the mouse to gamepad mapper.")
    parser.add_argument("--config-path", help="Path to the configuration file", required=False, default=None)

    args = parser.parse_args()

    config = Config(
        mouse_device=pick_mouse_device(),
        gamepad_name=pick_virtual_gamepad_name(),
        sensitivity=pick_sensitivity()
    )

    print(f"Created new config: {config.to_json()}")

    # Save configuration to file
    config_file = args.config_path or DEFAULT_CONFIG_FILE
    config_file.parent.mkdir(parents=True, exist_ok=True)
    config_file.write_text(json.dumps(asdict(config), indent=2))

    print(f"Config saved to {config_file}")


if __name__ == "__main__":
    main()
