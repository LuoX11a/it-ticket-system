# Review Intake – CR-1 (Issue #2): Ticket detail view + visible role switch

## 1. Intended behaviour
- New FR5: open one ticket and see all fields in full.
- New BR5: employees open only their own tickets; IT opens any.
- Role switch moved from sidebar to top of main page.

**Must remain unchanged:** FR1–FR4, BR1–BR4 (status flow, IT-only status
change, employees see only own tickets, title/description limits).

## 2. AI tool and task
- Tool: Microsoft Copilot
- Task given: "Based on the user feedback, add a ticket detail view with a
  permission check in service.py, write tests from the requirements, and move
  the role switch out of the sidebar in app.py."

## 3. Affected files and AI assumptions
Files: `tickets/service.py` (new `get_ticket_details`), `app.py`,
`tests/test_ticket_details.py`, docs.

| AI assumption | My check | Result |
|---|---|---|
| Another user's ticket should give the same error as a missing ticket | Agreed – prevents employees guessing which IDs exist | Accepted |
| Ticket ID must be a positive int; `True` rejected even though Python treats it as 1 | Checked in Python: `isinstance(True, int)` is True, so the extra check is needed | Accepted |
| Removing the Resolution column from the table is OK because the detail view shows it | Agreed – matches feedback; table stays readable on a phone | Accepted |
| Returning the stored Ticket object is safe because the UI only reads it | Reviewer showed callers can mutate it and bypass BR1/BR2/BR4; I reproduced it | **Rejected** – now returns a copy (RF-1) |

## 4. Human verification
- Read the full diff line by line (`git diff main`).
- Checked each test's expected result against FR5/BR5, not against the code.
- Ran `pytest -v` locally: 38 passed (23 regression + 15 new).
- Manual test on phone: role switch visible; long resolution fully readable;
  user "bob" cannot see alice's tickets.

**Security checks (change touches data access):**
| Area | Check | Result |
|---|---|---|
| Identity | Username still simulated (R3, out of scope) | Unchanged, documented |
| Permissions | BR5 enforced in service layer, not just UI | Tested |
| Caller-controlled input | ticket_id type/range validated | Tested |
| Data access / sensitive data exposure | Other users' tickets not readable; error does not reveal existence | Tested |
| Configuration defaults | No new config | N/A |

**Risk classification: Medium** – adds a new data-access path (possible data
leakage) and changes the UI login area; status rules and permission model
for changing tickets are untouched.

## Known test limitations
- UI layout on mobile checked manually, not automated.
- Simulated login means anyone can type another username (R3) – BR5 protects
  against reading through the app's own logic, not against identity spoofing.
