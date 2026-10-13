---
date: 2026-10-13
session: phase0
task: Sample Indian retail company on merchant.localhost
lane: config
phase: done
status: done (12 green / 0 red / 0 skipped)
---

# Sample Indian retail company — done log

## Handoff card

**Summary.** All of plan §3 steps 1–7 are applied on `merchant.localhost`. All 12 checks C1–C12 are green
on the re-run of 2026-10-13. The first run had C7 red because of a formatting fault in the check (D1,
ruled (a)). The sample company is ready for item #3 (GST invoice + GSTR-1/3B). Still owed: a CA confirms
the HSN codes and GST rates.

| Claim | Evidence pointer | Status |
|---|---|---|
| Setup wizard completed with the plan's args | step 2 → `{"status": "ok"}`; C1 green | proved |
| System settings, company, fiscal year, address as planned | C2, C3, C4, C5 green | proved |
| GST accounts mapped for DKS | C6 green | proved |
| 8 item tax templates incl. `GST 40% - DKS` at 20/20/40 | step 3 output; C7 green (re-run) | proved |
| Sales/purchase templates + 4 tax categories | C8 green | proved |
| 7 items + 14 prices exact | C9 green | proved |
| Supplier and walk-in customer | C10, C11 green | proved |
| GST engine applies in-state template + item rates (plug-in point) | C12 green: CGST 10.90, SGST 10.90, grand 231.80, rounded 232.00, 0 invoices saved | proved |
| HSN codes and per-item GST rates are legally right | — | owed (human: CA) |

