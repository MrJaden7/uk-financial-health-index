# UK Financial Health Index: How the 2022–2024 Rate Hike Cycle Reshaped Regional Financial Vulnerability

**Author:** Jaden Menezes  
**Date:** April 2026  
**Data Sources:** ONS Annual Population Survey, FCA Financial Lives Survey 2024, Bank of England Base Rate History, ONS Regional GDHI  
**Methodology Reference:** Urban Institute Financial Vulnerability Index (2017)  
**Tools:** Python (pandas, openpyxl, sqlite3), SQL (SQLite), Power BI  
**Dataset:** 998 rows × 19 columns — 200 UK local authorities, 2020–2024

---

## Executive Summary

Between December 2021 and August 2023, the Bank of England raised its base rate from 0.10% to 5.25% — the fastest rate hiking cycle in four decades. This report analyses the impact of that cycle on household financial health across 200 UK local authorities, using a composite Financial Health Index (FHI) constructed from four official data sources.

The central finding is stark: **the rate hike cycle did not affect all regions equally.** Wealthier southern regions largely absorbed the shock — and some improved. Meanwhile, already-stressed northern and Welsh communities saw little benefit from subsequent rate cuts and remain financially scarred. A 77.7-point gap now separates the most and least financially healthy local authorities in the UK — the widest disparity in the five-year analysis period.

---

## Methodology

### Financial Health Index Construction

The FHI is a composite score (0–100) calculated for each local authority and year using four components, each normalised to 0–100 via min-max scaling within each year:

| Component | Weight | Source | Direction |
|-----------|--------|---------|-----------|
| Employment rate (16–64) | 25% | ONS / Nomis APS | Higher = better |
| Unemployment rate (16+) | 10% | ONS / Nomis APS | Lower = better |
| Median household savings (£) | 15% | FCA Financial Lives Survey | Higher = better |
| % adults with zero savings | 15% | FCA Financial Lives Survey | Lower = better |
| Regional GDHI (£ million) | 35% | ONS Regional Accounts | Higher = better |

This methodology is informed by the Urban Institute's Financial Vulnerability Index, extended with the addition of Bank of England macro data and updated to include 2024 figures not yet available in the institutional version.

**FHI = (0.25 × employment_score) + (0.10 × unemployment_score) + (0.15 × savings_score) + (0.15 × zero_savings_score) + (0.35 × gdhi_score)**

---

## Key Finding 1: A 77.7-Point Chasm Between Britain's Best and Worst Areas

In 2024, Reading scores **86.18** on the Financial Health Index. South Tyneside scores **8.46**.

These are not different countries. They are both in England, 280 miles apart.

The gap between the highest and lowest scoring local authority in 2024 is **77.7 points** — wider than the gap between the UK and many developing economies on comparable indices. This is not a new divide, but the data shows it has **not meaningfully closed** despite five years of policy interventions, a pandemic recovery, and rate normalisation.

**Top 5 local authorities (2024):**

| Local Authority | Region | FHI Score |
|----------------|--------|-----------|
| Reading | South East | 86.18 |
| West Berkshire | South East | 86.15 |
| Oxfordshire | South East | 85.84 |
| Bracknell Forest | South East | 85.67 |
| Merton | London | 84.66 |

**Bottom 5 local authorities (2024):**

| Local Authority | Region | FHI Score |
|----------------|--------|-----------|
| South Tyneside | North East | 8.46 |
| Newcastle upon Tyne | North East | 8.68 |
| Middlesbrough | North East | 9.77 |
| Hartlepool | North East | 11.44 |
| North Tyneside | North East | 14.64 |

Four of the five most financially stressed local authorities in the UK are in the North East of England — a region where median household savings stood at just **£750 in 2020**, less than one month's rent in most of its urban centres.

---

## Key Finding 2: London is the Only Region That Got Worse

Of the 11 UK regions analysed, **London is the only one that recorded a decline** in average FHI between 2020 and 2023 (−5.11 points). Every other region improved or held steady.

