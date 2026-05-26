#!/usr/bin/env python3
"""
M.I.C. Installer - one-shot setup.

What it does:
  1. Adds <mic_path>/bin to your user PATH so `mic`, `mic-lavey`, etc.
     work from any terminal (Windows: HKCU\\Environment via winreg;
     Unix: appends to ~/.bashrc or ~/.zshrc).
  2. Writes ~/.mic/config.json so `/agent-launcher` knows where MIC
     lives without prompting.

Cross-platform: Windows + macOS + Linux. Idempotent: safe to re-run.

Usage:
    python install.py            # install relative to this file's directory
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def install_path_windows(bin_dir: str) -> bool:
    """Add bin_dir to user PATH on Windows. Returns True if changed."""
    import ctypes
    import winreg

    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_READ
    ) as key:
        try:
            current, _ = winreg.QueryValueEx(key, "PATH")
        except FileNotFoundError:
            current = ""

    # Case-insensitive check on Windows
    if bin_dir.lower() in current.lower():
        print(f"  [skip] PATH already contains {bin_dir}")
        return False

    new = current + ";" + bin_dir if current else bin_dir
    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_WRITE
    ) as key:
        winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new)

    # Broadcast WM_SETTINGCHANGE so new processes pick up the new PATH
    HWND_BROADCAST = 0xFFFF
    WM_SETTINGCHANGE = 0x001A
    SMTO_ABORTIFHUNG = 0x0002
    ctypes.windll.user32.SendMessageTimeoutW(
        HWND_BROADCAST,
        WM_SETTINGCHANGE,
        0,
        "Environment",
        SMTO_ABORTIFHUNG,
        5000,
        None,
    )
    print(f"  [+] Added to user PATH: {bin_dir}")
    return True


def install_path_unix(bin_dir: str) -> bool:
    """Append PATH export to ~/.bashrc or ~/.zshrc. Returns True if changed."""
    shell = os.environ.get("SHELL", "")
    rc = Path.home() / (".zshrc" if "zsh" in shell else ".bashrc")

    if rc.exists():
        content = rc.read_text()
        if bin_dir in content:
            print(f"  [skip] {rc} already references {bin_dir}")
            return False

    line = f'\n# Added by M.I.C. installer\nexport PATH="$PATH:{bin_dir}"\n'
    with rc.open("a", encoding="utf-8") as f:
        f.write(line)
    print(f"  [+] Appended PATH export to {rc}")
    print(f"      Run: source {rc}   (or open a new shell)")
    return True


def write_config(mic_path: str) -> None:
    """Write ~/.mic/config.json with the resolved MIC path."""
    config_dir = Path.home() / ".mic"
    config_dir.mkdir(exist_ok=True)
    config_file = config_dir / "config.json"
    config = {
        "mic_path": mic_path,
        "saved_at": datetime.now().isoformat(timespec="seconds"),
    }
    config_file.write_text(json.dumps(config, indent=2), encoding="utf-8")
    print(f"  [+] Wrote config: {config_file}")


def main() -> None:
    mic_root = Path(__file__).resolve().parent
    bin_dir = mic_root / "bin"

    print("M.I.C. Installer")
    print(f"  MIC root: {mic_root}")
    print(f"  bin dir:  {bin_dir}")
    print()

    if not bin_dir.is_dir():
        print(f"Error: bin/ not found at {bin_dir}", file=sys.stderr)
        print(
            "This installer expects to live in the MIC repo root, "
            "next to launch.py and bin/.",
            file=sys.stderr,
        )
        sys.exit(1)

    print("Step 1 - Add bin/ to user PATH:")
    if sys.platform == "win32":
        install_path_windows(str(bin_dir))
    else:
        install_path_unix(str(bin_dir))

    print()
    print("Step 2 - Write config for /agent-launcher:")
    write_config(str(mic_root))

    print()
    print("Done. Open a NEW terminal window, then:")
    print("  mic              - interactive agent menu")
    print("  mic-lavey        - direct activation of Lavey")
    print("  mic-bootstrap    - the onboarder")
    print()
    print("Inside Claude Code, slash commands work as well:")
    print("  /agent-launcher")
    print("  /lavey")
    print("  /bootstrap")


if __name__ == "__main__":
    main()
