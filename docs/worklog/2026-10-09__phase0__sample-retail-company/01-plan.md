---
date: 2026-10-12
session: phase0
task: Sample Indian retail company on merchant.localhost
lane: config
phase: approved
status: approved
plan-ref: docs/phased-plan.md §2 Phase 0 (checklist #2 in docs/phase-0-log.md)
---

# Sample Indian retail company — plan

## Handoff card

**Summary.** The site is blank: setup wizard not run, 0 companies, 0 accounts, 0 items. 18,687 HSN codes
are already loaded. Plan: run the setup wizard over the API (company, GSTIN, fiscal year, GST templates),
then add 1 company address, 1 supplier, 1 walk-in customer and 7 items with HSN, GST template and prices.
Nothing is done yet. You must decide three things: the home state, which GST slabs to set up, and audit
trail on/off.

| Claim | Evidence pointer | Status |
|---|---|---|
| Site is blank, setup wizard not run | `obs1.py` → `Company: 0`, `Account: 0`, `is_setup_complete: 0` ×3 (§1) | proved |
| India Compliance makes GST templates during the wizard | `india_compliance/setup_wizard.py:131` → `make_default_tax_templates` (§1) | proved |
| Shipped item GST templates are 5/12/18/28%, Nil-Rated, Exempted, Non-GST — no 40% | `gst_india/data/tax_defaults.json` (§1) | proved |
| India Compliance accepts a 40% rate | `gst_india/constants/__init__.py:1429` `GST_TAX_RATES` includes `40.000` | proved |
| GST 2.0 rates (5/18/40, from 22-09-2025) and the per-item rates in §2 | none in the repo | **UNVERIFIED** |
| All checks C1–C12 | not run (nothing built) | not done |

**Tests skipped.** None planned to be skipped. All checks are `needs-stack`.
**Not done (by design).** No opening stock, no B2B customer, no Sales Invoice is saved. Item #3 (GST
invoice + GSTR-1/3B) does those.
**Decisions needed.** None open. D1–D3 ruled 2026-10-12 (end of file).
**If you say go.** `/build` runs §3 in order against `merchant.localhost`, runs C1–C12, and writes
`02-done.md` with each check's output. The item closes there (config lane).

---

## 1. Today (observed 2026-10-12)

The stack was stopped. It was restarted with `docker compose -p merchant-erp -f infra/compose.local.yaml start`
→ `/api/method/ping` → `{"message":"pong"}`. Observation scripts were throwaways in the scratchpad, run with `bench --site merchant.localhost console`.

- **Wizard:** `Installed Application` → frappe/erpnext/india_compliance `is_setup_complete: 0`.
- **Records:** Company, Account, Fiscal Year, Item, Supplier, Customer, Address, Warehouse, UOM, Item Group,
  Customer/Supplier Group, Territory, Price List, Item Tax Template, Sales/Purchase Taxes Template → all `0`.
  `GST HSN Code` → `18687` (4-digit 1340, 6-digit 3180, 8-digit 14167).
- **System Settings:** `country/time_zone/language/currency` = `None`; `date_format` `yyyy-mm-dd`;
  `number_format` `#,###.##`; `enable_telemetry` **`1`**. Global Defaults: `default_currency` `INR`.
- **GST Settings (selected):** `enable_api 1` but `api_secret None`. `is_api_enabled()` returns
  `enable_api and can_enable_api(settings)` (`gst_india/utils/__init__.py:975-984`), so no GST portal
  calls are made without credentials. `validate_hsn_code 1`, `min_hsn_digits 6`, `hsn_wise_tax_breakup 1`,
  `enable_e_invoice 0`, `enable_e_waybill 1`, `e_waybill_threshold 50000`. Every child table is empty (`gst_accounts 0`, `gst_uom_map 0`).
