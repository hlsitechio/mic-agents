---
description: Pick a M.I.C. agent profile from ./agents/ and launch a Claude Code session that embodies it.
---

Run the M.I.C. launcher to start a new Claude Code session with a selected agent's profile loaded.

Execute this command in the repo root:

```
python launch.py
```

The launcher will:
1. Scan `./agents/` for every folder containing `M.json`, `I.json`, and `C.json`.
2. Display a numbered list of valid agents with their persona descriptions.
3. Prompt the user to pick a number.
4. Read the chosen agent's three files, compose them into a single system prompt block (M = triggers + facts, C = persona + voice + temperature, I = mission + goal + user purpose + success criteria).
5. Spawn `claude --append-system-prompt "<that block>"`, opening a new Claude Code session that embodies the agent.

If the user passes an alternate path (e.g. `python launch.py G:\Agents\some-other-folder\agents`), scan that folder instead of `./agents/`.

If the `claude` CLI is not on PATH, the launcher exits with a clear error.