**Tests skipped.** None.
**Not done.** Nothing planned is left. By design: no opening stock, no B2B customer, no saved invoice (item #3).
**Decisions needed.** None open. D1 ruled (a) on 2026-10-13.
**If you say go.** Nothing more for this item. The loop returns to `/next`.

## Checklist (plan §2 "What we set")

| Line | Status | Read back from the site |
|---|---|---|
| Wizard: language/country/timezone/currency | done | C2: `India`, `Asia/Kolkata`, `INR` |
| enable_telemetry `1 → 0` | done | C2: `0` |
| Company `Demo Kirana Store` / `DKS`, India chart, GSTIN, PAN, rate 18 | done | C3 |
| Fiscal Year `2026-2027` | done | C4: `2026-04-01` … `2027-03-31` |
| enable_audit_trail `1` | done | C3: Accounts Settings `enable_audit_trail 1` |
| Item Tax Template `GST 40% - DKS` | done | step 3: Output CGST/SGST `20.0`, IGST `40.0`; RCM `-20/-20/-40`; Refund `-20/-20/-40`; Input `20/20/40`, RCM `20/20/40` |
| Address `Demo Kirana Store-Billing` | done | step 4: `gst_state=Karnataka gst_state_number=29` |
| Supplier `Sample Wholesale Distributors Pvt Ltd` + Address | done | step 5: `gstin=29AACCS5678M1ZJ pan=AACCS5678M`; address `gst_state_number=29` |
| Customer `Walk-in Customer` | done | step 6: `gst_category=Unregistered` |
| 7 Items + 14 Item Prices | done | step 7 (all 7 lines), C9 |

## Execution log (`command → output`)

The scripts are throwaways in the session scratchpad (`build.py`, `checks.py`). Nothing was added to the repo.
The password was read from `infra/.env.local` and never printed.

- Branch: `git checkout -b phase0/sample-retail-company` (from `setup/phase-0-workflow`, see Deviations).
- Telemetry pre-check: Frappe telemetry sends nothing unless `pulse_api_key` is set
  (`frappe/utils/telemetry/pulse/client.py:14`). `grep -c pulse_api_key` on common + site config → `0` / `0`.
- `python -I build.py <env>`: first two runs died on the Windows console encoding (`UnicodeEncodeError` at
  the step 1 print) after login only, so no site writes. Third run with `-X utf8`:
  ```
  [1] login → ok
  [2] setup_complete → {"message": {"status": "ok"}}
  ```
  My read-back of `Installed Application` over REST did not return the requested fields (`KeyError` in the
  script). Confirmed in the bench console instead:
  `APPS [india_compliance 1, erpnext 1, frappe 1] COMPANY ['Demo Kirana Store'] ITT [Non-GST, Exempted, Nil-Rated, GST 28%, GST 12%, GST 5%, GST 18% - DKS] UOM_Nos Nos`
- `python -I -X utf8 build.py <env> 3` (steps 3–7):
  ```
  [3] Item Tax Template → GST 40% - DKS: Output Tax SGST=20.0, Output Tax CGST=20.0, Output Tax IGST=40.0, Output Tax SGST RCM=-20.0, Output Tax CGST RCM=-20.0, Output Tax IGST RCM=-40.0, Output Tax SGST Refund=-20.0, Output Tax CGST Refund=-20.0, Output Tax IGST Refund=-40.0, Input Tax SGST=20.0, Input Tax CGST=20.0, Input Tax IGST=40.0, Input Tax SGST RCM=20.0, Input Tax CGST RCM=20.0, Input Tax IGST RCM=40.0
  [4] Address → Demo Kirana Store-Billing gst_state=Karnataka gst_state_number=29
  [5] Supplier → Sample Wholesale Distributors Pvt Ltd gstin=29AACCS5678M1ZJ pan=AACCS5678M
  [5] Address → Sample Wholesale Distributors Pvt Ltd-Billing gst_state_number=29
  [6] Customer → Walk-in Customer gst_category=Unregistered
  [7] Item RICE-BAS-1KG hsn=10063020 tmpl=GST 5% - DKS sell=120.0 buy=100.0
  [7] Item DAL-TOOR-1KG hsn=07136000 tmpl=GST 5% - DKS sell=160.0 buy=135.0
  [7] Item BISC-200G hsn=19053100 tmpl=GST 5% - DKS sell=40.0 buy=32.0
  [7] Item DETG-1KG hsn=34022090 tmpl=GST 18% - DKS sell=110.0 buy=88.0
  [7] Item CHRG-USB hsn=85044030 tmpl=GST 18% - DKS sell=350.0 buy=250.0
  [7] Item MILK-500ML hsn=04012000 tmpl=Nil-Rated - DKS sell=30.0 buy=27.0
  [7] Item COLA-750ML hsn=22021010 tmpl=GST 40% - DKS sell=45.0 buy=36.0
  BUILD DONE
  ```

## Results (plan §4)

Run: `exec(open("/tmp/checks.py").read(), …)` in `bench --site merchant.localhost console`, 2026-10-13.
The first attempt raised `NameError: name 'R' is not defined` (console namespace), before any check ran.

| Check | Result | Evidence |
|---|---|---|
| C1 wizard-complete | green | apps frappe/erpnext/india_compliance `1`; `setup_complete 1` |
| C2 system-settings | green | `India`, `Asia/Kolkata`, `INR`, `dd-mm-yyyy`, `#,##,###.##`, telemetry `0` |
| C3 company | green | `DKS`, `INR`, `India - Chart of Accounts`, `29AAPFD1234K1Z7`, `Registered Regular`, `AAPFD1234K`, `18`, perpetual `1`, audit trail `1` |
| C4 fiscal-year | green | `2026-04-01`, `2027-03-31` |
| C5 company-address | green | `Karnataka` / `Karnataka` / `29` / `29AAPFD1234K1Z7` / `1` |
| C6 gst-accounts | green | Input: `Input Tax CGST/SGST/IGST - DKS`; Output: `Output Tax CGST/SGST/IGST - DKS` (plus Purchase/Sales Reverse Charge rows) |
| C7 item-tax-templates | green (re-run) | first run red: `gst40` got `["2E+1","2E+1","4E+1"]` (check formatting). Re-run: `names` match all 8, `rate_mismatches: []`, `gst40: ["20", "20", "40"]` |
| C8 tax-templates | green | 4 `Output GST …- DKS`, 4 `Input GST …- DKS`, 4 categories |
| C9 items | green | all 7 rows match exactly; Item Price count `14` |
| C10 supplier | green | `29AACCS5678M1ZJ`, `Registered Regular`, `Distributor`, address `29` |
| C11 customer | green | `Unregistered`, `Individual`, `India`, gstin `null` |
| C12 gst-applies | green | template `Output GST In-state - DKS`; net `210.00`; SGST 9% row `10.90`; CGST 9% row `10.90`; no IGST; grand `231.80`; rounded `232.00`; Sales Invoice count `0`. Items: BISC `GST 5%` 40.00, DETG `GST 18%` 110.00, MILK `Nil-Rated` 60.00 |

Raw C7 line:
```
CHK FAIL | C7 item-tax-templates | {"expected": {"names": [...8 names...], "rate_mismatches": [], "gst40": ["20", "20", "40"]}, "got": {"names": [...same 8...], "rate_mismatches": [], "gst40": ["2E+1", "2E+1", "4E+1"]}}
```

### Re-run after D1 (a), 2026-10-13

C7's text formatting changed from `str(Decimal.normalize())` to `format(Decimal.normalize(), "f")`. Nothing
else in the check changed. All of C1–C12 were run once:
```
CHK PASS | C1 wizard-complete
CHK PASS | C2 system-settings
CHK PASS | C3 company
CHK PASS | C4 fiscal-year
CHK PASS | C5 company-address
CHK PASS | C6 gst-accounts
CHK PASS | C7 item-tax-templates   ("gst40": ["20", "20", "40"])
CHK PASS | C8 tax-templates
CHK PASS | C9 items
CHK PASS | C10 supplier
CHK PASS | C11 customer
CHK PASS | C12 gst-applies         (Sales Invoice count 0)
```

## Deviations from the plan

1. **Branch base.** `docs/ai-workflow.md` §6 says to branch off `master`. `master` (`de77b88`) does not
   contain `docs/worklog/` or `.claude/` (`git ls-tree master` → 0 matches) because `setup/phase-0-workflow`
   is not merged. The item branch `phase0/sample-retail-company` was cut from `setup/phase-0-workflow`
   instead. Nothing is committed. Local and reversible.
2. Otherwise none. The values applied are exactly plan §2.

## Decisions needed

**D1 — C7 is red because of a fault in the check, not the site.**
*Issue.* The C7 script turns each rate into text with `Decimal.normalize()`, which writes 20 as `2E+1`.
So the text comparison failed even though the numbers match. The same run's numeric comparison found no
mismatch (`rate_mismatches: []`, which includes `GST 40% - DKS`), and step 3 read back `20.0/20.0/40.0`.
Root-cause class: **wrong check**. For a merchant: nothing; the 40% template is correct. It is your call
because the rule says a red check is never fixed or re-run without a ruling.
*Options.*
(a) Fix the formatting in the throwaway check (use `"0.##"`-style formatting instead of `normalize()`),
  re-run all of C1–C12 once, and record the output. About 1 minute. A full re-run proves the fix
  did not hide anything else. If anything else goes red, stop again.
(b) Accept C7 as green on the existing evidence (`rate_mismatches: []` + step 3 read-back) without re-running.
  No time. The written C7 result stays "red" in the log with your acceptance noted.
(c) Amend plan §4 C7 to drop the separate `gst40` text comparison, since `rate_mismatches` already covers
  it, then re-run. Changes the frozen plan for no gain over (a).
*Recommendation.* (a). It is the cheapest way to get a clean green run on record, and the assertion
stays exactly as approved. I would pick (b) only if you want to avoid touching the site again, and the
re-run only reads (C12 rolls back).

**Ruling (maintainer, 2026-10-13):** D1 → (a). Applied, and the re-run is all green (above).
