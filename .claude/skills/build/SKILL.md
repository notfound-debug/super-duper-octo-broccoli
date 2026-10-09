---
name: build
description: Execute the approved plan. Code lane — §3 of 01-research.md, file by file, under the ponytail skill (minimum code that works); never edits §5 (the tests); reports a checklist and hands to /verify. Config lane — applies 01-plan.md and runs its checks in the same run, then closes the item. Any disagreement between the plan and reality comes back to you as a decision, never a quiet choice. Use after /research is approved.
disable-model-invocation: true
---

# /build — execute the plan

Step 2 of the loop. You do what the approved document says, in its order. It is the whole spec; you do not add to it.

## Precondition
`docs/worklog/STATE.md` → In progress row at phase `approved`, and that folder's `01-research.md` or `01-plan.md` has `status: approved`. Otherwise stop and say so. Make sure you are on the item's branch (`<session>/<task-slug>` off `master`, `docs/ai-workflow.md` §6); create it if missing.

## Code lane
1. Read `01-research.md` Part B (§1–§5, Alternatives) and `docs/ai-workflow.md` §1 (invariants) and §6 (git). Invoke the **`ponytail`** skill (`.claude/skills/ponytail/SKILL.md`) — its ladder governs every line you write.
2. Create `02-build.md` with frontmatter (`date, session, task, lane: code, phase: build`) and copy §2 in as the **checklist**, every row `not started`. §5 is **not** copied and **not** touched — `/verify` owns it.
3. Implement **§3 in its order**, one file at a time, ticking the checklist as you go. Repo discipline: **never edit `vendor/`** (a hook denies it — do not work around it); extend ERPNext only through the rung §3 names; match surrounding style; existing tests stay **green**. Do not refactor anything the report did not name. No tests here beyond ponytail's one runnable check for non-trivial logic, and only if §5 does not already cover it.
4. **Stop for a decision** the moment any of these is true — record it in `02-build.md`, STATE → `blocked`, and ask in the `docs/ai-workflow.md` §2.2 shape (every option at equal depth, including "amend the report"):
   - the code or the live site disagrees with the report's §1;
   - §3 does not say what to do at a point you have reached;
   - a new dependency, a download, a scope change, a cost the user has not agreed to;
   - an invariant in `docs/ai-workflow.md` §1 would bend;
   - you are not confident. Decide nothing quietly.
5. Finish `02-build.md`: handoff card at the top; the **checklist** (`file · done / partial / not done · one line of what changed · file:function`); **Deviations from the report** (or "none"); **Ponytail notes** (what you did not write, what you reused); test-suite status.
6. STATE → phase `implemented`. Append to `HISTORY.md`: `- YYYY-MM-DD · <session> · implemented · <task> · <n files, test status>`.
7. 🛑 **STOP.** Chat = the checklist (one line per file), then Deviations, then Decisions needed in §2.2 shape, then "say go for `/verify`".

## Config lane
1. Read `01-plan.md` and `docs/ai-workflow.md` §1. Create `02-done.md` (frontmatter `lane: config, phase: build`) with §2 "What we set" as the checklist.
2. Apply §3 "How" in order, ticking each line, recording `command → output` (or the UI path and the resulting value read back from the site). Throwaway scripts live in the scratchpad, never in the repo.
3. Stop for a decision under the same triggers as the code lane — plus: the item turns out to need code (present re-laning to code).
4. Run **exactly** the plan's §4 checks. Results table `| Check | Result | Evidence |`, Result ∈ green / red / skipped (why). **Any red: stop. Do not fix, do not re-run until green** — report it in §2.2 shape with the raw output and a root-cause class (real defect / wrong check / plan gap); execute only the ruling.
5. All green (or skips the user accepted): handoff card at the top of `02-done.md`; remove the In-progress row; any human gate left open → **Owed gates**; advance **Position** if a phase step moved. `HISTORY.md`: `- YYYY-MM-DD · <session> · done · <task> · <n green / n red / n skipped>`.
6. 🛑 **STOP.** Chat = the checklist, the results table, "proved / not proved" in ≤5 lines, then "the loop returns to `/next`".

## Commits
**Only if the user asks** (the hook will ask you to confirm they did). On the item's branch, never `master`. End the message with the current model's `Co-Authored-By` line, never a hard-coded model name. Push only when asked.

## Guardrail — never spin
Repeated build, test or API failures after a bounded effort: stop and hand the user the raw output, what you have ruled out, and the options including abandoning the approach, in §2.2 shape. Do not loop.
