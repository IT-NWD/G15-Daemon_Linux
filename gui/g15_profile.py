"""Platform-independent data model for Logitech G15 v1 profiles."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

DEVICE_ID_PATTERN = re.compile(r"^[0-9a-fA-F]{4}:[0-9a-fA-F]{4}:[0-9a-fA-F]{8}$")
DEFAULT_DEVICE_ID = "0000:0000:95e990cb"
PROFILE_NAMES = ("m1", "m2", "m3")

@dataclass
class ProfileSet:
    device_id: str = DEFAULT_DEVICE_ID
    brightness: int = 2
    bindings: dict[str, list[str]] = field(default_factory=lambda: {
        name: ["noop"] * 18 for name in PROFILE_NAMES
    })

    def validate(self) -> None:
        if not DEVICE_ID_PATTERN.fullmatch(self.device_id):
            raise ValueError("Die Geräte-ID muss dem Muster 0000:0000:00000000 entsprechen.")
        if self.brightness not in (0, 1, 2):
            raise ValueError("Die Helligkeit muss 0, 1 oder 2 sein.")
        for profile in PROFILE_NAMES:
            values = self.bindings.get(profile, [])
            if len(values) != 18:
                raise ValueError(f"Profil {profile.upper()} benötigt genau 18 Belegungen.")
            if any(not value.strip() or "\n" in value or "\r" in value for value in values):
                raise ValueError(f"Profil {profile.upper()} enthält eine ungültige Belegung.")
