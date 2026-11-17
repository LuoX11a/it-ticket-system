# Requirements – IT Service Request Ticketing System (V1.0)

## 1. Problem and users
Small teams often handle IT problems through email or verbal requests. Requests get lost
and nobody can see their status. This app gives every request a record, a status and a
controlled workflow.

| Role | Can do | Cannot do |
|---|---|---|
| **Employee** | Submit tickets; view **own** tickets | Change status; view other people's tickets |
| **IT Support** | View **all** tickets; move a ticket to its next status; write a resolution note | Skip a status; move a ticket backwards |

**Scope note:** login is *simulated* (choose role + username in the sidebar). Real
authentication is out of scope for this prototype (see risk R3).

## 2. Functional requirements
| ID | Requirement | Acceptance criteria |
|---|---|---|
| FR1 | An employee can submit a ticket with title, description and category (Hardware / Software / Network / Account). | New ticket gets a unique ID, status `New`, and records the creator. |
| FR2 | An employee can view a list of their own tickets and each ticket's status. | List contains only tickets created by that user. |
| FR3 | IT Support can view all tickets and move a ticket to its next status. | IT list contains every ticket; status changes by exactly one step. |
| FR4 | IT Support must enter a resolution note when resolving a ticket. | Resolving with an empty/blank note is rejected; status stays `In Progress`. |

## 3. Business rules
| ID | Rule |
|---|---|
| BR1 | Status can only move `New → In Progress → Resolved`. No skipping, no moving back. `Resolved` is final. |
| BR2 | Only the IT Support role can change status. |
| BR3 | Employees can only see their own tickets. |
| BR4 | Title is required, 5–100 characters after trimming spaces. Description is at most 1000 characters. |

## 4. Software quality requirements
| ID | Quality attribute | Requirement | Evidence |
|---|---|---|---|
| QR1 | Reliability | Any invalid input or invalid action returns a clear error message and does not crash the app. | Failure-case tests; UI shows `st.error` |
| QR2 | Verifiability / maintainability | Every business rule has at least one automated test, and all tests must pass in CI on every push/PR to `main`. | `docs/traceability.md`; GitHub Actions |
| QR3 | Security | Permission checks are enforced in the business-logic layer (`tickets/service.py`), not only by hiding UI controls. Unknown roles are rejected (whitelist). | Unauthorised-access tests call service functions directly |

## 5. Risks
| ID | Risk | Impact | Response |
|---|---|---|---|
| R1 | Permissions only enforced in the UI could be bypassed. | Employees could change ticket status. | Enforce roles in `service.py` (QR3); tests call the service directly. |
| R2 | Streamlit Community Cloud storage is not persistent; data resets when the app restarts. | Demo data may be lost. | In-memory store with seeded demo data; documented as a prototype limitation. |
| R3 | Simulated login: anyone can pick the IT role. | Identity cannot be trusted. | Declared out of scope; production would need real authentication. |


## 6. V1.1 changes (CR-1, Issue #2)
Source: validation session on V1.0 (docs/vv_evidence.md).

| ID | Requirement | Acceptance criteria |
|---|---|---|
| FR5 (new) | A user can open one ticket and see its full details: title, status, category, creator, submitted time, full description and full resolution note. | All text shown in full (no truncation); viewing does not change the ticket. |
| BR5 (new) | Employees can open only their own tickets; IT Support can open any ticket. Another user's ticket returns the same "not found" message as a missing ticket. | Employee "bob" cannot open alice's ticket; error does not reveal it exists. |
| UI change | Role switch and username are at the top of the main page (not the sidebar). | Mobile user can switch role without opening the sidebar. |

Unchanged: FR1–FR4, BR1–BR4, QR1–QR3.

### Deferred
- Ticket priority (earlier idea) – **not raised by the user**, so not included in CR-1 to keep the change focused.


## V1.1 additions (CR-1) – `tests/test_ticket_details.py`
| Requirement / Rule | Test(s) | Test type | Risk controlled |
|---|---|---|---|
| FR5 | `test_employee_opens_own_ticket` | Happy path | – |
| FR5 (defect V3) | `test_full_resolution_text_is_returned` (1500-char note) | Defect regression | Truncated data |
| FR5 | `test_viewing_does_not_change_ticket` | Side-effect check | Accidental changes |
| BR5 | `test_employee_cannot_open_other_users_ticket` | Unauthorised data access | Data leakage |
| BR5 | `test_other_users_ticket_and_missing_ticket_give_same_error` | Information leakage | ID enumeration |
| BR5 | `test_it_can_open_any_ticket` | Permission | – |
| Caller input | `test_invalid_ticket_id_rejected` (0, -1, "1", 1.5, None, True) | Invalid input / boundary | Tampered input |
| QR3 | `test_unknown_role_cannot_open_ticket` | Unauthorised access | R1, R3 |

**Regression:** all 23 V1.0 tests in `tests/test_service.py` kept unchanged and re-run → 38/38 passed.
