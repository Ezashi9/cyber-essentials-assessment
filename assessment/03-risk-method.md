# 3. Risk scoring method

> Fictional business. The full register is in [`risk_register.csv`](../risk_register.csv) and the generated report is [`output/risk_register.md`](../output/risk_register.md).

Each risk gets two numbers from 1 to 5: how **likely** it is to happen in the next 12 months, and how bad the **impact** would be if it did. Multiply them to get a score from 1 to 25.

- **Inherent score:** the risk as things stand today, with only the controls already in place.
- **Residual score:** the risk left over after the recommended control is in place. It is never zero. Controls make bad things less likely or less damaging. They don't make them impossible.

## Likelihood (next 12 months)

| Score | Label | Meaning for Quillmere |
|---|---|---|
| 1 | Rare | Would need an unusual chain of events. Not expected in the next few years |
| 2 | Unlikely | Could happen, but there's no particular reason to expect it this year |
| 3 | Possible | Happens to firms like this. Nothing in place would stop it |
| 4 | Likely | The attack is common and aimed at firms like this, and a weakness makes it easy |
| 5 | Almost certain | Expected to happen this year unless something changes |

## Impact

| Score | Label | Money (rough) | Data | Disruption |
|---|---|---|---|---|
| 1 | Negligible | Under £1,000 | No client data exposed | Under an hour |
| 2 | Minor | £1,000 to £5,000 | One record, contained quickly, not reportable | Up to a day for one person |
| 3 | Moderate | £5,000 to £20,000 | A few clients' data. May need reporting to the ICO | 1 to 3 days for the firm |
| 4 | Major | £20,000 to £100,000 | Many clients' data. Reportable to the ICO, clients told | About a week. Missed client deadlines |
| 5 | Severe | Over £100,000, or a threat to the firm's survival | Most or all client data | Weeks. Loss of clients |

When the measures disagree, the worst one sets the score.

## Rating bands

| Score | Rating | What the firm should do |
|---|---|---|
| 20 to 25 | Critical | Act now. Owner tracks it weekly |
| 10 to 16 | High | Fix within 3 months, sooner if cheap |
| 5 to 9 | Medium | Plan a fix. Review each quarter |
| 1 to 4 | Low | Accept and review once a year |

Because the score is a product, only 14 values are possible (1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 20, 25). The tool's tests check every one of them falls into a band.

## Why this method

A 5x5 matrix is a widely used, simple way to score risk, and it's easy for a non-technical owner to follow. It has known weaknesses:

- Scores are judgements, not measurements. Two assessors might score the same risk differently by one point. Writing the reasons in the register (the `description` and `existing_controls` columns) makes the judgement visible so it can be challenged.
- Multiplying ordinal scales is rough. A 4x3 (12) and a 3x4 (12) are not really the same risk. When scores tie, the tool ranks the higher-impact risk first, because a small firm can survive frequent small problems more easily than one big one.
- It ignores how risks combine. Phishing (R01) and no MFA make payment fraud (R02) easier. Admin rights (R06) make ransomware (R03) worse, and weak backups (R04) make it much worse. The action plan groups related fixes for this reason.

## Columns in the register

| Column | Required | Notes |
|---|---|---|
| `id` | yes | Unique, for example `R01` |
| `title`, `description` | yes | Plain English |
| `assets` | no | IDs from the asset inventory, separated by `;` |
| `existing_controls` | no | What's in place today |
| `likelihood`, `impact` | yes | Whole numbers 1 to 5 |
| `recommended_control` | yes | The fix |
| `residual_likelihood`, `residual_impact` | yes | Whole numbers 1 to 5. The residual score can't be higher than the inherent score |
| `ce_theme` | yes | One or more of the five Cyber Essentials themes, or `Outside CE` |
| `ten_steps` | no | NCSC [10 Steps to Cyber Security](https://www.ncsc.gov.uk/collection/10-steps) areas, separated by `;` |
| `owner` | yes | Who is responsible |
| `timeframe` | yes | `Quick win`, `3 months` or `Longer term` |
| `est_cost` | no | Rough cost |
