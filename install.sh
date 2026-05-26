#!/usr/bin/env bash
# M.I.C. one-click installer for macOS / Linux.
# Adds <this folder>/bin to your user PATH and writes ~/.mic/config.json.
# Safe to run multiple times - idempotent.
set -e
python3 "$(dirname "$0")/install.py"
