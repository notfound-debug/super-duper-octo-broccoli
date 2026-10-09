---
name: next
description: The menu. Reads STATE.md, routes you to the skill a work item in flight needs, otherwise shows the owed gates and a one-line-per-option menu (option · lane · effort · what it buys · what blocks it). Writes only the tracker. Researches nothing, proposes nothing, writes no code. Hands your pick to /research.
disable-model-invocation: true
---

# /next — the menu

Step 0 of the loop: `/next` → `/research` → `/build` → `/verify` (`docs/ai-workflow.md` §2). This skill keeps the tracker and shows options. Nothing else.

## First use in a session
Ask for a **one-word session label** (e.g. `gst`, `barcode`). If declined, use `s-<MMDD>-<2 random chars>`. Keep it for the session.

## Step 0 — route before you survey
Read `docs/worklog/STATE.md` only (≤100 lines; never `HISTORY.md` here). If **In progress** has a row, route by its phase and **stop**:
- `picked` → "run `/research`".
- `research` → re-emit that item's chat summary (from its `01-research.md` or `01-plan.md`) and ask for the verdict.
- `approved` → "run `/build`".
- `implemented` → "run `/verify`" (code lane only; a config item never sits here).
- `blocked` → show the recorded blocker in the `docs/ai-workflow.md` §2.2 shape (issue → options → recommendation) and ask for the ruling.

Survey only when nothing is in flight, or the user asks for a fresh menu.

## Step A — orient and show the menu
1. Read `docs/worklog/STATE.md`, `docs/phased-plan.md`, `docs/backlog.md`, `git log --oneline -15`. If STATE's Position names a current phase or plan doc, read it and **continue that plan** — do not re-derive it.
2. Rewrite STATE → **Position**: facts only, no narrative.
3. Show STATE's **Owed gates** table and ask, per row, **keep or drop**.
4. Show the **menu**. Every viable option, one line each, this exact shape:
   `- **<option>** · code/config · S/M/L · buys: <what you get, plain words> · blocked by: <the one fact that stops it, or "nothing">`
   Rules: name things by their repo / ERPNext names; lane per `docs/ai-workflow.md` §2 (code = any code; config = data, settings, installs, docs); no adjectives; "unmeasured" where nothing was measured; skip anything another session has In progress; no recommendation and no argument — the line is the whole case.
5. Rewrite STATE → **Current menu**. Append to `HISTORY.md`: `- YYYY-MM-DD · <session> · survey · <one line>`.
6. 🛑 **STOP.** Ask the user to pick (they may also overrule the lane).

## On the pick
1. Add a STATE → **In progress** row: task · lane · session · phase `picked` · folder `docs/worklog/<YYYY-MM-DD>__<session>__<task-slug>/` · date. Create the folder, empty.
2. Append to `HISTORY.md`: `- YYYY-MM-DD · <session> · picked · <task> · <lane>`.
3. Say "run `/research`" and stop.

## Guardrail — never spin
If you cannot form a menu (unclear position, contradicting docs), stop and say what you read, what contradicts what, and the partial menu you do have. Do not research options here; that is `/research`'s job.