- **What the wizard does** (read in the running image):
  - Frappe `setup_wizard.py:59` exposes `setup_complete(args)` over the API. Line 105 reads
    `enable_telemetry` from args. Line 202 writes it to System Settings. Lines 316-318 create a user only
    if `email` is given.
  - ERPNext `setup_wizard.py` runs `install_fixtures.install(country)`, then `install_company`
    (Fiscal Year + Company, `enable_perpetual_inventory 1`, `chart_of_accounts` from args), then
    `install_defaults` (price lists Standard Buying/Selling, etc.). The fixtures create Item Group
    `Products`, Customer Group `Individual`, Supplier Group `Distributor`, Territory `India`
    (`install_fixtures.py:42,155,175,243`). The company creates warehouse `Stores` (`company.py:387`).
  - India Compliance adds wizard fields `company_gstin`, `default_gst_rate` (default `18.0`) and
    `enable_audit_trail` (`public/js/setup_wizard.js:41-95`).
    `setup_company_taxes` → `make_default_tax_templates(company, default_gst_rate)` → 4 tax categories,
    7 Item Tax Templates, 4 sales + 4 purchase tax templates (`tax_defaults.json`). Then it sets the company
    GSTIN and `gst_category`. With no API it creates **no address** (`setup_wizard.py:107`).
  - Audit trail: "Once enabled, Audit Trail cannot be disabled" (`audit_trail/overrides/accounts_settings.py:17`).
- **Chart of accounts for India:** `get_charts_for_country("India")` → `['India - Chart of Accounts']`.
  It contains the parents India Compliance needs (`Duties and Taxes`, `Tax Assets`, `Stock Expenses`,
  `Indirect Expenses`: 1 hit each in `in_standard_chart_of_accounts.json`).
- **Country defaults:** India `date_format` `dd-mm-yyyy`, `number_format` `#,##,###.##`, timezone `Asia/Kolkata`.
- **Sample GSTINs** were built and accepted by `validate_gstin_check_digit` (`obs4.py` → `valid`):
  `29AAPFD1234K1Z7` (company) and `29AACCS5678M1ZJ` (supplier). They are made up and are never sent
  anywhere (no API credentials).
- **HSN codes used in §2 all exist in the master:** `10063020`, `07136000`, `19053100`, `34022090`, `85044030`,
  `04012000`, `22021010` (`obs3.py` → description returned, none `MISSING`).

## 2. What we set (now → after)

Values follow the rulings of 2026-10-12: D1 = (a) Karnataka (29), D2 = (b), D3 = (a) on.

**Setup wizard args** (one call):

| Arg | Now → after |
|---|---|
| language / country / timezone / currency | — → `English` / `India` / `Asia/Kolkata` / `INR` |
| enable_telemetry | System Settings `1` → `0` (offline-first) |
| company_name / company_abbr | — → `Demo Kirana Store` / `DKS` |
| chart_of_accounts | — → `India - Chart of Accounts` |
| fy_start_date / fy_end_date | — → `2026-04-01` / `2027-03-31` (Fiscal Year `2026-2027`) |
| company_gstin | — → `29AAPFD1234K1Z7` (PAN `AAPFD1234K`, partnership firm) |
| default_gst_rate | — → `18.0` |
| enable_audit_trail | — → `1` (D3) |
| setup_demo / module_accounting / module_stock | — → `0` / `1` / `1` |
| email / full_name / password | not sent: Administrator stays the only user |

**Records after the wizard:**

| Record | Now → after |
|---|---|
| Item Tax Template `GST 40% - DKS` (D2) | none → `gst_treatment Taxable`, `gst_rate 40`. Rows mirror `GST 28% - DKS` with each rate scaled: Output/Input CGST & SGST `20`, IGST `40`; RCM rows `-20/-20/-40` (output), `20/20/40` (input); Refund rows `-20/-20/-40` |
| Address `Demo Kirana Store-Billing` | none → type `Billing`, line1 `12, 1st Main Road, Jayanagar`, city `Bengaluru`, state `Karnataka`, pincode `560041`, country `India`, gstin `29AAPFD1234K1Z7`, gst_category `Registered Regular`, `is_your_company_address 1`, link Company `Demo Kirana Store` |
| Supplier `Sample Wholesale Distributors Pvt Ltd` | none → supplier_group `Distributor`, supplier_type `Company`, gstin `29AACCS5678M1ZJ`, gst_category `Registered Regular`, pan `AACCS5678M` |
| Address `Sample Wholesale Distributors Pvt Ltd-Billing` | none → line1 `45, APMC Yard, Yeshwanthpur`, city `Bengaluru`, state `Karnataka`, pincode `560022`, country `India`, gstin `29AACCS5678M1ZJ`, gst_category `Registered Regular`, link Supplier |
| Customer `Walk-in Customer` | none → customer_type `Individual`, customer_group `Individual`, territory `India`, gst_category `Unregistered`, no GSTIN, no address |

