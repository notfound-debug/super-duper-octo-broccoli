# AI Collaboration Workflow — Merchant Billing & Inventory

> **Point any AI session at this file.** It encodes how the maintainer wants work done on this repo:
> the per-item loop, the verification layers, the invariants, and the project facts an agent needs so
> it doesn't relearn them every session. Read it fully before changing anything. If something here
> conflicts with a newer instruction from the maintainer, the maintainer wins — then update this doc.

Adapted 2026-10-09 from the maintainer's `remote` repo workflow (`/next` → `/research` → `/build` →
`/verify`). Rulings made when adapting (2026-10-09): **two lanes** (§2) · **API checks now, browser
checks from Phase 1** (§3) · **no feature toggles until real shops** (§1.7) · **branch + PR, hooks as in
`remote`** (§6).

---

## 0. What this project is (one paragraph)

Offline-first billing + inventory software for small Indian retail shops, running on the shop's own
laptop. Built **on top of ERPNext + India Compliance** (GST, accounting, stock — reused, never rebuilt);
we build only the differentiators: our UI/brand, barcode scanning with teach-once, phone-as-scanner over
LAN, handwriting → inventory, and Tally export. Strategy: **Path A ("feed Tally")** now, Path B later.
Canonical docs: §8.

---

## 1. The non-negotiable invariants (never break these)

1. **Never edit `vendor/`.** Frappe, ERPNext, India Compliance and frappe_docker are reference only.
   Build in our app via the extension ladder (`docs/dev-boundaries.md` §2). A hook denies Edit/Write
   under `vendor/` — do not work around it; if you think you must, it is a decision for the maintainer.
2. **AI suggests, a human confirms.** No AI output writes to stock, money or the catalog without the
   merchant's explicit confirmation, and matching is **closed-set** against the merchant's own catalog —
   there is no free-text → new-item path (`docs/architecture.md` §7.2).
3. **Offline-first.** Core operations (billing, stock, scanning, export) work with no internet. Any
   online lookup (e.g. Open Food Facts) is optional and has an offline fallback.
4. **The handwriting pipeline is a separate program** called over HTTP. It is never imported into the
   Frappe app (keeps our IP outside the GPL work — `docs/architecture.md` §7.3).
5. **No "ERPNext" or "Frappe" in our product, company, domain or logo**, nor in ads. "Built on ERPNext"
   as description is fine (`docs/phase-0-log.md` §5).
6. **No secret in the repo, a log, or an evidence file.** Passwords live in `infra/.env.local`
   (gitignored); generated files that embed them (`infra/compose.local.yaml`) are gitignored too.
7. **Money and tax are exact.** Checks compare amounts in paise / exact decimals, never "approximately".
   *(Feature toggles: ruled not needed until real merchants use the product — revisit at Phase 6.)*
8. **Match the codebase.** Same comment density, naming and idioms as the surrounding code. Existing
   tests stay green. Code is written under the **`ponytail`** skill (minimum code that works).

---

## 2. The per-item loop and its two lanes

`/next` (menu) → `/research` (find out, write the plan + tests) → 🛑 your go → `/build` → `/verify`.
The research document is the **only** spec `/build` and `/verify` read; its tests are approved
**before** any code exists and `/build` may not touch them — independence comes from that ordering.

`/next` assigns each picked item a **lane**; the maintainer can overrule it.

| Lane | When | What happens |
|---|---|---|
| **code** | Anything that adds or changes code (our app, scripts, the handwriting service, infra scripts) | Full loop: `/research` writes `01-research.md` (method log + five-section report) → go → `/build` writes `02-build.md` → review → `/verify` writes `03-verify.md` |
| **config** | No code: data and settings in ERPNext (company, GST settings, items, parties, print formats), installs, docs-only edits | `/research` writes a short `01-plan.md` (what changes, the checks) → go → `/build` does it **and runs the checks** in the same run, writes `02-done.md`, and the item closes. No separate `/verify`. |

A config item that turns out to need code is **re-laned to code** and goes back to `/research` — as a
decision, never quietly.

### 2.1 The handoff card (tops every phase document)

1. **Summary** — at most five lines: what changed, what was proved, what is not done, what you must decide.
2. **Claims table** — `| Claim | Evidence pointer | Status |`, status ∈ **proved** · **partial** ·
   **not done** · **owed (human)**. Evidence = a test name, a check name, `file:line`, or a `command → output`.
   **No pointer ⇒ the status cannot be "proved".**
3. **Tests skipped** — count and reason, or "none".
4. **Not done** — planned items not delivered, each with why.
5. **Decisions needed** — numbered, each in the §2.2 shape.
6. **If you say go** — exactly what happens next.

The chat message at each 🛑 stop is the skill's own summary, said the way a plumber reports — plain
words, no jargon the maintainer did not use first.

### 2.2 How a decision reaches the maintainer

**What counts as a decision:** a blocker · a bug found mid-flight · a red test · a design fork · a cost
not agreed (a dependency, a scope change, a download, spend, time) · anything you are **not confident**
about · anything where two readings of an approved document produce different work. A question the code
or docs could answer is homework — do it instead of asking.

Each decision is numbered and has three parts, in this order:

