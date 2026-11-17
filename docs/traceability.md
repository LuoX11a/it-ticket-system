# Requirements → Tests Traceability (V1.0)

All tests are in `tests/test_service.py`. Expected results are taken from
`requirements.md`, not from the implementation.

| Requirement / Rule | Test(s) | Test type | Risk controlled |
|---|---|---|---|
| FR1 | `test_employee_creates_ticket` | Happy path | – |
| FR1 | `test_invalid_category_rejected` | Invalid input (caller-controlled) | Tampered input |
| FR1 / roles | `test_it_cannot_create_ticket` | Permission | – |
| FR2, BR3 | `test_employee_sees_only_own_tickets` | Permission / data access | Data leakage |
| FR3 | `test_it_sees_all_tickets` | Happy path | – |
| BR1 | `test_new_to_in_progress`, `test_in_progress_to_resolved_with_note` | State transition | – |
| BR1 | `test_resolved_ticket_cannot_advance` | Expected failure | Backward / repeated change |
| BR2, QR3 | `test_employee_cannot_change_status` | Unauthorised access | R1 |
| QR3 | `test_unknown_role_rejected` (admin, IT, "", None) | Unauthorised access | R1, R3 |
| BR4 | `test_title_length_boundaries` (4 ✗, 5 ✓, 100 ✓, 101 ✗) | Boundary values | Bad data |
| BR4 | `test_whitespace_only_title_rejected`, `test_title_is_trimmed_before_length_check` | Invalid input | Blank titles |
| BR4 | `test_description_too_long_rejected` | Boundary | Bad data |
| FR4 | `test_resolve_without_note_rejected` | Expected failure | Incomplete records |
| QR1 | `test_ticket_not_found`, `test_empty_username_rejected` | Failure handling | App crash |
| BR1/BR2/BR4 protection (RF-1) | `test_changing_returned_details_does_not_change_stored_ticket` | Encapsulation / regression | Rule bypass |
| Caller input (RF-4) | `test_very_large_missing_id_returns_not_found` | Extreme value | Crash / wrong error |

**Verification check:** every FR, BR and QR above has at least one test (QR2 satisfied).
