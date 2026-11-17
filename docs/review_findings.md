# Review Findings – PR #3 (CR-1, Issue #2)

**Review tool:** Microsoft Copilot (chat). GitHub Copilot code review is not
available on this account, so the PR diff was given to Copilot chat in a new
session. Full output saved as evidence: *Review Ticket Detail Pull Request.pdf*
(attached to the PR conversation).

**Focused task given to the reviewer:**
1. Can an employee read another user's ticket through `get_ticket_details()`?
2. Does this PR change any V1.0 rule (BR1–BR4)?
3. Are tests missing for invalid ticket IDs or edge cases?

**Reviewer's answer to Q1:** no unauthorised read found – BR5 ownership check is correct.

| # | Affected code | Finding (from tool) | Tool severity | My assessment | Evidence | Disposition |
|---|---|---|---|---|---|---|
| RF-1 | `tickets/service.py` – `return ticket` in `get_ticket_details` | Function returns the live stored object; a caller could change status/title/description and bypass BR1, BR2, BR4. | Blocking | **Agree it is a real design weakness, but I rate it Medium, not blocking for users.** End users cannot run Python; `app.py` only reads the returned object, so there is no UI path to exploit it. However, any future code calling this function could silently break BR1/BR2/BR4, and the fix is small. | Reproduced: changing `d.status` on the returned object changed the stored ticket. Fix: `return deepcopy(ticket)`. A frozen dataclass was rejected because `advance_status()` must update stored tickets. | **Fixed** |
| RF-2 | `tests/test_ticket_details.py` – same-error test | Test only checks both messages contain "not found", so two different messages could pass and leak existence. | Non-blocking | **Agree with the problem, but the suggested fix was wrong.** The tool suggested `assert str(other.value) == str(missing.value)`. I ran it: messages are `"Ticket #1 not found."` and `"Ticket #999 not found."` – they differ only by the requested ID, so this assert would always fail. | Test now asserts each message equals the exact template `f"Ticket #{id} not found."`, so any extra wording (e.g. "belongs to another user") fails the test. | **Fixed (with my own correction)** |
| RF-3 | `tests/test_ticket_details.py` – read-only test | No test proves the returned details cannot change stored data. | Blocking | Agree – this is the test that would have caught RF-1. | New `test_changing_returned_details_does_not_change_stored_ticket` changes 5 fields on the returned copy and checks the stored ticket is unchanged. **It fails on the old code and passes on the fix** (red → green). | **Fixed** |
| RF-4 | `tests/test_ticket_details.py` – invalid ID cases | Could add `False`, other non-int types, and a very large ID. | Non-blocking | Partly agree. `False` and `[]` are cheap to add; `10**100` checks an extreme value. `{}` and `object()` follow the exact same `isinstance` branch as `[]`, so they add no new coverage. | Added `False`, `[]` and `test_very_large_missing_id_returns_not_found`. | **Fixed (partly); `{}`/`object()` dismissed – same branch already covered** |

> Tool output is not approval. Each finding above was reproduced or checked by me before deciding.

## Out of scope (recorded, not fixed in this PR)
- `list_tickets()` (V1.0) also returns live stored objects – the same pattern as RF-1.
  It was **not introduced by this PR**, and changing it would widen the patch.
  Risk is the same (no UI exploit path). Raised as a follow-up issue: **(add issue number)**.

## Merge decision
**Decision: Ready to merge.**

**Reasons:**
- Both blocking findings (RF-1, RF-3) fixed and protected by a test shown to fail before the fix.
- RF-2 fixed after correcting the reviewer's faulty suggestion; RF-4 handled.
- CI passed on the PR: 42/42 tests (23 V1.0 regression tests unchanged + 19 CR-1 tests).
- BR1–BR4 behaviour unchanged (all V1.0 tests pass unmodified).
- I understand every changed line; AI use is disclosed in `docs/review_intake.md` and `docs/ai_usage_log.md`.
- No blocking issue remains open; the one related weakness outside this change is tracked separately.
