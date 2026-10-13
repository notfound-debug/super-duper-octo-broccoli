# Developer Boundaries — What Not to Touch

> The one rule that keeps this project upgradeable and license-clean.
> Read this before writing code against ERPNext. If you're unsure, this doc decides.

Status: **v1** · Last updated: 2026-10-09
Companion docs: [`architecture.md`](./architecture.md) · [`phased-plan.md`](./phased-plan.md)

---

## 0. The one rule

**Do not edit anything inside `vendor/erpnext/`, `vendor/india-compliance/`, or `vendor/frappe/`.
Build every feature in our own app instead, using the extension points below.**

If you follow this rule, two good things happen automatically:

1. **Upgrades stay free.** ERPNext and India Compliance ship updates (including GST law
   changes we depend on). If we never edit their files, `bench update` just works. Every
   file we edit in their tree becomes a merge conflict we own **forever** — and free GST
   upkeep was the whole reason we chose this base.
2. **The license stays simple.** We never have to reason about modification notices,
   header preservation, or derivative-work rules, because we didn't modify their code.

> This is an **engineering** rule first. We open-source our own app under GPLv3, so editing
> their code is *legally* allowed — but it's a maintenance trap. The boundary exists to
> protect upgrades, not to satisfy a lawyer.

---

## 1. Where our code lives

```
super-duper-octo-broccoli/        (this repo)
├── vendor/                      ← REFERENCE ONLY. Never edit. Gitignored.
│   ├── frappe/                  (MIT)     the framework
│   ├── erpnext/                 (GPLv3)   billing/inventory/accounting/GST
│   └── india-compliance/        (GPLv3)   GST returns, e-invoice, e-way bill
│
└── (our custom Frappe app)      ← ALL our work goes here
    handwriting-service/         ← separate program (its own process + repo)
```

Everything we build lives in **our custom app** (a normal Frappe app installed alongside
the base) or in the **separate handwriting service**. Nothing we write goes into `vendor/`.

---

## 2. The extension ladder — always use the lowest rung that works

Frappe is designed to be extended without touching core. Prefer the top of this list;
only move down when the rung above genuinely can't do the job.

| Rung | Mechanism | Lives in | Use it for |
|---|---|---|---|
| 1 | **Custom Field / Property Setter / Customize Form** | database | Add a field (e.g. `barcode` on Item), change a label, hide a field, make something mandatory |
| 2 | **Client Script** | database | Change form behaviour in the browser (buttons, validations, auto-fill) |
| 3 | **Server Script** | database | Small server-side logic without deploying code |
| 4 | **`doc_events` (hooks.py)** | our app | Run our code on validate / before_save / on_submit of an ERPNext doctype |
| 5 | **`override_doctype_class` (hooks.py)** | our app | Replace an ERPNext controller with our subclass (`class OurSalesInvoice(SalesInvoice)`) |
| 6 | **`override_whitelisted_methods` (hooks.py)** | our app | Replace an ERPNext API endpoint with ours |
| 7 | **New DocTypes / Pages / Reports** | our app | Anything genuinely new (teach-once cache, phone-sync, confirmation UI) |
| — | ~~Edit `vendor/erpnext/*.py`~~ | their files | **Never. This is the boundary.** |

**Rungs 1–7 cover essentially everything in our roadmap.** Examples:

- Barcode field on Item → **Rung 1** (Custom Field).
- Teach-once: on unknown scan, create a catalog entry → **Rung 4** (`doc_events`) or **Rung 7** (new DocType for the cache).
- Custom billing logic on Sales Invoice → **Rung 5** (`override_doctype_class`).
- Phone-sync WebSocket server → **Rung 7** (new code in our app), or the separate service.
- Confirmation UI for handwriting → **Rung 7** (new Page/DocType) that calls the handwriting service over HTTP.

---

## 3. Verified: you can override without touching core

These are real Frappe mechanisms, confirmed in the vendored source:

- `override_doctype_class` is resolved in `frappe/model/base_document.py` — register
  `{"Sales Invoice": "our_app.overrides.CustomSalesInvoice"}` in our `hooks.py` and Frappe
  loads **our** class instead of ERPNext's, with ERPNext's file untouched.
- `doc_events`, `override_whitelisted_methods`, and `extend_bootinfo` are all declared as
  hooks in `frappe/hooks.py` and are available to any installed app.
- The entire REST API lives in `frappe/api/` (the **MIT** layer); ERPNext ships no REST
  layer of its own. Any separate program can read/write ERPNext data over
  `localhost/api/resource/...` — fully offline — without importing ERPNext.

So: **we never need to fork a core file to change behaviour.** If it feels like we do,
we've picked the wrong rung — ask before editing core.

---

## 4. Two things that are NOT modifications (do these freely)

- **Configuration / data.** Creating the company, chart of accounts, GST settings, HSN
  codes, tax slabs, items, customers, price lists — all of that is **data in the database**,
  not code. It never touches `vendor/` and is not a "modification" in any sense.
- **Custom Fields, Property Setters, Client/Server Scripts.** These are stored in the
  database too (rungs 1–3). They change behaviour without changing a single vendor file.

---

## 5. Trademark boundary (separate from code)

Copyright and trademark point in **opposite directions** — don't confuse them:

| Thing | Where it is | What to do |
|---|---|---|
| Copyright / license headers | inside source **files** (comments) | If we ever did edit a vendor file, keep them. Since we don't edit vendor files, N/A. |
| Trademark: "ERPNext" name, logo, splash | the **UI** (`app_title`, `app_logo_url`, `splash_image`, favicon) | When we ship under **our** brand, override these from **our app's** hooks + Website/Navbar Settings — **not** by editing `vendor/erpnext/hooks.py`. |

Rebranding is done by **overriding** brand settings from our side, never by editing their
files. Same boundary, applied to the logo.

Also: never use "ERPNext" in our **product / company / service / domain name**, or in
**advertising / AdWords**. Saying "built on ERPNext" as honest description is fine.

---

## 6. If you think you MUST edit a vendor file

Stop and ask first. The answer is almost always one of the rungs in §2. But if there is
genuinely no extension point (rare), then it is a **team decision**, and whoever approves it
accepts that:

- the change must be re-applied and re-tested on **every** future `bench update`, forever;
- it must be documented (what, where, why, date) so the next upgrade doesn't silently lose
  or clobber it;
- and legally (since we edit GPL code): keep their copyright + license headers, add ours
  alongside, and add a dated "modified by" note. But again — **avoid getting here.**

---

## 7. The boundary in one line

**Build in our app. Extend via hooks and overrides. Configure via the database.
Never edit `vendor/`. If you think you must, you've picked the wrong rung — ask.**
