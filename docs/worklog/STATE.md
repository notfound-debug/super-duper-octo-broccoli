# Worklog — STATE (the only tracker file the skills read)

Keep this file **under 100 lines**: facts, not narrative. Every event gets one line in `HISTORY.md`
(append-only). Per work item a folder `YYYY-MM-DD__<session>__<task-slug>/` holds, by lane:
**code** `01-research.md` → `02-build.md` → `03-verify.md` · **config** `01-plan.md` → `02-done.md`.
Each document is topped by the handoff card (`docs/ai-workflow.md` §2.1).
**Phases:** `picked` → `research` → `approved` → `implemented` (code only) → `verified`/`done` · or `blocked`.

_Last updated: 2026-10-13 (session `phase0`): sample retail company done (12/12 green)._

## Position
- **Strategy:** Path A ("feed Tally") — ruled 2026-10-09. Sequencing source of truth: `docs/phased-plan.md`.
- **Current phase:** **Phase 0 — Foundation & validation** (record: `docs/phase-0-log.md`).
  - ✅ Base install: site `merchant.localhost` on <http://localhost:8080> — frappe 16.51.0, erpnext 16.50.0,
    india_compliance 16.10.0 (`bench list-apps`, 2026-10-09); scheduler enabled. Stack: `infra/erp.sh`.
  - ✅ Trademark policy read (`docs/phase-0-log.md` §5).
  - ✅ Sample retail company `Demo Kirana Store` (DKS), GSTIN `29AAPFD1234K1Z7` (Karnataka), FY 2026-2027, audit trail on,
    telemetry off; 8 item GST templates incl. 40%; 7 items, 1 supplier, `Walk-in Customer` — 2026-10-13,
    `docs/worklog/2026-10-09__phase0__sample-retail-company/02-done.md`.
  - ⬜ GST invoice + GSTR-1/3B + P&L/balance sheet check.
  - ⏸️ Handwriting spike → `docs/backlog.md` (ruled 2026-10-09; gates Phase 4 only).
- **Phase 0 exit:** base runs ✅; GST/audit reports confirmed ⬜.
- **Workflow rulings 2026-10-09:** two lanes (code/config) · API checks now, browser checks from Phase 1 ·
  no feature toggles until real shops · branch + PR off `master`, hooks deny push-master/force/vendor edits, ask on commit.
- **Repo:** `master` = `origin/master` @ `de77b88`. Branch `setup/phase-0-workflow` @ `1db8a94` (docs fixes, `infra/`,
  `.claude/` workflow, `docs/worklog/`) pushed to origin, not merged into `master`. `gh` CLI not installed.
- **Branch:** item work on `phase0/sample-retail-company` (cut from `setup/phase-0-workflow`, uncommitted).
- **Stack:** `merchant-erp-*` containers do not auto-restart; restarted 2026-10-12 with `docker compose -p merchant-erp -f infra/compose.local.yaml start`. `qa/checks/` does not exist yet.

## In progress
| Task | Lane | Session | Phase | Folder | Date |
|---|---|---|---|---|---|
| — | | | | | |

## Owed gates (human)
| Gate | Who | Since | Folder / note |
|---|---|---|---|
| Choose the product name (constraints: `docs/phase-0-log.md` §5) | maintainer | 2026-10-09 | — |
| Line up 2–3 friendly merchants + 1 CA for validation | maintainer | 2026-10-09 | `docs/phased-plan.md` §6.4 |
| CA confirms sample HSN codes + GST rates (GST 2.0) | CA (via maintainer) | 2026-10-13 | `…sample-retail-company/01-plan.md` §2 items table |

## Current menu
_Surveyed 2026-10-09 (session `phase0`); sample company line removed (done 2026-10-13)._
- **Merge `setup/phase-0-workflow` into `master` by PR** · config · S · buys: `master` carries `infra/`, `.claude/` skills and `docs/worklog/`, so item branches cut from `master` have them · blocked by: nothing (PR opened on GitHub web; `gh` not installed)
- **Acceptance-check harness `qa/checks/run.py`** (login over REST, PASS/FAIL/SKIPPED, stdlib only) · code · S · buys: layer B from `docs/ai-workflow.md` §3 exists, so config items can be checked over the API · blocked by: nothing
- **GST Sales Invoice + GSTR-1 / GSTR-3B + P&L / Balance Sheet check** · code · M · buys: Phase 0 checklist #3 → Phase 0 exit · blocked by: nothing
- **Product-name shortlist with domain + IP India availability** · config · S · buys: candidates for the owed name gate · blocked by: nothing
- **Phase 1 custom Frappe app scaffold** (`bench new-app`, installed on `merchant.localhost`) · code · M · buys: the app every Phase 1–6 feature lives in · blocked by: product name not chosen (app name); Phase 0 not exited
- **Handwriting accuracy spike** (`docs/backlog.md`) · code · M · buys: Phase 4 go/no-go · blocked by: no photos of real handwritten lists; no populated catalog