This appears counterintuitive given London's high income levels, but reflects a structural feature of the rate hike cycle: **London's financial stress is mortgage-driven, not income-driven.** Areas with high property values carry proportionally larger mortgage debt. When rates rose from 0.10% to 5.25%, the monthly repayment increase on an average London mortgage was significantly larger in absolute terms than anywhere else in the country.

This is confirmed at the local authority level. The biggest FHI declines between 2020 and 2024 are concentrated in inner London boroughs:

| Local Authority | FHI 2020 | FHI 2024 | Change |
|----------------|----------|----------|--------|
| Kensington & Chelsea | 76.38 | 59.04 | −17.34 |
| Greenwich | 77.65 | 60.69 | −16.96 |
| Redbridge | 80.78 | 66.55 | −14.23 |
| Richmond upon Thames | 84.62 | 73.88 | −10.74 |
| Camden | 75.25 | 64.92 | −10.33 |

Kensington & Chelsea — the wealthiest postcode in Britain — fell **17.3 points** in four years. Richmond upon Thames declined in **every single year** between 2020 and 2024, the most consistent trajectory of decline of any local authority in the dataset.

The implication for consumer lending strategy is significant: **high income does not equal low financial vulnerability when leverage is extreme.**

---

## Key Finding 3: The North Was Already Left Behind Before the Rate Hikes

A common narrative attributes northern financial stress to the rate hike cycle. The data does not support this. The North-South divide was **pre-existing, structural, and stable** across the entire analysis period.

In 2020 — before a single rate hike — the average FHI gap between South and North was already **42.9 points**. By 2024, after the full rate cycle and subsequent cuts, it stood at **43.7 points**. The gap barely moved.

More telling: **19 northern local authorities had FHI scores below 25 in 2020**. In 2024, that figure is **17**. Just two areas escaped financial distress — not through improvement, but through marginal score changes near the threshold.

The North East's median household savings in 2020 were **£750**. The UK average was £2,955. That £2,200 gap is not a consequence of the rate cycle. It predates it entirely.

What the rate hike cycle *did* do was **accelerate divergence in savings behaviour**. Between 2022 and 2024:
- South West: zero-savings rate fell from 10% to **5%** — the biggest improvement nationally
- North West: zero-savings rate fell from 15% to **11%** — improved, but still more than double the South West
- London: zero-savings rate *increased* from 8% to **9%** — the only region where it worsened

---

## Key Finding 4: The "Working Poor" Problem — Employment Without Financial Security

One of the most analytically interesting findings emerges from cross-referencing employment rates with savings data. A significant cluster of local authorities shows **high employment rates but critically low savings** — what can be characterised as a "working poor" profile.

Areas like Darlington (78% employment, £2,500 median savings), Gateshead (75.6% employment, £2,500 median savings), and Cumberland (77.4% employment, £2,500 median savings) demonstrate that employment alone is insufficient as a measure of financial health.

These areas have employment rates comparable to the South East, but median savings less than 40% of the South East average. Workers in these areas are economically active but financially exposed — one unexpected expense away from financial crisis.

This finding has direct implications for financial inclusion strategy: **targeting interventions purely at unemployment misses the most structurally vulnerable employed households.**

---

## Key Finding 5: Rate Cuts Have Not Reversed the Damage for the Most Vulnerable

By December 2024, the Bank of England had cut rates from 5.25% to 4.75%. The data shows that this partial reversal **did not meaningfully improve financial health in the most stressed areas.**

The North East's average FHI in 2024 (**16.3**) is still below its 2023 peak (**19.2**) despite rate cuts. Wales (**25.2** in 2024) is below its 2023 level (**26.6**). The rate transmission mechanism — the process by which central bank decisions filter through to household finances — works faster in wealthier, more financially integrated areas.

Put simply: **rate hikes hurt the North faster than rate cuts helped it.**

The South East, by contrast, moved from 67.9 in 2020 to 80.2 at the 2023 peak, then held at 79.1 in 2024. The rate cycle was, for this region, a net positive.

---

## Limitations and Methodology Notes