1. **The issue.** What is true, in two or three sentences, with the evidence pointer. What it costs or
   breaks **for a merchant or for the product**. Why it is the maintainer's call.
2. **The options.** Every real one, including doing nothing, amending the plan instead of the code, and
   accepting the defect. **Equal depth** for each; **facts, not steering** (what it does, effort, what is
   gained, what is given up, what it breaks); no straw men, no bundling; **unmeasured means unmeasured**;
   no cost in the recommendation that is not already in the option.
3. **The recommendation.** Exactly one, after the options. The reason in terms of the facts, what would
   change your mind, how close the call is. Say so when confidence is low.

**After the ruling:** execute exactly what was ruled. Unanswered decisions stay open and are
re-presented. Record the ruling + date in the phase document.

---

## 3. Verification layers

| Layer | What | Where | Run |
|---|---|---|---|
| **A. Unit / integration** | Tests of our Frappe app (from Phase 1) | in our app, `test_*.py` (Frappe test runner) | `infra/erp.sh test` *(added with the app)* |
| **B. Acceptance checks** | The automated "does it actually work" check: talks to the **live site over its REST API** and gives a hard PASS/FAIL with the numbers printed (e.g. "Sales Invoice → CGST 9% + SGST 9%, grand total = ₹1,180.00") | `qa/checks/<name>.py` — Python **stdlib only**, exits non-zero on FAIL | `python qa/checks/run.py [name]` |
| **C. Browser checks** | Click through our screens like a shopkeeper | *from Phase 1 (ruled 2026-10-09); tool chosen then* | — |
| **Human gates** | Things only a person can judge: a CA accepts the Tally file, a merchant can bill unaided | STATE → **Owed gates** | — |

Test **cost** classes used in every test table: `none` · `needs-stack` (Docker up, site
`merchant.localhost` exists) · `needs-human (<who>)`.

**Green must mean "ran".** A check that cannot run (stack down, missing data) reports **SKIPPED with the
reason**, never PASS. A red test is **reported** to the maintainer (raw output, root-cause class,
options) — never self-fixed, never weakened; the fix runs only on their ruling.

---

## 4. Running the base system

- Stack: Docker Desktop + `vendor/frappe_docker`; helper `infra/erp.sh build | up | site | down | logs`
  (`infra/README.md`). Site `merchant.localhost` on <http://localhost:8080>, user `Administrator`,
  password in `infra/.env.local`.
- REST API: `http://localhost:8080/api/resource/<DocType>` and `/api/method/<dotted.path>`; log in with
  `POST /api/method/login`. This is also how a separate program (the handwriting service) talks to ERPNext.

---

## 5. Reporting & honesty

- Report outcomes faithfully. No win, a regression, or an inconclusive result is said plainly, with the
  numbers, and diagnosed.
- A claim of "works" names the check or test that proves it.

---

## 6. Git & commit conventions

- **Branch off `master`** for each item (`<session>/<task-slug>`); merge by pull request. Never commit
  straight to `master`.
- **Commit only when the maintainer asks.** **Push only when asked.**
- Commit message: clear subject + body with the change and its evidence; end with the current model's
  `Co-Authored-By` line (never hard-code a model name in the skills).
- **Surface uncommitted changes you didn't make** before committing; don't sweep them in.
- **Enforced by hooks** (`.claude/settings.json` → `.claude/hooks/guard.py`): push to `master` or any
  force-push → **deny**; `git commit` → **ask**; Edit/Write under `vendor/` → **deny**. If a hook fires
  wrongly, say so — don't work around it.

---

## 7. Project facts & gotchas

- **Windows + Git `core.autocrlf=true`:** shell scripts that run inside Linux containers must be LF.
  `vendor/frappe_docker` is cloned with `-c core.autocrlf=false`; our own `*.sh` are pinned LF by
  `.gitattributes`. Symptom of getting it wrong: `exec /usr/local/bin/entrypoint.sh: no such file or directory`.
- **Versions:** Frappe / ERPNext / India Compliance all `version-16` (`infra/apps.json`).
- **Python on the host:** 3.12, no `requests` installed — checks use `urllib` (stdlib).
- Tools present: git, Docker Desktop (WSL2, 8 GB to Docker), Python 3.12, Node, winget.

---

## 8. Canonical docs

- `docs/phased-plan.md` — phases, MVP scope, estimates. **Source of truth for sequencing.**
- `docs/architecture.md` — components, deployment, the no-hallucination pipeline.
- `docs/dev-boundaries.md` — the `vendor/` rule and the extension ladder.
- `docs/phase-0-log.md` — Phase 0 record (versions, trademark findings).
- `docs/backlog.md` — deferred items (e.g. the handwriting spike).
- `docs/worklog/STATE.md` — the live tracker (≤100 lines). **The only tracker file the skills read.**
  `docs/worklog/HISTORY.md` — append-only, one line per event.
- This file.

---

## 9. TL;DR for a new session

1. Read this doc + `docs/worklog/STATE.md`. Drive work with `/next` → `/research` → `/build` → `/verify`.
2. Never edit `vendor/`; extend ERPNext from our app; configure via data.
3. Every claim has a check; red is reported, not fixed silently.
4. Branch off master; commit and push only when asked.
