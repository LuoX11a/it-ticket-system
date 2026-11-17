# Generative AI Usage Log

| Date | Tool | What I asked | What it produced | How I checked / changed it |
|---|---|---|---|---|
| 17-11-2026 | Microsoft Copilot | Suggest project ideas and plan for Assessment 3 | Requirements draft, presentation outline | Chose idea; edited requirements to my scope |
| 17-11-2026 | Microsoft Copilot | Generate V1.0 code, tests, workflow and docs | `tickets/*.py`, `app.py`, `tests/test_service.py`, workflow, docs | Read every file; ran `pytest` locally; ran the app and tried each FR manually; checked each test's expected result against `requirements.md` |
| 17-11-2026 | Microsoft Copilot | Implement CR-1 from user feedback: detail view, BR5 check, tests, UI layout | get_ticket_details(), tests/test_ticket_details.py, app.py changes, docs | Read diff line by line; checked test expectations against FR5/BR5; ran 38 tests; manually tested role switch, long resolution and bob/alice access |


## Files mainly AI-generated
- V1.0: tickets/*.py, app.py, tests/test_service.py, workflow, docs – AI-generated, reviewed and tested by me - V1.1: get_ticket_details() in tickets/service.py, tests/test_ticket_details.py, app.py layout – AI-generated, reviewed and tested by me