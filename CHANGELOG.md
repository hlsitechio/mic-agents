# Changelog

All notable changes to this project are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/). Versioning follows [SemVer](https://semver.org/).

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
