# Phased Delivery Plan — Merchant Billing & Inventory Product

> How we build the product in stages, what ships when, effort estimates, and the
> Path A → Path B business strategy.

Status: **Draft v1** · Last updated: 2026-10-09
Companion docs: [`architecture.md`](./architecture.md) · [`dev-boundaries.md`](./dev-boundaries.md)

---

## 0. Strategy in one picture

```
Path A ("feed Tally")  ─────────────►  Path B ("replace Tally")
Own daily operations.                  Become the whole system.
Export clean data to Tally             Flip on ERPNext's full
so the CA is happy →                   accounting/GST/audit that's
switching cost ≈ 0.                    already underneath.
```

> **Decided (2026-10-09): we go with Path A.** Phase 0 is under way.

- **Sell on Path A** (easy pitch: better daily experience + scanning + handwriting magic + real support).
- **Architect for Path B** (the base already has full accounting/GST/audit — switch it on once merchants
  trust us and CAs come around).

---

## 1. Guardrails (apply to every phase)

- **Offline-first**, on-premise on the shop laptop.
- **No hallucination**: AI output is always constrained + human-confirmed before writing to inventory/money.
- **Reuse the engine** (ERPNext + India Compliance), **build only differentiators**.
- **Protect IP**: handwriting pipeline is a separate private API service.
- **Validate with real merchants** at each phase before scaling.

---

## 2. Phase-by-phase roadmap

### Phase 0 — Foundation & validation *(≈ 1–2 weeks)*
**Goal:** stand up the base and de-risk the hardest unknown early.
- [ ] Install ERPNext + India Compliance on a laptop; configure a sample Indian retail company
      (GST, HSN, tax slabs, a few products, a supplier, a customer).
- [ ] Produce a GST invoice + view GSTR-1/3B report + P&L/balance sheet → confirm audit-readiness.
- [ ] **Spike the risk:** run 2–3 *real* merchants' handwritten sheets through PaddleOCR/docTR and a
      small VLM (Florence-2/Phi-3.5) to calibrate real accuracy. **Decision gate:** is confirm-first
      recognition good enough to be useful? (It usually is, because the human confirms.)
- [ ] Read Frappe trademark policy; pick a product name.

> **Backlogged (2026-10-09):** the handwriting spike is moved out of Phase 0. It can run any time
> before Phase 4 starts (it only gates Phase 4, not the MVP).

**Exit:** base runs; GST/audit reports confirmed. *(Handwriting go/no-go deferred — see above.)*

---

### Phase 1 — Rebrand + core billing UX *(≈ 2–3 weeks)*
**Goal:** a merchant can bill and manage stock in *our* branded, simple interface.
- [ ] Custom Frappe app scaffold (installed alongside base).
- [ ] Rebrand: our logo + product name in UI; keep GPL license headers in code.
- [ ] Simplify the counter-billing screen for a non-accountant shopkeeper.
- [ ] Basic product/inventory management screens.

**Exit:** looks like our product, not raw ERPNext; daily billing is pleasant.

---

### Phase 2 — Barcode scanning + teach-once *(≈ 2 weeks)*
**Goal:** scan existing manufacturer barcodes for stock-in and billing.
- [ ] Integrate html5-qrcode (browser) / ZXing-C++ (desktop) for EAN/UPC.
- [ ] Barcode → Open Food Facts lookup.
- [ ] **Teach-once cache:** unknown barcode → prompt name once → save to local catalog forever.
- [ ] Wire scan → billing line and scan → stock-in.

**Exit:** merchant scans at counter and at goods-inward; unknown items self-populate over time.

---

### Phase 3 — Phone-as-scanner LAN sync *(≈ 1–2 weeks)*
**Goal:** use a phone as a scanner when there's no USB hardware.
- [ ] Local WebSocket server in the custom app.
- [ ] Phone PWA (getUserMedia + html5-qrcode) with QR pairing to the laptop.
- [ ] Push scanned codes / captured photos to the laptop over LAN.
- [ ] Fallback documented: hid-barcode-scanner (Bluetooth HID).

**Exit:** any phone becomes a scanner over shop WiFi, no install, no cloud.

---

