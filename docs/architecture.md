# Architecture — Merchant Billing & Inventory Product

> Offline-first billing + inventory + accounting for small Indian retail merchants,
> with a phone-camera scanner and handwritten-list capture.
> **Adopt-and-adjust**: reuse mature open source for the hard parts, build only the differentiators.

Status: **Draft v1** · Last updated: 2026-10-09

> Phase numbers in this doc follow [`phased-plan.md`](./phased-plan.md), which is the source of truth for sequencing.

---

## 1. Product vision

Small Indian retail merchants currently juggle two kinds of software:

- **Daily operations** (billing, stock-in/out, scanning) — Vyapar / Marg / paper.
- **Accounting & compliance** (GST returns, ledgers, year-end audit) — **Tally** (because their CA demands it).

Both have poor customer support, and neither handles the messy real world (supplier handwritten
purchase lists, quick barcode stock-in, phone-as-scanner). **Our product owns the daily-operations
layer with a delightful, low-friction experience, while staying GST- and audit-compliant underneath.**

**Strategy:** start on **Path A ("feed Tally")** — be the operations + scanning layer and export
clean data the CA accepts — while architecting for **Path B ("replace Tally")**, since the chosen
base already contains a full accounting/GST/audit engine we can switch on later.

---

## 2. Guiding principles

1. **Reuse the engine, own the differentiators.** Don't rebuild accounting/GST — inherit it.
2. **Offline-first.** Everything core runs on the shop's laptop over local WiFi, no internet required.
3. **No hallucination, ever.** Any AI output is *constrained* and *human-confirmed* before it touches
   inventory or money.
4. **Protect the secret sauce.** Keep our real IP (handwriting pipeline) as a **separate service**
   with a clean API, so it stays private even when the GPL base is distributed.
5. **Permissive where possible; copyleft only where it saves the most.**

---

## 3. Component / pillar map

| # | Pillar | Chosen tech | License | Build vs Reuse |
|---|--------|-------------|---------|----------------|
| 1 | Base billing/inventory/accounting/GST | **ERPNext + India Compliance** | GPLv3 | **Reuse** (configure + custom app on top) |
| 2 | Barcode scanning (EAN/UPC) | **ZXing-C++** (native) + **html5-qrcode** (browser) | Apache-2.0 | **Reuse** libs; build teach-once cache |
| 2b | Barcode → product DB | **Open Food Facts** + local teach-once cache | ODbL (data) | **Reuse** + custom cache |
| 3 | Handwriting → inventory | **PaddleOCR / docTR** or **Florence-2 / Phi-3.5-vision** VLM + **RapidFuzz** | Apache-2.0 / MIT | **Build** the pipeline (reuse the models) |
| 4 | Phone-as-scanner LAN sync | **html5-qrcode** PWA + **WebSocket (ws)** | Apache-2.0 / MIT | **Build** the glue (reuse libs) |
| 5 | App shell / UI | Frappe UI (from ERPNext) + custom Frappe app | MIT/GPL mix | **Build** our UI/app |

---

## 4. Base system: ERPNext + India Compliance (DECIDED) — Phases 0–1

**What we get for free (why we chose it):**

- GST-compliant invoicing with **HSN/SAC**, CGST/SGST/IGST, multiple tax slabs.
- **GSTR-1 / GSTR-3B / GSTR-2A-2B** reports and reconciliation (via India Compliance add-on).
- **e-invoicing (IRN + QR)** and **e-way bill** generation.
- Inventory: purchases + sales, stock adjustments, **batch/expiry**.
- Party/customer/supplier ledgers, **AR/AP**.
- Full **double-entry accounting**: P&L, balance sheet, financial-year close, **audit-ready reports**.
- Multi-user, roles/permissions.

**Stack:** Frappe Framework (Python + MariaDB + JS). Runs on a laptop/mini-PC (on-premise).

**How we extend it:** our features live in a **custom Frappe app** installed alongside ERPNext +
India Compliance, so upgrades to the base don't break our code.

### Licensing rules for the base (GPLv3) — the contract we operate under

