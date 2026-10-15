# 1. Scope and context

> **Quillmere Accountancy Ltd is a fictional business.** It was invented for this portfolio exercise. Any resemblance to a real firm is a coincidence. Every person, number and system below is made up, except where a public source is linked.

## The business

| | |
|---|---|
| Name | Quillmere Accountancy Ltd (fictional) |
| Location | One small office in Hertfordshire, plus staff working from home |
| People | 12: 2 partners (one is the managing partner), 1 practice manager, 6 accountants, 1 payroll administrator, 1 part-time bookkeeper, 1 receptionist |
| Clients | About 600: sole traders, small limited companies and landlords |
| Services | Year-end accounts, self assessment tax returns, VAT returns, payroll, bookkeeping |
| IT support | A local IT contractor, paid by the hour, called when something breaks |
| Who looks after IT day to day | The practice manager, alongside their main job. No one has security training |
| Busy periods | January (the 31 January self assessment deadline) and the end of each VAT quarter |

The firm moved most of its work to Microsoft 365 and cloud accounting software over the last five years. Six staff work from home two or three days a week.

## The data it holds

This is the main reason the firm matters to an attacker.

| Data | Examples | Why it's sensitive |
|---|---|---|
| Client financial records | Bank statements, accounts, tax returns, VAT records | Confidential. Useful for fraud |
| Personal data | Names, addresses, dates of birth, National Insurance numbers, tax references (UTRs) | Personal data under UK GDPR. Enough to commit identity fraud |
| Identity documents | Passport and driving licence scans collected for anti-money-laundering checks | High risk if leaked. Can't be "changed" like a password |
| Payroll data | Client employees' salaries and bank details | Personal data of people who never chose Quillmere |
| Access to money and HMRC | Online banking, HMRC agent services account | Direct route to fraud |

Under UK GDPR the firm is a data controller. If a personal data breach is likely to put people at risk, it must report it to the Information Commissioner's Office (ICO) within 72 hours of becoming aware of it ([ICO guidance](https://ico.org.uk/for-organisations/report-a-breach/personal-data-breach/personal-data-breaches-a-guide/)).

## What an attack would cost Quillmere

These are estimates for this fictional firm, not statistics.

| Cost | How it would hit |
|---|---|
| Lost working time | 11 fee-earning staff unable to work. A week's outage in January could mean missed client deadlines and HMRC penalties passed back to the firm |
| Fraud losses | One diverted client payment or refund could be tens of thousands of pounds |
| Recovery | Emergency IT contractor time, new devices, rebuilding files from whatever backups survive |
| Legal and regulatory | ICO reporting, possible enforcement, letters to up to 600 clients and their employees |
| Reputation | Accountancy runs on trust. Clients who hear their passport scans leaked may leave |

### What the official numbers say

The UK government's [Cyber Security Breaches Survey 2025/2026](https://www.gov.uk/government/statistics/cyber-security-breaches-survey-20252026/cyber-security-breaches-survey-20252026) (published 30 April 2026) found:

- 43% of UK businesses reported a cyber security breach or attack in the last 12 months. For small businesses it was 46%.
- Phishing was by far the most common type, experienced by 38% of businesses.
- 24% of businesses reported having the technical controls in all five Cyber Essentials areas.
- Only 5% of businesses held Cyber Essentials certification, rising to 12% of small businesses.

The same survey found that the typical (median) business put the cost of its most disruptive breach at £0, but a minority faced much higher costs. That fits Quillmere: most attempts will bounce off or cost a few hours. The risk this assessment is about is the one serious incident that leaks client data or diverts a payment.

## Scope of this assessment

The scope follows the rules in [Cyber Essentials: Requirements for IT Infrastructure v3.3](https://www.ncsc.gov.uk/files/cyber-essentials-requirements-for-it-infrastructure-v3-3.pdf) (NCSC, April 2026), so the same scope can be used for certification later.

**In scope**
- The whole organisation. No sub-set is excluded.
- Every end-user device: the 10 laptops, the reception PC, staff phones that access work email (including personal phones, which v3.3 counts as in scope as "bring your own device"), and the part-time bookkeeper's home PC.
- The office router and the network storage box (NAS).
- Every cloud service holding the firm's data. v3.3 says plainly: "Cloud services cannot be excluded from scope."
- All accounts the firm owns, including the shared admin account the IT contractor uses.

**Out of scope**
- Staff home routers. v3.3 puts routers not supplied by the organisation out of scope, which is why software firewalls on laptops matter.
- The brochure website, which a web designer hosts and which holds no client data.
- Paper records and physical office security, except where they affect IT (for example, the password notebook).

## How the assessment was done

1. Listed the assets (see [02-asset-inventory.md](02-asset-inventory.md)).
2. For each asset, asked what could go wrong, how likely it is and how bad it would be, using a 5x5 scale (see [03-risk-method.md](03-risk-method.md)).
3. Recorded every risk in [`risk_register.csv`](../risk_register.csv). The Python tool checks it and builds the [risk register report](../output/risk_register.md) and heat maps.
4. Checked the firm against each Cyber Essentials v3.3 requirement (see [04-cyber-essentials-gap-analysis.md](04-cyber-essentials-gap-analysis.md)).
5. Turned the fixes into a costed plan (see [05-action-plan.md](05-action-plan.md)) and a one-page summary for the managing partner (see [00-executive-summary.md](00-executive-summary.md)).