**Items** (all: `is_stock_item 1`, item_group `Products`, stock_uom `Nos`, one `taxes` row = the template.
Prices are exclusive of GST, with an Item Price in `Standard Selling` and `Standard Buying`). Rates are
GST 2.0 as best known; they are **UNVERIFIED**, see the C-gate note in §4.

| item_code | item_name | gst_hsn_code | Item Tax Template | Selling ₹ | Buying ₹ |
|---|---|---|---|---|---|
| `RICE-BAS-1KG` | Basmati Rice 1 kg (packed) | `10063020` | `GST 5% - DKS` | 120.00 | 100.00 |
| `DAL-TOOR-1KG` | Toor Dal 1 kg (packed) | `07136000` | `GST 5% - DKS` | 160.00 | 135.00 |
| `BISC-200G` | Sweet Biscuits 200 g | `19053100` | `GST 5% - DKS` | 40.00 | 32.00 |
| `DETG-1KG` | Detergent Powder 1 kg | `34022090` | `GST 18% - DKS` | 110.00 | 88.00 |
| `CHRG-USB` | USB Mobile Charger | `85044030` | `GST 18% - DKS` | 350.00 | 250.00 |
| `MILK-500ML` | Toned Milk 500 ml pouch | `04012000` | `Nil-Rated - DKS` | 30.00 | 27.00 |
| `COLA-750ML` | Aerated Soft Drink 750 ml | `22021010` | `GST 40% - DKS` (D2) | 45.00 | 36.00 |

Not changed: GST Settings (`is_api_enabled()` is already False; e-waybill stays as shipped and is
unreachable below ₹50,000 and without credentials). No other settings change.

## 3. How (in order; all scripts are scratchpad throwaways, nothing kept)

1. `POST /api/method/login` as `Administrator`. The password is read from `infra/.env.local` and never printed.
2. `POST /api/method/frappe.desk.page.setup_wizard.setup_wizard.setup_complete` with the §2 wizard args as `args` JSON.
   Wait until `Installed Application` shows `is_setup_complete 1` for all three apps.
3. `POST /api/resource/Item Tax Template`: `GST 40% - DKS` (D2). Copy the row accounts from `GST 28% - DKS` and set the rates as in §2.
4. `POST /api/resource/Address`: company address.
5. `POST /api/resource/Supplier`, then its Address.
6. `POST /api/resource/Customer`: `Walk-in Customer`.
7. `POST /api/resource/Item` ×7 (with `taxes` row), then `POST /api/resource/Item Price` ×14.
8. Run C1–C12. Record `command → output` in `02-done.md`.

If any step fails, `/build` stops and reports. It does not hand-fix data.

## 4. The checks

All are `needs-stack`, run as throwaway scripts (bench console or REST), with output copied into `02-done.md`.

| Name | Layer | What it checks | PASS means | Cost |
|---|---|---|---|---|
| C1 wizard-complete | check | Installed Application + System Settings | `is_setup_complete 1` for frappe, erpnext, india_compliance; `setup_complete 1` | needs-stack |
| C2 system-settings | check | System Settings | country `India`, time_zone `Asia/Kolkata`, currency `INR`, date_format `dd-mm-yyyy`, number_format `#,##,###.##`, enable_telemetry `0` | needs-stack |
| C3 company | check | Company `Demo Kirana Store` | abbr `DKS`, default_currency `INR`, chart `India - Chart of Accounts`, gstin `29AAPFD1234K1Z7`, gst_category `Registered Regular`, pan `AAPFD1234K`, default_gst_rate `18`, enable_perpetual_inventory `1`; Accounts Settings enable_audit_trail `1` (D3) | needs-stack |
| C4 fiscal-year | check | Fiscal Year | `2026-2027` = `2026-04-01` … `2027-03-31` | needs-stack |
| C5 company-address | check | Address linked to Company | state `Karnataka`, gst_state `Karnataka`, gst_state_number `29`, gstin `29AAPFD1234K1Z7`, is_your_company_address `1` | needs-stack |
| C6 gst-accounts | check | GST Settings → gst_accounts for DKS | rows for account_type `Input` and `Output` exist, each with cgst, sgst and igst account set (non-empty) | needs-stack |
| C7 item-tax-templates | check | Item Tax Templates of DKS | exactly `GST 5%/12%/18%/28%/40%`, `Nil-Rated`, `Exempted`, `Non-GST` (8). For each taxable one, the Output CGST rate equals the Output SGST rate, which equals gst_rate/2, and the Output IGST rate equals gst_rate (e.g. 40% → 20 / 20 / 40) | needs-stack |
| C8 tax-templates | check | Sales/Purchase Taxes and Charges Templates + Tax Category | 4 `Output GST …- DKS` + 4 `Input GST …- DKS`; categories `In-State`, `Out-State`, `Reverse Charge In-State`, `Reverse Charge Out-State` exist | needs-stack |
| C9 items | check | 7 Items + 14 Item Prices | each row of the §2 items table matches exactly (code, name, HSN, template, stock_uom `Nos`, group `Products`), with prices exact to the paisa | needs-stack |
| C10 supplier | check | Supplier + its Address | gstin `29AACCS5678M1ZJ`, gst_category `Registered Regular`, group `Distributor`; address gst_state_number `29` | needs-stack |
| C11 customer | check | Customer `Walk-in Customer` | gst_category `Unregistered`, group `Individual`, territory `India`, gstin empty | needs-stack |
| C12 gst-applies (plug-in point) | check | **Unsaved** Sales Invoice (`frappe.new_doc`, `set_missing_values`, `calculate_taxes_and_totals`; never inserted) to `Walk-in Customer`: `BISC-200G` 1 @ 40.00, `DETG-1KG` 1 @ 110.00, `MILK-500ML` 2 @ 30.00 | taxes template `Output GST In-state - DKS`; net_total `210.00`; CGST `10.90`; SGST `10.90`; no IGST row amount; grand_total `231.80`; rounded_total `232.00`. Afterwards Sales Invoice count is still `0` | needs-stack |

