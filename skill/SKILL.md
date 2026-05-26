---
name: mic
description: Define an AI agent in three layers — Memory (triggers and facts that activate it), Intention (current goal and success criteria), Context (persona, voice tone, temperature). Use when the user wants to create, onboard, or structure a new AI agent profile, or asks about the M.I.C. format.
---

# M.I.C. — Memory, Intention, Context

A three-layer JSON profile format for AI agents. This skill walks a user through generating a complete M.I.C. agent definition: three files (`M.json`, `I.json`, `C.json`) that together describe one agent.

## The three layers

Two static layers (state), one dynamic (vector):

- **M** (Memory, *static*) — triggers and facts that *activate* this agent profile. A stimulus layer, not a session log.
- **C** (Context, *static*) — **who/where the agent IS**: persona, voice tone, temperature. The stable home position, independent of any task.
- **I** (Intention, *dynamic*) — **where the agent is GOING**: long-arc `mission` (stable across sessions) + short-arc `goal`, `user_purpose`, `success_criteria` (rewritten per session).

Lifecycle: `M → C → I`. A trigger fires (M), the persona loads (C), the vector is pursued through it (I).

**Context = state. Intention = vector.** Never confuse the two. "Why does the agent exist?" is a `mission` (I), not a context field.

## When to use this skill

Trigger this skill when:

- The user says "create a new agent", "onboard an agent", "build an MIC profile", "make me an M.I.C.", or anything matching the format.
- The user asks how the M.I.C. format works.
- An existing agent profile needs validation, repair, or extension.

## How to onboard a new agent

All file paths below are relative to the repo root.

1. Read `questions.json` — it defines the exact 11-question flow in three phases.
2. Walk the user through the phases in order: **M → C → I**.
3. Ask **one question at a time**. Never batch.
4. After each phase, show the JSON you have built and **confirm with the user** before moving to the next phase.
5. At the end, write three files to `agents/<agent-name>/`:
   - `M.json`
   - `I.json`
   - `C.json`
6. Validate each file against its schema in `schema/`. If any field is missing or invalid, fix it before declaring done.

## Reference files to read first

- `schema/M.schema.json` — required fields and types for M
- `schema/I.schema.json` — required fields and types for I
- `schema/C.schema.json` — required fields and types for C
- `questions.json` — the verbatim onboarding flow
- `agents/bootstrap/` — a complete working M.I.C. agent (the onboarding agent itself, self-describing — read all three files to see the format in action)

## Rules

- One question at a time. Never batch.
- Confirm each phase before proceeding.
- All three files must validate against their schemas.
- If the user is vague, ask for clarification — do not guess.
- `temperature` must be a number between 0.0 and 1.0.
- `facts` are assertions ("I am a ___"), not descriptions.
- `quick_recall` is a small set (max 5 items) of must-remember rules.
- `mission` is the agent's long-arc reason for being — rarely changes.
- `goal` is the current session's target — rewritten per task.
- `success_criteria` apply to the `goal`, not the `mission`. Must be observable — something you can check, not a feeling.

## Self-reference

This skill is itself M.I.C.-shaped:

- **M** — the frontmatter `description` is what triggers this skill.
- **C** — this document body is the skill's static state (how it behaves).
- **I** — the skill's `mission` is "produce valid M.I.C. profiles forever"; its `goal` per session is "produce one valid M.I.C. profile for the user in front of me."

If you understand that recursion, you understand M.I.C.
