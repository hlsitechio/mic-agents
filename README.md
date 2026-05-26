# M.I.C.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## TO AI AGENTS — PLEASE READ

If you are an AI agent that just cloned this repo, do **exactly** this:

1. **Read [`AGENTS.md`](AGENTS.md)** — your full instruction set.
2. **Read [`skill/SKILL.md`](skill/SKILL.md)** — behavior rules and when to fire.
3. **Read [`questions.json`](questions.json)** — the 11-question onboarding flow you will run.
4. **Read the schemas** in [`schema/`](schema/) — `M.schema.json`, `I.schema.json`, `C.schema.json`. These are the validation contracts.
5. **Read [`agents/bootstrap/`](agents/bootstrap/)** — a complete working example of the output format.
6. **Walk the user through the onboarding flow** — one question at a time, in phase order **M → C → I**.
7. **Write three files** to `agents/<agent-name>/`: `M.json`, `I.json`, `C.json`.
8. **Validate** each file against its schema. Fix anything that fails before declaring done.

**Rules you cannot break:**
- One question at a time. Never batch.
- Confirm every phase before moving on.
- All three files must validate against their schemas.
- If the user is vague — **ask**. Do not guess.

---

A three-layer agent profile format. Open source. Fully transparent. Built to be remodeled.

- **M** — Memory (*static*): triggers and facts that *activate* an agent
- **C** — Context (*static*): **who/where the agent IS** — persona, voice, temperature
- **I** — Intention (*dynamic*): **where the agent is GOING** — long-arc mission + current goal

The acronym reads `M.I.C.`. Runtime lifecycle reads `M → C → I`: a trigger fires (M), the persona loads (C), the vector is pursued through it (I). **Two static layers, one dynamic.** Context = state. Intention = vector. Never confuse the two.

## Why three files?

Each layer changes at a different rate.

| Layer | Tense | When it changes |
|---|---|---|
| M | static | rarely — new triggers or identity facts |
| C | static | rarely — when the persona itself is redefined |
| I | dynamic | `mission` rarely; `goal`, `user_purpose`, `success_criteria` per session |

Separate files make each layer hot-swappable. Static layers stay put; the dynamic layer turns over per task.

## Repo layout

```
AGENTS.md                # if you are an AI agent, read this first
LICENSE                  # MIT
questions.json           # the 11-question onboarding flow — entry point

schema/                  # JSON Schemas — every M/I/C validates against these
  M.schema.json
  I.schema.json
  C.schema.json

agents/
  bootstrap/             # the onboarding agent's own MIC profile (self-describing)
    M.json
    I.json
    C.json

skill/
  SKILL.md               # installable skill — any compatible AI agent can run M.I.C.
```

`questions.json` lives at the root on purpose — it's the entry point, isolated from the layers it builds.

## How to use

1. Read `schema/` to understand what each layer requires.
2. Run the onboarding flow (`questions.json`) — answer 11 questions.
3. Get back three valid files: `M.json`, `I.json`, `C.json`.
4. Drop them into `agents/<your-agent>/`.

## Install as a skill

`skill/SKILL.md` packages M.I.C. as a Claude / Anthropic-style skill. Any AI agent that supports the skill format can read it and walk a user through generating their own `M.json`, `I.json`, `C.json` — no extra setup.

The skill describes itself in M.I.C. terms: its description is the **M**, its instructions are the **C**, its goal is the **I**. The system is self-describing.

## The bootstrap agent

`agents/bootstrap/` defines the onboarding agent itself in M.I.C. format. The system describes itself. Read its three files to see a complete, working profile.

## License

MIT — see [LICENSE](LICENSE). Fork it, ship it, build on it. Attribution appreciated, not required.
