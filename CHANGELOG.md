# Changelog

All notable changes to this project are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/). Versioning follows [SemVer](https://semver.org/).

## [0.5.0] — 2026-05-26

### Added
- **`--agent <name>` flag on `launch.py`** — skips the interactive menu and activates an agent directly. Case-insensitive folder lookup. If the name doesn't match, prints the list of available agents and exits with an error.
- **`bin/mic.cmd`** — generic terminal wrapper. `mic` opens the interactive menu; `mic <name>` activates by name. Works from any cwd.
- **`bin/mic-bootstrap.cmd` and `bin/mic-lavey.cmd`** — per-agent one-word shortcuts. `mic-lavey` from any PowerShell window opens a Claude Code session already as Lavey.
- **Two parallel triggers per agent** — bootstrap onboarding now generates both a slash command (`/lavey` for in-session use) AND a terminal wrapper (`mic-lavey` for shell use) at the end of each onboarding flow. New agents are reachable from either surface automatically.

### Why
v0.4 made activation one keystroke inside Claude Code. v0.5 makes it one keystroke from anywhere — terminal or in-session — with no asymmetry.

### PATH setup (one-time)
Add `G:\MIC\bin` to your user PATH:
```powershell
[Environment]::SetEnvironmentVariable("PATH", "$env:PATH;G:\MIC\bin", "User")
```

## [0.4.1] — 2026-05-26

### Fixed
- `/agent-launcher` slash command shell quirks on Windows. The body now explicitly tells Claude that the Bash tool runs Git Bash (not PowerShell), and to use `$HOME` / bash conditionals / Write tool with absolute paths. Resolves the `$env:USERPROFILE` mis-expansion that caused the config persistence step to fail.

## [0.4.0] — 2026-05-26

### Added
- **Smart `/agent-launcher`** — first-run detection cascade (`$ARGUMENTS` → `~/.mic/config.json` → `$MIC_HOME` → ancestor MIC repo → `G:\MIC` default → ask the user). The resolved path is persisted to `~/.mic/config.json` so subsequent runs are instant. If no install is found, the launcher offers to `git clone` from GitHub.
- **Per-agent slash commands** — `bootstrap.md` and `lavey.md` ship as project-local slash commands at `.claude/commands/`. Direct activation with `/lavey`, `/bootstrap`, etc. — no menu, no number-picking. Onboarding now auto-generates a per-agent slash command at the end of the flow, so every new agent gets its own one-keystroke trigger.
- **First user agent: Lavey** at `agents/Lavey/` — a funny exploratory web-surfing companion built during real test-driving in the previous session. Lives in the canonical install.
- **Empty-library handling** — if only `bootstrap` is present, the launcher offers to onboard the user's first real agent rather than show an empty menu.
- **"Create a new agent" menu option** — when listing agents, the launcher includes `c` as a final option that routes to bootstrap onboarding without a separate command.

### Why
v0.3 made M.I.C. executable. v0.4 makes it ergonomic. The slash command IS the trigger — M.triggers in JSON describe intent, but the actual activation is one keystroke. Each agent gets its own first-class command.

## [0.3.0] — 2026-05-26

### Added
- **`launch.py`** at the repo root — the first M.I.C. *runtime*. Scans `./agents/` (or a custom path) for valid agent profiles, presents a numbered menu, and launches Claude Code with the chosen agent's M + I + C injected via `--append-system-prompt`. Cross-platform Python, stdlib only.
- **`/agent-launcher` slash command** in `.claude/commands/` — invokes `launch.py` from inside any Claude Code session opened in the repo.

### Why
M.I.C. was a *format* before this release. With a launcher, it is a *system* — agents become executable. The M-layer triggers, which were always meant to be activation keys, finally have a listener.

## [0.2.0] — 2026-05-26

### Changed (breaking)
- **`C.json` no longer has `why_here`.** The Context layer is now purely *static state* — `persona`, `voice_tone`, `temperature`. Three fields.
- **`I.json` now requires `mission`.** The Intention layer is *dynamic vector* — long-arc `mission` (stable across sessions) plus short-arc `goal`, `user_purpose`, `success_criteria` (rewritten per session). Four fields.
- The conceptual frame: **Context = state** (where/who you are). **Intention = vector** (where you are going). Two static layers (M, C), one dynamic (I).

### Migration from 0.1.x
- Move the content of `C.why_here` → `I.mission`.
- Remove `why_here` from `C.json`.
- Add a `mission` field to `I.json` (free-form string, long-arc reason for being).
- Existing `M.json` files require **no change**.

### Docs
- `README.md`, `AGENTS.md`, and `skill/SKILL.md` updated to teach the static/dynamic split.
- `questions.json` bumped to version `0.2.0`. Total question count unchanged (11 — distributed `4 + 3 + 4`).

## [0.1.0] — 2026-05-26

### Added
- Initial M.I.C. agent profile format: three-layer JSON (`M.json`, `I.json`, `C.json`) per agent.
- JSON Schemas for each layer in `schema/`.
- Self-describing bootstrap agent in `agents/bootstrap/`.
- 11-question onboarding flow in `questions.json`.
- `AGENTS.md` — cold-start instruction file for AI agents.
- `skill/SKILL.md` — installable skill packaging.
- `LICENSE` — MIT.
