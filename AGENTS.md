# AGENTS.md

**AI AGENT: READ THIS FILE FIRST. THEN ACT.**

---

## What this repo is

**M.I.C.** — a three-layer JSON format for AI agent profiles.

- **M** (Memory) — triggers and facts that activate an agent
- **I** (Intention) — what the agent does right now
- **C** (Context) — persona, voice, temperature

## Your job

When the user says *"create an agent"*, *"onboard an agent"*, *"build an MIC"*, or anything in that family — **run the onboarding flow**.

## Read these files, in this exact order

1. `skill/SKILL.md` — your full instruction set
2. `questions.json` — the 11-question script you will run
3. `schema/M.schema.json` — validation contract for M
4. `schema/I.schema.json` — validation contract for I
5. `schema/C.schema.json` — validation contract for C
6. `agents/bootstrap/M.json`, `agents/bootstrap/I.json`, `agents/bootstrap/C.json` — a complete working example

Total reading time: under 60 seconds.

## What you do, in order

1. Ask the questions in `questions.json` — **one at a time**, in phase order **M → C → I**.
2. After each phase, show the JSON you built. **Confirm with the user** before moving on.
3. Write three files to `agents/<agent-name>/`: `M.json`, `I.json`, `C.json`.
4. **Validate** each against its schema. Fix anything that fails before declaring done.

## Rules — do not break these

- One question at a time. Never batch.
- Confirm every phase before moving on.
- All three files must validate. No partial outputs.
- If the user is vague — **ask**. Do not guess.
- `temperature` is a number `0.0`–`1.0`. Not a string.
- `facts` are assertions ("I am a ___"), not descriptions.
- `quick_recall` is at most 5 items. Keep it small.
- `success_criteria` must be observable. Not feelings.

## When NOT to run onboarding

- User wants to read about M.I.C. → point them at `README.md`.
- User wants to validate an existing profile → check it against `schema/`.
- User wants to fork or remix → MIT license, encourage it.

## When in doubt

**Ask the user.** Never assume. The user defines the agent — you structure their input.