**FCA data granularity:** The FCA Financial Lives Survey is available at regional (ITL1) level only — not local authority level. Savings figures are therefore applied as regional attributes to all local authorities within a region. This means within-region variation in savings behaviour is not captured.

**GDHI lag:** ONS Regional GDHI is published with an approximate 18-month lag. The 2024 data point uses forward-filled 2023 figures. This is standard practice in regional economic analysis but should be noted.

**Nomis data suppression:** The Annual Population Survey suppresses values where sample sizes are too small to be statistically reliable. Approximately 30 unemployment rate observations and 487 qualifications observations were excluded on this basis. These suppressions are concentrated in smaller rural local authorities and Scottish councils.

**Northern Ireland:** Not included in the Nomis local authority dataset used. Northern Ireland figures are available at national level only and are excluded from LA-level analysis.

---

## Conclusions and Implications

This analysis of 200 UK local authorities across five years yields three conclusions with practical relevance for financial services strategy:

**1. Risk segmentation must go below regional level.**
Regional averages mask enormous within-region variation. Luton (FHI: 46.3) sits 17 points below the East of England regional average (63.6). Slough (65.2) sits 14 points below the South East average (79.1). Any financial product or risk model using regional averages as a proxy for local financial health will systematically misprice risk.

**2. High income is not a proxy for low vulnerability.**
The Kensington & Chelsea finding — a 17-point FHI decline in the UK's wealthiest postcode — demonstrates that leverage-adjusted financial health tells a fundamentally different story than income alone. Credit risk models that do not account for debt-to-income ratios alongside absolute income levels will underestimate vulnerability in high-value property markets.

**3. Financial inclusion interventions should target the working poor, not just the unemployed.**
The existence of a "high employment, low savings" cluster in northern England and Wales suggests that employment-focused policy alone will not close the financial health gap. Savings products, financial literacy programmes, and accessible credit facilities targeted at employed but cash-poor households represent an underserved market opportunity.

---

## Data Sources

| Dataset | Source | URL |
|---------|--------|-----|
| Annual Population Survey — Labour Market | ONS / Nomis | nomisweb.co.uk |
| Financial Lives Survey 2024 — Assets & Debts | FCA | fca.org.uk/financial-lives |
| Regional Gross Disposable Household Income | ONS | ons.gov.uk |
| Official Bank Rate History | Bank of England | bankofengland.co.uk |

---

## Repository Structure

```
uk_financial_health_index/
├── data/
│   ├── nomis_unemployment.csv          # ONS unemployment by region 2019-2024
│   ├── nomis_inactivity.csv            # ONS inactivity by region 2019-2024
│   ├── nomis_la_labour.csv             # ONS labour market by local authority
│   ├── boe_base_rate.csv               # Bank of England base rate history
│   ├── ons_gdhi_regional.xlsx          # ONS regional GDHI 1997-2023
│   ├── financial-lives-survey-*.xlsx   # FCA Financial Lives data
│   └── clean/
│       └── uk_fhi_master_final.csv     # Master analytical dataset (998 rows)
├── outputs/
│   ├── q1_regional_ranking_2024.csv
│   ├── q2_rate_hike_impact.csv
│   ├── q3a_top10_las_2024.csv
│   ├── q3b_bottom10_las_2024.csv
│   ├── q4_north_south_divide.csv
│   ├── q5_zero_savings_hotspots.csv
│   ├── q6_rate_sensitivity_timeline.csv
│   ├── q7_worst_per_region_2024.csv
│   ├── q8_working_poor_analysis.csv
│   ├── q9_yoy_declining_las.csv
│   └── q10_executive_summary.csv
├── 01_data_cleaning.py                 # Data ingestion, cleaning, FHI calculation
├── 02_sql_analysis.py                  # 10 SQL queries via SQLite
├── uk_financial_health_index.pbix      # Power BI dashboard (4 pages)
└── INSIGHT_REPORT.md                   # This document
```

---

*This project was completed independently as part of a data analyst portfolio. All data is sourced from official UK government and regulatory publications and is freely available under Open Government Licence v3.0.*
