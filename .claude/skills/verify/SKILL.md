---
name: verify
description: Execute §5 of the approved research report — the tests you approved before any code existed. Shows you the test table once more (name · layer · checks · PASS means · cost), confirms, writes exactly those tests, runs them, reports green / red / skipped with raw output. A red is reported with a root-cause class and your ruling is executed; a test is never weakened. Code lane only (config items are checked inside /build). Use after /build is reviewed.
disable-model-invocation: true
---

# /verify — run the tests you approved

Step 3 of the loop (code lane). Independence does not come from a second author; it comes from the fact that §5 was written and approved **before** the code existed and `/build` could not touch it. Your job is to run §5 faithfully and report what happened.

## Precondition
`docs/worklog/STATE.md` → In progress row at phase `implemented`, lane `code`. Read `01-research.md` Part B §5 (frozen) and `02-build.md` (checklist + deviations).

## Step A — confirm the table  (Gate 1)
1. Rebuild §5 as a table: `| Test | Layer | What it checks | PASS means | Where it lives | Cost |`. "Where" per `docs/ai-workflow.md` §3: unit → `test_*.py` in our app (run by `infra/erp.sh test`); check → `qa/checks/<name>.py` (stdlib Python against the live site's REST API, hard PASS/FAIL, exit non-zero on FAIL); human → an **Owed gate**. Cost: `none` · `needs-stack` · `needs-human (<who>)`.
2. If `02-build.md` lists a **deviation** that §5 does not cover, add a row marked **proposed** and say why — the user accepts or rejects it. If a §5 row has become impossible as written, say so and why; **do not substitute an easier test silently**.
3. If any row is `needs-stack`, check the stack is up (`curl -s http://localhost:8080/api/method/ping`) and say so in the table.
4. Write `03-verify.md` (frontmatter `phase: verify`, handoff card at the top, the table).
5. 🛑 **STOP.** Chat = the table, then one question per `proposed` row and per `needs-human` row: run now, or record as an owed gate. Nothing else.

## Step B — write, run, report  (Gate 2)
1. Write **exactly the confirmed rows**, one test per row, the §5 claim quoted in the test's docstring. Checks create their own test data with a recognisable prefix (e.g. `QA-<task>-`) and never depend on records a person made by hand. Credentials are read from `infra/.env.local`, never written into a test or its output.
2. Run. **Green must mean "ran"**: a check that cannot run (stack down, prerequisite missing) prints SKIPPED with the reason and is reported as skipped, never as a pass.
3. Results table: `| Test | Result | Evidence |` with Result ∈ **green / red / skipped (why)**; evidence = test name, check name with the numbers it printed, or the exact failure line.
4. **Any red: stop. Do not fix. Do not rerun until green.** Report in `docs/ai-workflow.md` §2.2 shape: the test, its raw failure output, your root-cause class — **real defect** / **wrong test** / **spec gap** (the report claimed something the code was never asked to do) — then every option at equal depth (fix the code · amend the report and record the test as testing a withdrawn claim · accept the defect) with effort and what each gives up. One decision per root cause. **Execute only the user's ruling**; the rerun after an approved fix is confirmatory.
5. Append to `03-verify.md` (`phase: verified`): the results table, skipped count with reasons, **what was proved** and **what was not** in plain words, evidence pointers. Rewrite the card at the top to match. Changing an assertion, weakening a bound, or deleting a test to reach green is **forbidden**.
6. STATE: remove the In-progress row (or set `blocked` on an unruled red); any human gate left open → **Owed gates** with the folder; advance **Position** if a phase step moved. Append to `HISTORY.md`: `- YYYY-MM-DD · <session> · verified|blocked · <task> · <n green / n red / n skipped> · <commit if any>`.
7. 🛑 **STOP.** Chat = the results table, then "proved / not proved" in ≤5 lines, then Decisions needed in §2.2 shape, then "the loop returns to `/next`".

## Guardrail — never spin
A check failing repeatedly for environmental reasons (stack flapping, site not responding), or a harness with no clear verdict: stop after a bounded number of attempts and hand the user the unedited output, what it does and does not tell us, and the options including declaring the result inconclusive. Do not loop trying to make it pass.
