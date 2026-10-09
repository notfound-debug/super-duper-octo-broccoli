# Backlog — deferred and future work

> Items consciously moved out of their phase, with why and what they gate. `/next` reads this file.

| Item | Moved from | Ruled | Gates | Needs | Notes |
|---|---|---|---|---|---|
| **Handwriting accuracy spike** — run 2–3 real merchants' handwritten lists through PaddleOCR/docTR and a small VLM (Florence-2 / Phi-3.5-vision); measure line accuracy and closed-set catalog match rate | Phase 0 | 2026-10-09 | Phase 4 start (go/no-go) | Photos of real handwritten lists from the maintainer; a populated catalog to match against | Plan: `docs/phased-plan.md` Phase 4; method: `docs/architecture.md` §7 |
| **Browser checks** (verification layer C) | adopting the workflow | 2026-10-09 | Phase 1 screens | Tool choice (e.g. Playwright) — a dependency decision at that time | `docs/ai-workflow.md` §3 |
| **Feature toggles** for our app | adopting the workflow | 2026-10-09 | Phase 6 (real merchants) | — | `docs/ai-workflow.md` §1.7 |