| | Rule |
|---|---|
| ✅ CAN | Sell it / charge subscriptions. No license fee to anyone. |
| ✅ CAN | Modify code freely; put **our own logo + product name** in the UI. |
| ✅ CAN | Install on each merchant's laptop (on-premise) and run offline. |
| ✅ CAN | Build our custom features as our own app — that part **we own**. |
| 🚫 CANNOT | Close-source the ERPNext/India-Compliance parts or relicense them. |
| 🚫 CANNOT | Strip the copyright/license headers **inside** the source files. |
| 🚫 CANNOT | Use their **trademark** ("ERPNext"/Frappe logo) as our own or claim we wrote it. |
| 📌 MUST | Keep the GPL parts under GPLv3; offer their source to any merchant we distribute to (they rarely ask). |
| 📌 MUST | Keep license headers; add our own copyright alongside for our changes. |

> **Trademark vs copyright:** GPL (copyright) lets us change and rebrand the code. Trademark is
> separate — we must **strip their name/logo** and ship under our brand. "Built on ERPNext" is honest
> attribution and allowed; "is ERPNext" is not.

> **Cost note:** the only thing that can cost money is the optional **e-invoice/e-way-bill GSP API
> gateway** (a govt-connectivity service, not the software license). We can use our own GSP or free
> tier. The software itself is free.

---

## 5. Barcode scanning of existing manufacturer barcodes — Phase 2

- **Scanning:** `html5-qrcode` (Apache-2.0) decodes EAN-13/UPC in the browser via `getUserMedia`
  (used by the phone PWA); `ZXing-C++` (Apache-2.0) for any native/desktop decoding.
  *(Google ML Kit is NOT open source — excluded.)*
- **Product lookup:** `Open Food Facts` (ODbL) free barcode→product API.
  - **Honest gap:** food-centric and India-sparse; most regional/non-food Indian SKUs will miss.
  - **Fallback — teach-once:** on unknown barcode, prompt the merchant to name the product **once**,
    cache it in the **local catalog forever**. After a few weeks each shop has a complete local DB and
    no internet dependency. (Our custom code; also a privacy/offline win.)

---

## 6. Phone-as-scanner syncing to laptop — Phase 3

- **Top approach (simplest robust):** laptop runs a local web server; phone opens a URL / scans a
  pairing QR → **PWA using `getUserMedia` + html5-qrcode** decodes on the phone → result pushed to the
  laptop over **local WiFi via WebSocket** (`ws`, MIT). No cloud, no app-store install.
- **Fallback:** `hid-barcode-scanner` (FOSS Android) turns a phone into a **Bluetooth HID keyboard** —
  scanned code is "typed" into the focused field. Zero integration code.
- **Avoid for now:** WebRTC-via-QR peer connection (FOSS examples are immature/WIP).

---

## 7. Handwriting → inventory (the differentiator) — Phase 4

**Goal:** photograph a supplier's handwritten purchase/sale list → draft stock entries → merchant
confirms. **On-device, offline, zero hallucination.**

### 7.1 Models (all commercial-safe licenses)

- **Extraction (pick one):**
  - Traditional OCR: **PaddleOCR** / **docTR** (Apache-2.0) — good on semi-neat handwriting.
  - Small VLM (better on messy handwriting): **Florence-2** / **Phi-3.5-vision** (MIT), or
    **Moondream2** / **SmolVLM** (Apache-2.0).
  - ⚠️ **Avoid** Qwen2.5-VL 3B (Qwen license) and MiniCPM-V (custom scale-restricted license) — not
    cleanly commercial.
- **Matching:** **RapidFuzz** (MIT).

> **Code license ≠ model-weight license.** The models above are chosen because *both* are permissive.

### 7.2 The no-hallucination pipeline (why it's structurally safe)

```
photo
  │
  ▼
[1] Extract raw tokens (VLM/OCR)   ← output treated as UNTRUSTED noise
  │
  ▼
[2] Constrained match to the MERCHANT'S OWN catalog only  ← cannot invent items
  │      (RapidFuzz fuzzy match; candidate set is CLOSED)
  ▼
[3] Confidence thresholds  → high = pre-filled · low = flagged · none = "unknown, pick/create"
  │
  ▼
[4] MANDATORY human-confirmation screen   ← nothing writes to inventory until merchant taps confirm
  │      (photo crop | parsed line | matched product | qty/price)
  ▼
[5] Learn abbreviation → product mapping per merchant   ← next time it's an instant exact hit
```

