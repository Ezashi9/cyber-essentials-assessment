# 2. Asset inventory

> Fictional business. The IDs below are used in the risk register's `assets` column.

The NCSC's v3.3 requirements say asset management "isn't a specific Cyber Essentials control, but effective asset management can help meet all five controls". You can't protect what you don't know you have.

## Devices

| ID | Asset | Count | Details | Current state |
|---|---|---|---|---|
| D01 | Staff laptops | 10 | Windows 11 Pro, bought 2022 to 2024. Used in the office, at home and at client sites | Staff log in as administrators. 3 of 10 encrypted with BitLocker. Updates installed when staff remember. Microsoft Defender Antivirus on |
| D02 | Reception PC | 1 | Windows 10 desktop. Email, web browsing, scanning client ID documents | Unsupported since 14 October 2025. No Extended Security Updates bought |
| D03 | Office router | 1 | Business broadband router from the ISP. Also the office firewall and Wi-Fi | Admin password never changed. Remote administration switched on. One port forward to the NAS |
| D04 | Network storage (NAS) | 1 | Shared drive for older client files. Nightly backup to an attached USB disk | Login page reachable from the internet. Firmware a year out of date |
| D05 | Printer and scanner | 1 | Multifunction device, scans to email | Default admin password |
| D06 | Mobile phones | 12 | 2 company iPhones (partners). About 10 personal phones with Outlook | No screen lock rule. Some too old for updates |
| D07 | Home routers | 6 | Staff-owned broadband routers | Out of Cyber Essentials scope. Firewall protection has to come from the laptops |
| D08 | Bookkeeper's home PC | 1 | Family Windows PC, one login shared by the household | Personal device used for work, so in scope as BYOD |

## Accounts

| ID | Asset | Details | Current state |
|---|---|---|---|
| A01 | Microsoft 365 user accounts | 14 accounts: 12 staff and 2 former staff | No MFA. One leaver's account still enabled |
| A02 | Microsoft 365 admin accounts | Practice manager's everyday account is a global admin. The IT contractor uses a shared `admin@` account | Shared password known by 3 people. No MFA |
| A03 | Local Windows admin | Every staff login on every laptop | All users are administrators |
| A04 | Accounting and practice software logins | Named logins for accountants. One shared login for bookkeeping | Shared password not changed since two leavers |
| A05 | HMRC online services | Agent services account and Government Gateway sign-in | HMRC requires 2-step verification |
| A06 | Online business banking | 2 partners | Bank requires a card reader or app approval |
| A07 | Device admin logins | Router, NAS, printer | Default or weak passwords |

## Cloud services

| ID | Service | What it holds | Notes |
|---|---|---|---|
| C01 | Microsoft 365 Business Standard | Email, OneDrive, SharePoint, Teams | The firm's main system. Security Defaults turned off years ago "because MFA annoyed people" |
| C02 | Cloud accounting and practice management software | Client books, tax returns, deadlines, client portal | Supports MFA, not turned on |
| C03 | Cloud payroll software | Payroll for about 40 client businesses | Supports MFA, not turned on |
| C04 | HMRC online services | Filing and client authorisations | See A05 |
| C05 | Online banking | The firm's own accounts and client money | See A06 |
| C06 | Business password manager | None yet | Recommended in R05 |

## Data

| ID | Data | Where it lives |
|---|---|---|
| DA1 | Client financial records | C02, C01 (email attachments, OneDrive), D04 (older years) |
| DA2 | Personal data of clients | C02, C01 |
| DA3 | Identity documents for anti-money-laundering checks | Scanned at D02, stored in C01 and C02 |
| DA4 | Client employees' payroll data | C03 |
| DA5 | The firm's own finance and HR records | C01, D04 |
