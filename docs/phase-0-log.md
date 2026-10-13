# Phase 0 Log — Foundation & Validation

> Running record of Phase 0 work: what was done, what was found, what's still open.
> Plan: [`phased-plan.md` §2 Phase 0](./phased-plan.md) · Started: 2026-10-09

Decision recorded: **Path A ("feed Tally")** — confirmed 2026-10-09.

---

## Checklist

| # | Task | Status |
|---|------|--------|
| 1 | Install ERPNext + India Compliance on the laptop | ✅ done 2026-10-09 — frappe 16.51.0, erpnext 16.50.0, india_compliance 16.10.0 (see [`infra/`](../infra/README.md)) |
| 2 | Configure sample Indian retail company (GST, HSN, tax slabs, products, supplier, customer) | ✅ done 2026-10-13 — `Demo Kirana Store` (see [`worklog`](./worklog/2026-10-09__phase0__sample-retail-company/02-done.md)); HSN/rates owed a CA check |
| 3 | GST invoice + GSTR-1/3B + P&L/balance sheet → confirm audit-readiness | ⬜ |
| 4 | Handwriting spike: 2–3 real merchants' sheets through OCR/VLM → go/no-go | ⏸️ **backlog** (2026-10-09) — run any time before Phase 4 |
| 5 | Read Frappe trademark policy; pick product name | 🟡 policy read (below); name not yet chosen |

---

## 1. Base install

- **Versions:** Frappe `version-16`, ERPNext `version-16`, India Compliance `version-16`
  (both upstreams have a `version-16` branch as of 2026-10-09).
- **Method:** Docker Desktop (WSL2) + official `frappe_docker`, custom image `merchant-erp:16`
  built from [`infra/apps.json`](../infra/apps.json). Helper: `infra/erp.sh`.
- **Site:** `merchant.localhost`, served on <http://localhost:8080>.
- **Gotcha hit:** Git's `core.autocrlf=true` turned frappe_docker's shell scripts into CRLF →
  containers crash-looped with `exec /usr/local/bin/entrypoint.sh: no such file or directory`.
  Fix: clone frappe_docker with `-c core.autocrlf=false` and rebuild (now in `infra/README.md`).

## 5. Trademark policy — findings

Source: [`frappe/erpnext` TRADEMARK_POLICY.md](https://github.com/frappe/erpnext/blob/develop/TRADEMARK_POLICY.md)
(read 2026-10-09). Matches what `architecture.md` §4 and `dev-boundaries.md` §5 already assume.

- "ERPNext" name + logo are trademarks of Frappe Technologies Pvt. Ltd.
- 🚫 Not in our **product, project, service, domain or company name** (commercial use gets no permission).
- 🚫 Not in our **logo/branding**, and nothing that suggests affiliation with or endorsement by Frappe.
- 🚫 Not in **advertising, including AdSense/AdWords**.
- ✅ Allowed: using the name to **describe** what we do — e.g. "built on ERPNext" — and the ERPNext
  logo on a page that describes our product (not as our logo).
- The policy explicitly encourages commercial ERPNext-based businesses.

**Product-name constraints:** no "ERPNext", "Frappe", or anything confusingly similar
(e.g. "ERP-Next", "NextERP"). Check domain + Indian trademark registry (IP India) availability
before committing.
