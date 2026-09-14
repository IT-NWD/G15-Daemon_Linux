"""Platform-independent data model for Logitech G15 v1 profiles."""

from __future__ import annotations

import re
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum

DEVICE_ID_PATTERN = re.compile(r"^[0-9a-fA-F]{4}:[0-9a-fA-F]{4}:[0-9a-fA-F]{8}$")
DEFAULT_DEVICE_ID = "0000:0000:95e990cb"
PROFILE_NAMES = ("m1", "m2", "m3")
DEFAULT_PROFILE_NAME = "Standardprofil"
WINDOWS_DEFAULT_BINDINGS = tuple(
    [f"f{number}" for number in range(1, 13)]
    + [str(number) for number in range(1, 7)]
)
MACRO_PATTERN = re.compile(r"^macro\((.*)\)$", re.DOTALL)
REPEATING_MACRO_PATTERN = re.compile(
    r"^macro2\((\d+),\s*(\d+),\s*macro\((.*)\)\)$", re.DOTALL
)


class ActionKind(str, Enum):
    DISABLED = "disabled"
    KEYSTROKE = "keystroke"
    MACRO = "macro"
    REPEATING_MACRO = "repeating_macro"
    ADVANCED = "advanced"


@dataclass(frozen=True)
class BindingAction:
    kind: ActionKind
    value: str = ""
    initial_delay: int = 600
    repeat_delay: int = 50

    def render(self) -> str:
        value = self.value.strip()
        if self.kind == ActionKind.DISABLED:
            return "noop"
        if not value or "\n" in value or "\r" in value:
            raise ValueError("Die Aktion darf nicht leer oder mehrzeilig sein.")
        if self.kind == ActionKind.MACRO:
            return f"macro({value})"
        if self.kind == ActionKind.REPEATING_MACRO:
            if not 1 <= self.initial_delay <= 9999 or not 1 <= self.repeat_delay <= 9999:
                raise ValueError("Makro-Verzögerungen müssen zwischen 1 und 9999 ms liegen.")
            return f"macro2({self.initial_delay}, {self.repeat_delay}, macro({value}))"
        if self.kind == ActionKind.ADVANCED and re.search(r"\bcommand\s*\(", value):
            raise ValueError("command(...) ist wegen der keyd-root-Rechte in der GUI gesperrt.")
        return value

    @classmethod
    def parse(cls, binding: str) -> "BindingAction":
        binding = binding.strip()
        if binding == "noop":
            return cls(ActionKind.DISABLED)
        match = REPEATING_MACRO_PATTERN.fullmatch(binding)
        if match:
            return cls(ActionKind.REPEATING_MACRO, match.group(3),
                       int(match.group(1)), int(match.group(2)))
        match = MACRO_PATTERN.fullmatch(binding)
        if match:
            return cls(ActionKind.MACRO, match.group(1))
        if re.fullmatch(r"(?:[CMASG]-)*[A-Za-z0-9_.+-]+", binding):
            return cls(ActionKind.KEYSTROKE, binding)
        return cls(ActionKind.ADVANCED, binding)


def disabled_bindings() -> dict[str, list[str]]:
    return {name: ["noop"] * 18 for name in PROFILE_NAMES}


@dataclass
class ProfileSet:
    name: str = DEFAULT_PROFILE_NAME
    device_id: str = DEFAULT_DEVICE_ID
    brightness: int = 2
    bindings: dict[str, list[str]] = field(default_factory=disabled_bindings)

    def validate(self) -> None:
        if not self.name.strip() or len(self.name.strip()) > 80 or any(
                character in self.name for character in "\r\n"):
            raise ValueError("Der Profilname muss 1 bis 80 Zeichen lang und einzeilig sein.")
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
            for value in values:
                BindingAction.parse(value).render()

    def copy_bank(self, source: str, target: str) -> None:
        if source not in PROFILE_NAMES or target not in PROFILE_NAMES:
            raise ValueError("Unbekannter M-Modus.")
        self.bindings[target] = deepcopy(self.bindings[source])

    def reset_bank(self, profile: str, use_windows_defaults: bool = False) -> None:
        if profile not in PROFILE_NAMES:
            raise ValueError("Unbekannter M-Modus.")
        self.bindings[profile] = list(
            WINDOWS_DEFAULT_BINDINGS if use_windows_defaults else ["noop"] * 18
        )
