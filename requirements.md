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
