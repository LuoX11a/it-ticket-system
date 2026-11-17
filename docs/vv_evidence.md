# Verification & Validation Evidence

## Verification (are we building the product right?)
| Activity | Method | Result |
|---|---|---|
| Requirements–test traceability review | Checked every FR/BR/QR in requirements.md maps to ≥1 test (docs/traceability.md) | All covered (V1.0 and V1.1) |
| Automated testing in CI | pytest runs on every push/PR via GitHub Actions | V1.0: 23/23 passed. V1.1: 42/42 passed (23 regression + 15 new) |

## Validation (are we building the right product?)
**Date:** 17/11/2026  **Participant:** Student peer A (used a mobile phone)
**Version tested:** V1.0 – https://luox11a-it-ticket.streamlit.app/

| Scenario | Observed | User feedback |
|---|---|---|
| As employee "carol", submit a Wi-Fi ticket and track it | Ticket submitted, but user could not find how to see its details/progress | "After submitting a ticket, it is not clear how to view the specific details of my ticket to track its progress." |
| Switch to IT Support and resolve the ticket | User could not find the role switch on the phone; thought the sidebar toggle was a "Back" button | "I couldn't figure out how to switch to the IT Support role… I thought the role-switching button on the left was a Back button." |
| As employee, read the resolution | Resolution text cut off in the table cell, even when scrolling | "The solution text in the user view is truncated… cannot be fully displayed." |

## Findings
| # | Finding | Type | Action |
|---|---|---|---|
| V1 | Role switch hidden in collapsed sidebar on mobile | Usability / requirement gap (no mobile requirement in V1.0) | CR-1: move role switch to top of main page |
| V2 | No way to view one ticket's full details | Requirement gap (FR2 only listed tickets) | CR-1: new FR5 ticket detail view |
| V3 | Resolution note truncated in table | **Defect** (FR4 note recorded but not readable) | CR-1: show full text in detail view; table keeps short columns |

**Lesson:** all automated tests passed in V1.0, yet a real user found 3 problems.
Verification proved the rules were built correctly; only validation showed the
product did not fully meet user needs.