**Owed (human), not a check of this item:** a CA confirms the §2 HSN codes and GST rates. This goes
under the existing gate "Line up 2–3 friendly merchants + 1 CA" in STATE.

---

## Decisions needed

**D1 — Home state of the sample shop.**
*Issue.* The GSTIN's first two digits and the company address fix the shop's state. In-state sales get
CGST+SGST, out-of-state sales get IGST, so every later tax check depends on this. Nothing in the repo
says which state your merchants are in.
*Options.*
(a) Karnataka (`29`, Bengaluru addresses as in §2). Plan unchanged.
(b) Your own state: new GSTIN prefix and addresses. Same effort, about 5 values change.
*Recommendation.* (b) if your first merchants are in another state, because the sample should match them.
(a) if you have no preference. Low stakes: the site can be rebuilt.

**D2 — Which GST slabs to set up.**
*Issue.* India Compliance 16.10.0 ships item templates at 5/12/18/28% plus Nil-Rated, Exempted and Non-GST
(`tax_defaults.json`). Its rate list already includes 40% (`constants/__init__.py:1429`). As far as I know,
GST 2.0 (from 22-09-2025) moved most goods to 5% and 18%, with 40% for sin/luxury goods such as aerated drinks,
and 28% kept for a few items such as tobacco. This is **UNVERIFIED** in the repo. A wrong template on an
item means a wrong tax on a merchant's bill.
*Options.*
(a) Shipped templates only. 12% and 28% stay. No 40%, so `COLA-750ML` is dropped.
(b) Shipped templates plus `GST 40% - DKS`; 12% and 28% stay enabled. One extra record.
(c) As (b), and also disable `GST 12% - DKS` and `GST 28% - DKS`, so they cannot be picked by mistake.
  Two more settings. A 28% item (tobacco) would then need the template re-enabled.
*Recommendation.* (b). It adds the one rate GST 2.0 introduced and removes nothing. Disabling templates is
a per-merchant choice for later. I would change to (c) if your CA confirms 12% and 28% are unused for your merchants' goods.

**D3 — Audit trail.**
*Issue.* The wizard offers India Compliance's audit trail (MCA notification 24-03-2021). Once on, it
cannot be switched off on this site (`audit_trail/overrides/accounts_settings.py:17`). It records every
change to accounting documents.
*Options.*
(a) On. The sample behaves like a real company's books. It is irreversible short of recreating the
  site (`infra/erp.sh site` on a fresh site).
(b) Off. Can be switched on later from Accounts Settings.
*Recommendation.* (a). The product's pitch is audit-readiness, and the site is a disposable sample.
I would change to (b) if you plan to use this site for experiments that delete submitted documents.

**Rulings (maintainer, 2026-10-12):** D1 → (a) Karnataka · D2 → (b) shipped templates + `GST 40% - DKS` · D3 → (a) audit trail on. Plan unchanged.

**Approved (maintainer "go", 2026-10-13).** The whole plan is frozen for `/build`.
