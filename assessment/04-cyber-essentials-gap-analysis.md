# 4. Cyber Essentials gap analysis

> Fictional business. Requirements are quoted from the official NCSC document.

**Standard used:** [Cyber Essentials: Requirements for IT Infrastructure v3.3](https://www.ncsc.gov.uk/files/cyber-essentials-requirements-for-it-infrastructure-v3-3.pdf), NCSC, April 2026. The [NCSC Cyber Essentials resources page](https://www.ncsc.gov.uk/cyberessentials/resources) lists v3.3 as the current version, effective from 27 April 2026. Applications started before that date could continue under v3.2. Checked on 15 October 2026.

Cyber Essentials is a UK government-backed scheme that certifies an organisation has five basic technical controls in place. It doesn't cover everything (backups, training and incident response are outside it), but it blocks most common, untargeted internet attacks.

## Verdict: Quillmere would fail today

Every one of the five themes has at least one requirement the firm doesn't meet. The biggest single blocker is that none of its cloud services use multi-factor authentication. v3.3 says: "authentication to cloud services must always use MFA".

| Theme | Status today | Main gap | Risks |
|---|---|---|---|
| Scope | Not met | Unsupported reception PC and a personal family PC are in scope and fail other controls | R09, R10 |
| 1. Firewalls | Not met | Router admin open to the internet. Undocumented port forward to the NAS. Firewall off on one laptop | R10, R12 |
| 2. Secure Configuration | Not met | Default passwords on router, NAS and printer. No lockout or screen lock rules. Unneeded software installed | R06, R08, R10, R13 |
| 3. Security Update Management | Not met | Windows 10 PC unsupported. No 14-day patching. Old phones and NAS firmware | R03, R09, R12, R13 |
| 4. User Access Control | Not met | No MFA. Everyone is an admin. Leavers' accounts active. Shared logins | R01, R05, R06, R07, R11 |
| 5. Malware Protection | Partly met | Defender is on the laptops. Family PC and reception PC can't be relied on | R03, R10 |

## Scope

> "A scope that doesn't include end-user devices isn't acceptable. If your organisation's data or services are hosted on cloud services, these services must be in scope. Cloud services cannot be excluded from scope."

| | |
|---|---|
| Current state | Everything listed in the [asset inventory](02-asset-inventory.md) is in scope, apart from staff home routers (out of scope under v3.3) |
| Gap | Two devices can't pass in their current form. The reception PC runs Windows 10, which is unsupported. The bookkeeper's family PC is a personal device ("BYOD") used for work, so v3.3 puts it in scope, and it is shared by the household with no separate work login |
| Fix | Replace the reception PC. Give the bookkeeper a company laptop so the family PC no longer touches work data |
| Effort and cost | About £1,300 to £1,800 for two devices (rough estimate). Half a day of IT contractor time to set them up |

## 1. Firewalls

> Aim: "To make sure that only secure and necessary network services can be accessed from the internet."

Key requirements: "You must protect every device in scope with a correctly configured firewall", and for every firewall, "change default administrative passwords", "prevent access to the administrative interface ... from the internet, unless there is a clear and documented business need", "block unauthenticated inbound connections by default", "ensure inbound firewall rules are approved and documented by an authorised person, and include the business need", and "remove or disable unnecessary firewall rules". Also: "Make sure you use a software firewall on devices which are used on untrusted networks, such as public wifi hotspots."

| | |
|---|---|
| Current state | The ISP router blocks inbound connections by default. Its admin password has never been changed and remote administration is on. A previous IT contractor opened a port so staff could reach the NAS from home. Nobody wrote down why. Windows Defender Firewall is on for 9 laptops. It was turned off on one laptop during a printer fix in 2025 and never turned back on |
| Gap | Default admin password. Admin interface reachable from the internet with no documented need. An inbound rule with no approval or record, which is no longer needed now that files are in OneDrive. One laptop with no software firewall, used on home and public Wi-Fi |
| Fix | Set a strong, unique router admin password and store it in the password manager. Turn off remote administration. Delete the NAS port forward. Keep a one-page firewall record: each inbound rule, who approved it and why (currently empty, which is the goal). Turn the laptop firewall back on and stop users turning it off (Intune policy, see the action plan) |
| Effort and cost | 1 to 2 hours of IT contractor time, about £100 to £200 (rough estimate) |

## 2. Secure Configuration

> Aim: make sure computers and network devices are properly configured to "reduce vulnerabilities" and "provide only the services required to fulfil their role".

Key requirements: regularly "remove and disable unnecessary user accounts", "change any default or guessable account passwords", "remove or disable unnecessary software", "disable any auto-run feature which allows file execution without user authorisation", "ensure users are authenticated before allowing them access to organisational data or services", and "ensure appropriate device locking controls". Device unlocking must be protected against brute force by throttling ("no more than 10 guesses in 5 minutes") or "locking devices after no more than 10 unsuccessful attempts", with a PIN or password of "at least 6 characters" if it only unlocks the device.

| | |
|---|---|
| Current state | Laptops are set up by hand, each a little differently. Router, NAS and printer still use default or weak admin passwords. Old Java and a second PDF reader are installed on most laptops but not used. No lockout or screen lock policy is set centrally, so nobody can say what each laptop does. Personal phones have no screen lock requirement. All staff are local administrators |
| Gap | Default passwords on three devices. Unneeded software. Device locking and lockout not configured or evidenced. No standard build, so the firm can't prove the settings to an assessor |
| Fix | Change all default device passwords. Uninstall unused software. Join the laptops to Microsoft Entra ID and manage them with Intune (included in Microsoft 365 Business Premium) so one policy sets: screen lock after 5 minutes, lockout after 10 failed attempts, Windows Hello PIN of at least 6 digits, auto-run off, BitLocker on. Use app protection so work email only opens on phones with a screen lock. Remove admin rights from daily accounts (also a User Access Control fix) |
| Effort and cost | Microsoft 365 Business Premium upgrade (see the action plan for cost). 1 to 2 days of IT contractor time to set up the policies, about £600 to £1,000 (rough estimate) |

## 3. Security Update Management

> Aim: "Ensure that devices and software are not vulnerable to known security issues for which fixes are available."

Key requirements: all software in scope must "be licensed and supported", "be removed from devices when it becomes unsupported", "have automatic updates enabled where possible", and be updated "within 14 days of release" where the update fixes vulnerabilities the vendor calls "critical" or "high risk", or with "a CVSS v3 base score of 7 or above", or where the vendor gives no details of severity.

| | |
|---|---|
| Current state | Windows Update runs on laptops but staff postpone restarts, and several are weeks behind. The reception PC runs Windows 10. Microsoft ended support on 14 October 2025 and the firm didn't buy Extended Security Updates. NAS firmware is about a year old. Some personal phones no longer receive updates. Nobody checks whether updates have been installed |
| Gap | Unsupported operating system in scope (an outright fail). No evidence that critical and high-risk updates go on within 14 days. Firmware and phones not covered |
| Fix | Replace the reception PC. Use Intune update rings to install Windows and Microsoft 365 updates automatically and force a restart within a set deadline. Turn on automatic updates in browsers and the PDF reader. Update NAS and router firmware and turn on their auto-update. Only allow work email on phones with a supported operating system. The practice manager checks the Intune update report every Monday |
| Effort and cost | New PC £600 to £900 (rough estimate). Update policies are part of the Intune setup above. About 15 minutes a week to check |

## 4. User Access Control

> Aim: ensure that user accounts "are assigned to authorised individuals only" and "provide access to only those applications, computers and networks that the user needs to carry out their role".

Key requirements: "have in place a process to create and approve user accounts", "authenticate users with unique credentials", "remove or disable user accounts when they're no longer required", "implement MFA, where available" (and "authentication to cloud services must always use MFA"), "use separate accounts to perform administrative activities only", and "remove or disable special access privileges when no longer required". v3.3 also says accounts used by third parties such as an IT contractor are in scope. Where passwords are used, they need technical controls for quality, such as MFA, a minimum of 12 characters, or a minimum of 8 characters with a deny list of common passwords.

| | |
|---|---|
| Current state | Accounts are created when someone asks the practice manager. Two leavers in the last year: one Microsoft 365 account still enabled, and the shared bookkeeping login unchanged. No MFA on Microsoft 365, the accounting software or the payroll software. All staff are local admins. The practice manager uses a global admin account for everyday email. The IT contractor uses a shared `admin@` account whose password three people know. Microsoft 365 already enforces an 8-character minimum and Microsoft's own banned password list for cloud accounts |
| Gap | No MFA on cloud services (an outright fail under v3.3). No separate admin accounts. No joiners and leavers process. Shared credentials, so actions can't be traced to a person |
| Fix | Turn on MFA for every Microsoft 365, accounting and payroll account, using the Microsoft Authenticator app. Write a one-page joiners, movers and leavers checklist and use it from today. Disable the leaver's account. Replace shared logins with named ones. Give the practice manager and the IT contractor separate named admin accounts with MFA, used only for admin. Remove local admin rights from daily accounts. Roll out a password manager |
| Effort and cost | MFA: £0, about half a day including helping staff set up the app. Password manager: about £400 to £1,000 a year (rough estimate). Removing local admin: part of the Intune setup |

## 5. Malware Protection

> Aim: "To restrict execution of known malware and untrusted software, from causing damage or accessing data."

Key requirements: "a malware protection mechanism is active on all devices in scope". Anti-malware software must "be updated in line with vendor recommendations", "prevent malware from running", "prevent the execution of malicious code" and "prevent connections to malicious websites over the internet". The alternative is application allow listing, where only approved, code-signed applications can run.

| | |
|---|---|
| Current state | Microsoft Defender Antivirus is on and updating on the Windows 11 laptops. Nobody has checked that web protection (Microsoft Defender SmartScreen) is on everywhere. The family PC has a free antivirus that the household installed, and anyone in the family can install software. Phones only install apps from the official app stores |
| Gap | Can't show that malicious website blocking is on for every device. The family PC can't be shown to meet the requirement. The reception PC fails anyway under Security Update Management |
| Fix | Manage Defender settings centrally through Intune, including SmartScreen. Microsoft Defender for Business (included in Business Premium) adds central alerts. Retire the family PC from work use. Keep phones limited to official app stores |
| Effort and cost | Included in the Business Premium upgrade and Intune setup |

## Getting certified

Once the action plan's quick wins and 3-month items are done, Quillmere should be able to apply for Cyber Essentials. The self-assessment is done online through IASME, the NCSC's Cyber Essentials partner, and is reviewed by a certification body. Certification needs renewing every year. At the time of writing, IASME's fee for a small organisation (10 to 49 staff) was reported as £440 + VAT. Check [iasme.co.uk](https://iasme.co.uk/cyber-essentials/) for the current fee before budgeting.

Cyber Essentials Plus adds a hands-on technical audit. It's worth considering in year two, once the basic controls have settled in.

## What Cyber Essentials does not cover

These risks from the register sit outside the scheme but still matter:

| Risk | Why it's outside CE | Covered by |
|---|---|---|
| R02 Payment fraud | A process and people problem, not a technical control | Call-back rule, training |
| R04 Backups | v3.3 says backing up "is not a technical requirement of Cyber Essentials" but is "highly recommend[ed]" | Action plan, 3 months |
| R14 Incident response | Not part of the scheme | One-page plan, yearly exercise |
| R15 Misdirected data | Data handling, not a technical control | Client portal, training |

The NCSC's [10 Steps to Cyber Security](https://www.ncsc.gov.uk/collection/10-steps) covers these wider areas. Each risk in the register is mapped to one or more of the 10 Steps.
