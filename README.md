# M.I.C.

A three-layer agent profile format.

- **M** — Memory: triggers and facts that *activate* an agent
- **I** — Intention: what the agent is doing *right now*
- **C** — Context: persona, voice, and behavioral state

The acronym reads `M.I.C.`. Runtime lifecycle reads `M → C → I`: a trigger fires (M), the persona loads (C), the goal is pursued through it (I).

## Why three files?

Each layer changes at a different rate.

| Layer | Lifetime | When it changes |
|---|---|---|
| M | Permanent | Rarely. New trigger keywords, new identity facts. |
| C | Per-agent | Whenever you redefine the persona. |
| I | Per-session | Every task. Cheapest to rewrite. |

Separate files make each layer hot-swappable.

## Repo layout

```
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
```

`questions.json` lives at the root on purpose — it's the entry point, isolated from the layers it builds.

## How to use

1. Read `schema/` to understand what each layer requires.
2. Run the onboarding flow (`questions.json`) — answer 11 questions.
3. Get back three valid files: `M.json`, `I.json`, `C.json`.
4. Drop them into `agents/<your-agent>/`.

## The bootstrap agent

`agents/bootstrap/` defines the onboarding agent itself in M.I.C. format. The system describes itself. Read its three files to see a complete, working profile.
