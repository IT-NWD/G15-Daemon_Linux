"""Distribution-neutral discovery of paths and external Linux tools."""

from __future__ import annotations

import os
import re
import shutil
import sys
from pathlib import Path


def user_config_path() -> Path:
    root = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return Path(os.environ.get("G15_PROFILE_PATH", root / "g15daemon/g15.conf"))


def find_tool(environment_name: str, default_name: str) -> str:
    override = os.environ.get(environment_name)
    command = override or shutil.which(default_name)
    if not command:
        raise OSError(f"{default_name} wurde nicht gefunden ({environment_name} kann den Pfad setzen).")
    return command


def system_apply_command(helper: Path, profile: Path, brightness: int) -> list[str]:
    if not sys.platform.startswith("linux"):
        raise OSError("Die systemweite keyd-Übernahme wird derzeit nur unter Linux unterstützt.")
    selected_helper = Path(os.environ.get("G15_INSTALL_HELPER", helper))
    if not selected_helper.exists():
        raise OSError(f"Installationshelfer nicht gefunden: {selected_helper}")
    return [find_tool("G15_PKEXEC", "pkexec"), str(selected_helper),
            str(profile), str(brightness)]


def local_file_path(file) -> Path:
    if file is None or file.get_path() is None:
        raise OSError("Es werden derzeit nur lokale Dateien unterstützt.")
    return Path(file.get_path())


def safe_profile_filename(name: str) -> str:
    stem = re.sub(r"[^A-Za-z0-9._-]+", "-", name.strip()).strip("-.")
    return f"{stem or 'g15-profile'}.conf"
