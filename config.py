#!/usr/bin/env python3

from pathlib import Path
import json
from dataclasses import dataclass, field

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
