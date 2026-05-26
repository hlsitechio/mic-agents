#!/usr/bin/env python3
"""
M.I.C. Launcher - pick an agent and start a Claude Code session with that
agent's M + I + C profile loaded into the system prompt.

Usage:
    python launch.py                    # scan ./agents/
    python launch.py /path/to/agents    # scan a custom folder

An agent folder must contain three files: M.json, I.json, C.json.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

REQUIRED_FILES = ("M.json", "I.json", "C.json")


def discover_agents(agents_dir: Path) -> list[tuple[Path, dict, dict, dict]]:
    """Return [(folder, M, I, C), ...] for every valid agent in agents_dir."""
    if not agents_dir.is_dir():
        print(f"Error: {agents_dir} is not a directory.", file=sys.stderr)
        sys.exit(1)

    agents: list[tuple[Path, dict, dict, dict]] = []
    for d in sorted(agents_dir.iterdir()):
        if not d.is_dir():
            continue
        if not all((d / f).exists() for f in REQUIRED_FILES):
            continue
        try:
            m = json.loads((d / "M.json").read_text(encoding="utf-8"))
            i = json.loads((d / "I.json").read_text(encoding="utf-8"))
            c = json.loads((d / "C.json").read_text(encoding="utf-8"))
            agents.append((d, m, i, c))
        except (json.JSONDecodeError, OSError) as e:
            print(f"  [skip] {d.name}: {e}", file=sys.stderr)
    return agents


def show_menu(agents: list[tuple[Path, dict, dict, dict]]) -> tuple[Path, dict, dict, dict]:
    print()
    print(f"M.I.C. - found {len(agents)} agent(s):")
    print()
    for idx, (folder, _m, _i, c) in enumerate(agents, 1):
        persona = c.get("persona", "(no persona)")
        print(f"  {idx}. {folder.name:<20} - {persona}")
    print()

    while True:
        choice = input("Select an agent (number, or q to quit): ").strip()
        if choice.lower() in ("q", "quit", "exit"):
            sys.exit(0)
        try:
            n = int(choice)
            if 1 <= n <= len(agents):
                return agents[n - 1]
        except ValueError:
            pass
        print("Invalid choice. Try again.")


def build_prompt(folder: Path, m: dict, i: dict, c: dict) -> str:
    """Compose M + I + C into a single system-prompt block."""
    return f"""You are now operating as the M.I.C. agent named '{folder.name}'.

This is your profile. Embody it fully - its persona, its voice, its mission.

## M - Memory (static: what activates you)
Triggers: {m.get("triggers")}
Identity facts: {m.get("facts")}
Quick recall: {m.get("quick_recall", [])}

## C - Context (static: who you are)
Persona: {c.get("persona")}
Voice and tone: {c.get("voice_tone")}
Temperature target: {c.get("temperature")}

## I - Intention (dynamic: where you are going)
Mission (long-arc, stable): {i.get("mission")}
Goal (current session): {i.get("goal")}
User purpose: {i.get("user_purpose")}
Success criteria: {i.get("success_criteria")}

Hold these as your identity. Speak in the voice from C. Pursue the mission and goal from I.
When the user invokes one of your M triggers, respond as this agent.
"""


def launch_claude(system_prompt: str) -> None:
    if shutil.which("claude") is None:
        print(
            "Error: the `claude` CLI was not found on PATH.\n"
            "Install Claude Code first, then re-run.",
            file=sys.stderr,
        )
        sys.exit(1)

    print()
    print("Launching Claude Code with this profile loaded...")
    print()
    subprocess.run(["claude", "--append-system-prompt", system_prompt])


def main() -> None:
    agents_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("./agents")
    agents = discover_agents(agents_dir)
    if not agents:
        print(f"No valid M.I.C. agents found in {agents_dir}.")
        print("Each agent folder must contain M.json, I.json, and C.json.")
        sys.exit(1)
    chosen = show_menu(agents)
    prompt = build_prompt(*chosen)
    launch_claude(prompt)


if __name__ == "__main__":
    main()
