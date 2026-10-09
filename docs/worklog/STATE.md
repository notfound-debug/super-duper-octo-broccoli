# Worklog — STATE (the only tracker file the skills read)

Keep this file **under 100 lines**: facts, not narrative. Every event gets one line in `HISTORY.md`
(append-only). Per work item a folder `YYYY-MM-DD__<session>__<task-slug>/` holds, by lane:
**code** `01-research.md` → `02-build.md` → `03-verify.md` · **config** `01-plan.md` → `02-done.md`.
Each document is topped by the handoff card (`docs/ai-workflow.md` §2.1).
**Phases:** `picked` → `research` → `approved` → `implemented` (code only) → `verified`/`done` · or `blocked`.

_Last updated: 2026-10-09 (session `setup`): workflow adopted; Phase 0 base install done._

## Position
- **Strategy:** Path A ("feed Tally") — ruled 2026-10-09. Sequencing source of truth: `docs/phased-plan.md`.
- **Current phase:** **Phase 0 — Foundation & validation** (record: `docs/phase-0-log.md`).
  - ✅ Base install: site `merchant.localhost` on <http://localhost:8080> — frappe 16.51.0, erpnext 16.50.0,
    india_compliance 16.10.0 (`bench list-apps`, 2026-10-09); scheduler enabled. Stack: `infra/erp.sh`.
  - ✅ Trademark policy read (`docs/phase-0-log.md` §5).
  - ⬜ Sample Indian retail company (GST, HSN, tax slabs, items, supplier, customer) — setup wizard not yet run.
  - ⬜ GST invoice + GSTR-1/3B + P&L/balance sheet check.
  - ⏸️ Handwriting spike → `docs/backlog.md` (ruled 2026-10-09; gates Phase 4 only).
- **Phase 0 exit:** base runs ✅; GST/audit reports confirmed ⬜.
- **Workflow rulings 2026-10-09:** two lanes (code/config) · API checks now, browser checks from Phase 1 ·
  no feature toggles until real shops · branch + PR off `master`, hooks deny push-master/force/vendor edits, ask on commit.
- **Repo:** `master` @ `de77b88` + uncommitted: docs fixes, `infra/`, `.claude/` workflow, `docs/worklog/`.

## In progress
| Task | Lane | Session | Phase | Folder | Date |
|---|---|---|---|---|---|
| — | | | | | |

## Owed gates (human)
| Gate | Who | Since | Folder / note |
|---|---|---|---|
| Choose the product name (constraints: `docs/phase-0-log.md` §5) | maintainer | 2026-10-09 | — |
| Line up 2–3 friendly merchants + 1 CA for validation | maintainer | 2026-10-09 | `docs/phased-plan.md` §6.4 |

## Current menu
_(not yet surveyed — run `/next`)_