### Phase 4 — Handwriting → inventory (the differentiator) *(≈ 4–8 weeks)*
**Goal:** photograph a handwritten list → draft entries → merchant confirms → inventory updates.
- [ ] Separate handwriting **API service** (keeps IP private): OCR/VLM extraction.
- [ ] **Constrained matching** to the merchant's own catalog via RapidFuzz (never invent items).
- [ ] Confidence thresholds (high pre-fill / low flag / none = pick-or-create).
- [ ] **Mandatory confirmation UI**: photo crop | parsed line | matched product | qty/price.
- [ ] **Abbreviation learning**: every correction saves a per-merchant alias for instant future hits.
- [ ] Works for **both purchase and sale** lists.

**Exit:** the "wow" feature works safely; nothing writes without a human tap; it improves per shop.

> This is the long pole and the biggest differentiator. Do it *after* the catalog exists (Phases 1–2),
> because matching needs a populated catalog to match against.

---

### Phase 5 — Tally export (Path A bridge) *(≈ 1–2 weeks)*
**Goal:** hand the CA data they already accept → near-zero switching cost.
- [ ] Confirm exact format/fields CAs accept (Tally XML import route).
- [ ] Export sales/purchases/ledgers from ERPNext → Tally-import file.
- [ ] Validate with a real CA.

**Exit:** merchant keeps their CA + Tally; we own their daily operations. Path A complete.

---

### Phase 6 — Safety, backup, packaging *(≈ 2–3 weeks)*
**Goal:** production-ready for real shops.
- [ ] Local/USB backup baseline; optional paid cloud backup endpoint.
- [ ] License/activation + update server (minimal, on our side).
- [ ] One-click installer for the shop laptop.
- [ ] Onboarding flow + basic support tooling (the pain point that started this).

**Exit:** a merchant can be onboarded and safely run the product daily.

---

### Later — Path B (replace Tally) *(post-traction)*
- Generate CA-acceptable audit/GST reports directly from ERPNext.
- Win over CAs; flip merchants off Tally onto our full accounting engine (already underneath).

---

## 3. MVP definition (what ships first to real merchants)

**MVP = Phase 0 + 1 + 2 + 3 + 5** (billing, inventory, barcode scanning, phone-scanner, Tally export).
The **handwriting feature (Phase 4)** is the headline differentiator but is the long pole — ship the
MVP without it, then add it as the "wow" upgrade. This gets a usable, sellable product out fastest and
validates demand before the biggest build.

---

## 4. Rough effort estimate (solo developer)

| Phase | Effort |
|-------|--------|
| 0 Foundation & validation | 1–2 weeks |
| 1 Rebrand + billing UX | 2–3 weeks |
| 2 Barcode + teach-once | 2 weeks |
| 3 Phone-as-scanner | 1–2 weeks |
| 5 Tally export | 1–2 weeks |
| **→ MVP subtotal** | **~7–11 weeks (~2–3 months)** |
| 4 Handwriting pipeline | 4–8 weeks |
| 6 Safety/backup/packaging | 2–3 weeks |
| **→ Full v1** | **~4–5 months** |

> Standing on ERPNext + India Compliance saves the ~6–12 months (plus permanent GST-law upkeep) it
> would take to build accounting/GST/audit from scratch. That saving is the whole reason for the
> adopt-and-adjust approach.

---

## 5. Key risks & mitigations

| Risk | Mitigation |
|------|------------|
| Handwriting accuracy on messy notes | Spike before Phase 4 (backlogged from Phase 0); confirm-first design makes it usable even at mediocre accuracy; alias learning improves it per shop. |
| CA won't accept our data (Path A) | Validate Tally export with a real CA early (Phase 5). |
| GST rules change | India Compliance community maintains this for free — track their releases. |
| GPL obligations on-premise | Keep handwriting as a separate private API service; provide GPL base source only if asked (merchants rarely ask). |
| Scope creep before revenue | Ship the MVP (no Phase 4) first; add the differentiator after demand is proven. |

---

## 6. Immediate next actions

1. ~~Create the project repo~~ — done: `super-duper-octo-broccoli/` (this repo).
2. Execute **Phase 0**: install ERPNext + India Compliance; run the handwriting accuracy spike.
3. Decide product name (after reading Frappe trademark policy).
4. Line up 2–3 friendly merchants + 1 CA for validation feedback.