**Why hallucination is impossible:** there is **no "free text → new item" path**. The system can only
*point at* items that already exist in the catalog. Even mediocre recognition is *usable* because the
merchant always confirms, and the alias table sharpens accuracy per shop over time.

### 7.3 IP protection

The handwriting pipeline is deployed as a **separate service with a clean API** (a distinct program
the Frappe app merely *calls*). A separate program is **not** part of the GPL work, so this — our real
IP — **stays private even when the base is installed on a merchant's machine.**

---

## 8. Deployment model (on-premise, offline-first)

```
┌──────────────────────────────────────────────────────────────┐
│  SHOP LAPTOP / MINI-PC  (runs offline on shop WiFi)            │
│                                                                │
│  ERPNext + India Compliance      ← REUSE (GST, accounting,     │
│  (Frappe: Python / MariaDB)         inventory, audit)          │
│        ▲  REST API                                             │
│  ┌─────┴──────────────────────────────────┐                   │
│  │ OUR custom Frappe app        ← BUILD    │                   │
│  │  • barcode teach-once cache             │                   │
│  │  • phone-sync WebSocket server          │                   │
│  │  • confirmation UI / rebrand            │                   │
│  └─────┬──────────────────────────────────┘                   │
│        │ local API call                                        │
│  ┌─────▼──────────────────────────────────┐                   │
│  │ Handwriting service  ← BUILD (separate, │  keeps IP private │
│  │ private API): OCR/VLM + RapidFuzz match │                   │
│  └────────────────────────────────────────┘                   │
└───────────────────────▲────────────────────────────────────────┘
                        │ LAN (WebSocket) — no cloud
              ┌─────────┴───────────┐
              │  PHONE (PWA)  ← REUSE html5-qrcode │
              │  • scan EAN/UPC barcodes           │
              │  • capture handwritten-list photos │
              └────────────────────────────────────┘

Optional: nightly backup → USB drive (offline) or paid cloud endpoint (upsell).
```

- **What we host from our end:** almost nothing — only optional license/activation, an update server,
  and (if sold) a cloud-backup endpoint. Each merchant's app + data lives on *their* machine.
- **Backup:** not required for operation. Offer USB/local backup as baseline; optional cloud backup as
  a paid add-on (data-safety, not a dependency).

---

## 9. Reuse vs custom-build — the honest split

**Reuse (don't build):**
- ERPNext + India Compliance — the entire GST/accounting/audit/inventory core.
- html5-qrcode + ZXing-C++ — scanning.
- Open Food Facts — initial barcode lookups.
- PaddleOCR/docTR or Florence-2/Phi-3.5 — handwriting extraction models.
- RapidFuzz — matching.
- ws / WebRTC — transport.

**Must build (our product / IP):**
1. **Handwriting → catalog-match → confirm → learn** pipeline (biggest effort, biggest differentiator).
2. **Phone-sync glue** (LAN WebSocket + QR pairing) — small.
3. **Barcode teach-once cache** — small.
4. **Merchant-friendly UI skin** + rebrand over ERPNext.
5. **Tally export** (Path A) — clean data the CA accepts.

---

## 10. Open questions / risks

- **Handwriting accuracy (Phase 4) is unproven** until we prototype on *real* merchant handwriting
  (the Phase 0 spike). The confirm-first
  design makes even mediocre recognition usable, but validate before promising anything.
- **Tally-acceptance (Path A):** confirm the exact export format/fields CAs will accept.
- **GST law upkeep:** handled by the India Compliance community — monitor their releases.
- **Trademark policy:** read Frappe's before finalizing product name and marketing copy.

---

## 11. Related docs

- [`phased-plan.md`](./phased-plan.md) — delivery roadmap, MVP scope, effort estimates, Path A→B.
- [`dev-boundaries.md`](./dev-boundaries.md) — what not to touch: extend ERPNext via Frappe hooks, never edit `vendor/`.
