---
name: research
description: The backbone. Takes the picked item and researches it like a scientist — question, prior work, observation with file:line or API output, hypotheses with a kill-fact each, cheap experiments, conclusion with confidence — then writes 01-research.md (method log + a five-section report) and gives a chat summary in plumber language. Config-lane items get a short 01-plan.md instead. Writes no source code. Stops for your verdict; on approval the plan is frozen and /build executes it.
disable-model-invocation: true
---

# /research — find out, then say it plainly

Step 1 of the loop. The document this skill writes is the **only** one `/build` and `/verify` read. Nothing downstream may know anything it does not say.

## Precondition
`docs/worklog/STATE.md` → In progress row at phase `picked`. Otherwise stop and say which phase it is at and which skill handles it. Read the row's **lane**: `code` → the full method below; `config` → **Config lane** at the end.

## The method (code lane; in this order, each step logged)
1. **Frame the question.** Rewrite the pick as one precise question with a success condition you can observe ("when X, Y happens, seen as Z"). If it cannot be framed, stop and ask — unframed research wanders.
2. **Prior work.** Before reading code, read what the repo already knows: the plan doc STATE's Position names, `docs/architecture.md` / `docs/dev-boundaries.md` for the area, `HISTORY.md` lines about it, earlier `01-*.md` in `docs/worklog/`, negative results in memory. Cite conclusions already reached; never re-derive them. A conclusion you would reverse is **flagged as a reversal** and becomes a decision for the user.
3. **Observe.** Read the code the item touches and trace the real flow end to end: entry point → touch point → out. For ERPNext behaviour, read the source in the running image (`docker compose -p merchant-erp -f infra/compose.local.yaml exec backend …`) or `vendor/` — **read only** — and find the extension point on the ladder (`docs/dev-boundaries.md` §2), lowest rung that works. Record each fact as `file:line — what it does` or `command → output`. Where behaviour can be observed (call the API, run the existing test), observe it instead of inferring. Keep **observations** and **inferences** in two separate lists.
4. **Hypotheses.** Two or three candidate designs. Each as a prediction: what changes · which ladder rung · what it costs · what it would break · **the fact that would prove it wrong**. A candidate with no kill-fact is not a candidate.
5. **Experiment.** Try to kill each candidate cheaply before anyone builds it: grep every caller; check the hook/override really exists in the installed version; call the API on the live site; a ≤10-line spike in the scratchpad if only running code answers it (thrown away). Log `command → output`. **Keep negative results.**
6. **Conclude.** Pick the survivor on the logged facts. Confidence in one word (high / medium / low) plus the reason. List every **unknown** and how it would be learned — each becomes a test in §5 or a question to the user.
7. **Write up** (`01-research.md`, below). 8. **The stop.**

Budget: if step 3 or 5 is not converging after a bounded effort, stop and report what you have and what blocks you. Do not keep reading files.

## `01-research.md`
Frontmatter: `date, session, task, lane: code, phase: research, status: awaiting-verdict, plan-ref` (the `docs/phased-plan.md` phase). Then the handoff card (`docs/ai-workflow.md` §2.1). Then two parts:

**Part A — Method log.** Question · Prior work (cited) · Observations · Inferences · Hypotheses (with kill-facts) · Experiments (`command → output`, negatives included) · Conclusion (confidence + reason) · Unknowns.

**Part B — Report.** Five fixed sections, always these, always in this order:
1. **Today.** What exists now where this item lands. Repair: the fault, where it lives, how a merchant sees it. New thing: the nearest existing pieces (ours or ERPNext's) it connects to, and the gap. Every fact `file:line` or `command → output`.
2. **What we add or change.** One line per file or per ERPNext record (Custom Field, Client Script, DocType…): *now → after*. New file: its one job, and why no existing file could carry it.
3. **How it is built.** The change per file, in build order, plain words. Name every plug-in point into ERPNext (hook name, doctype, ladder rung). Code only when a line of code is clearer than the words.
4. **The house after.** The flow once this is in. If nothing above file level changes, one line says so.
5. **The tests.** One test per claim the report makes: `name · layer (unit / check / human) · what it checks · what PASS means · cost (none / needs-stack / needs-human)`. At least one test proves the **plug-in point** (e.g. the hook actually fires on a real Sales Invoice), not just the piece. Money and tax assertions are exact.
Then **Alternatives**: one line each — what it would buy, the fact that killed it (from Part A).

Rules: every claim about current code or ERPNext behaviour has a `file:line` or a `command → output`; anything else is marked **UNVERIFIED**. No theory unless a decision depends on it, then one sentence. No adjectives doing the arguing. Check the plan against `docs/ai-workflow.md` §1 — an invariant it would bend is a decision, not a footnote.

## The stop
1. STATE → In progress phase `research`. Append to `HISTORY.md`: `- YYYY-MM-DD · <session> · research · <task> · <confidence>`.
2. 🛑 **STOP.** The chat message is the **plumber summary**: Part B's five sections, compressed, same order, same headings, nothing the report does not say. Bounds: each section ≤5 lines; §2 and §5 one line per item. Then one line: confidence + the unknowns. Then **Decisions needed**, each in §2.2 shape. End with the path to the document and "say go to freeze it".

## On "go"
Set `status: approved`, STATE phase `approved`, HISTORY line `approved`. §2, §3, §5 (config lane: the whole plan) are now **frozen**: `/build` may not change them, `/verify` may not weaken the tests. Say "run `/build`".

## Config lane — `01-plan.md`
For items with no code (`docs/ai-workflow.md` §2). Skip hypotheses and experiments unless a real fork exists (then it is a Decision). Still observe before planning: read the current values on the live site (`command → output`) — never plan against assumed defaults.
Frontmatter: `date, session, task, lane: config, phase: research, status: awaiting-verdict, plan-ref`. Then four short sections:
1. **Today** — the current state on the site, observed.
2. **What we set** — one line per record/setting: *now → after*, with every value written out (no "sensible defaults").
3. **How** — UI path or API call per line, in order; anything scripted is a throwaway in the scratchpad unless the plan says it is kept (then it is code → re-lane).
4. **The checks** — same shape as §5 above; each one says what PASS means in numbers or exact values.
The stop and "go" are as above. If observing shows the item needs code, stop and present re-laning as a Decision.

## Guardrail — never spin
Not converging, or going in circles: stop and hand the user what you tried, what blocks you, and the partial hypotheses, in §2.2 shape. Never write source code here.
