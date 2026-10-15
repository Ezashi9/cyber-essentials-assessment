# 5. Prioritised action plan

> Fictional business. All costs are rough estimates for a 12-person firm, excluding VAT, based on typical 2026 prices. They are not quotes. Get real quotes before committing.

The plan is ordered by how much risk each step removes for the money and effort. Most of the biggest risks can be cut in the first two weeks for almost nothing, because the controls are already included in what the firm pays for and just aren't switched on.

## Phase 1: Quick wins (first 2 weeks)

Mostly free. Needs the practice manager's time and a few hours from the IT contractor.

| # | Action | Risks | Cost |
|---|---|---|---|
| 1 | Turn on MFA for every Microsoft 365 account, using the Microsoft Authenticator app. Then turn it on in the accounting and payroll software | R01, R05, R11 | £0. About half a day helping staff set up |
| 2 | Block automatic email forwarding to outside addresses. Check every mailbox for forwarding rules nobody recognises | R01 | £0 |
| 3 | Bank details rule: any new or changed bank details are confirmed by phone on a number already on file. Brief all staff and add a line to client engagement letters | R02 | £0 |
| 4 | Disable the former employee's Microsoft 365 account. Change the shared bookkeeping login password. Start using a leavers checklist | R07 | £0 (saves one licence) |
| 5 | Give the practice manager a separate admin account with MFA. Replace the shared `admin@` account with a named one for the IT contractor | R06, R11 | £0 |
| 6 | Stop using the reception PC for email and web browsing. Order a Windows 11 replacement | R09 | £600 to £900 |
| 7 | Router and NAS: change admin passwords, turn off remote admin, close the NAS port, update firmware. Change the printer's default password | R12 | £100 to £200 contractor time |
| 8 | Turn on BitLocker on the 7 unencrypted laptops and save the recovery keys to Microsoft 365. Turn the firewall back on for the one laptop where it's off | R08, R10 | £0 |
| 9 | Turn on automatic updates on every laptop and install anything outstanding. Uninstall old Java and the second PDF reader | R03 | £0 to £300 contractor time |
| 10 | Roll out a business password manager. Delete the password spreadsheet and shred the notebook | R05 | £400 to £1,000 a year |
| 11 | 30-minute staff session: spotting phishing, why MFA matters, the bank details rule, how to report something odd | R01, R02, R15 | £0 using free [NCSC small business guidance](https://www.ncsc.gov.uk/collection/small-business-guide) |

**Phase 1 total:** about £1,100 to £2,400 (mostly the new PC and password manager).

**Effect:** the only Critical risk (R01) drops to Medium. Payment fraud, leavers, the exposed NAS, the old PC and unencrypted laptops all drop sharply.

## Phase 2: Next 3 months

Needs a budget decision from the partners and 2 to 3 days of IT contractor time.

| # | Action | Risks | Cost |
|---|---|---|---|
| 12 | Upgrade Microsoft 365 Business Standard to Business Premium. This adds Intune (device management), Microsoft Defender for Business and Conditional Access | R03, R06, R08, R13 | Roughly £5 to £8 more per user per month, so about £700 to £1,200 a year for 12 users |
| 13 | Join laptops to Microsoft Entra ID and manage them with Intune: update rings with deadlines, screen lock, lockout after 10 attempts, BitLocker, firewall on, Defender settings | R03, R08, R10 | £600 to £1,000 contractor time |
| 14 | Remove local admin rights from everyday accounts. The IT contractor installs software on request | R06 | Included in item 13 |
| 15 | App protection for phones: work email only on phones with a screen lock and a supported operating system. Remote wipe of work data | R13 | Included in item 12 |
| 16 | Company laptop for the part-time bookkeeper. Stop work on the family PC | R10 | £700 to £900 |
| 17 | Backups: keep one copy offline or in storage that can't be changed or deleted, add a Microsoft 365 backup service, test a restore and record the result | R04 | £300 to £800 a year |
| 18 | One-page incident plan: who decides, who to call, ICO 72-hour reporting, Action Fraud, insurer, template letter to clients | R14 | £0 |
| 19 | Send client documents through the client portal by default. No personal email or messaging apps for client data. Add a short send delay in Outlook | R15 | £0 |
| 20 | Apply for Cyber Essentials | All CE themes | Around £440 a year for a small organisation (check IASME's current fee) |

**Phase 2 total:** about £2,700 to £4,300 in the first year.

**Ongoing yearly cost after both phases:** about £1,800 to £3,400 (the Business Premium upgrade, password manager, backup service and certification renewal).

**Effect:** every risk is Medium or Low. The firm meets all five Cyber Essentials themes and can certify.

## Phase 3: Longer term (3 to 12 months)

| # | Action | Risks | Cost |
|---|---|---|---|
| 21 | Supplier review: list each supplier, the data it holds, whether it has Cyber Essentials or similar, and whether MFA is on. Export key client data from the accounting software monthly | R11 | £0 to £200 |
| 22 | Run a tabletop exercise with the NCSC's free [Exercise in a Box](https://www.ncsc.gov.uk/information/exercise-in-a-box) | R04, R14 | £0, half a day |
| 23 | Quarterly checks: user accounts against the staff list, the Intune update report, a backup restore test, the firewall rule record | R03, R04, R07, R12 | About 2 hours a quarter |
| 24 | Repeat the phishing session every year and for every new starter | R01, R02 | £0 |
| 25 | Review this risk register every year, and after any incident or big change | All | £0 |
| 26 | Consider Cyber Essentials Plus in year two, and check whether cyber insurance is worth it | All | Get quotes |

## Who owns what

| Role | Responsible for |
|---|---|
| Managing partner | Budget sign-off. Bank details rule. Incident plan. Supplier review. Final say in an incident |
| Practice manager | Day-to-day: MFA rollout, leavers checklist, quarterly checks, staff session, Cyber Essentials application |
| IT contractor | Router, NAS, laptops, Intune setup, backups. Works through a named admin account with MFA |
| All staff | Report anything suspicious straight away. Follow the bank details rule. Use the client portal |

## Score before and after

Generated by `risk_register.py`. See [output/risk_register.md](../output/risk_register.md).

| Rating | Today | After the plan |
|---|---|---|
| Critical | 1 | 0 |
| High | 11 | 0 |
| Medium | 3 | 8 |
| Low | 0 | 7 |

The total score across all 15 risks falls from 195 to 81, 58% lower.
