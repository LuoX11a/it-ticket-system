# IT Service Request Ticketing System

A small Streamlit app where **employees** submit IT support tickets and **IT Support** staff
process them through a controlled workflow (`New → In Progress → Resolved`).
Built for CP5401 Assessment 3 to demonstrate software quality engineering.

- **Live app:** _add Streamlit URL here_
- **Releases:** _add V1.0 / V1.1 links here_
- **Requirements:** [requirements.md](requirements.md)
- **Traceability:** [docs/traceability.md](docs/traceability.md)

## Architecture
```
app.py               Streamlit UI only (display + input)
tickets/service.py   Business rules + permission checks (tested)
tickets/storage.py   In-memory storage
tickets/models.py    Ticket data model
tests/               pytest test suite (regression suite)
```

## Run locally
```bash
pip install -r requirements.txt
pytest -v
streamlit run app.py
```

## Quality checks
GitHub Actions (`.github/workflows/quality-checks.yml`) runs the full test suite on every
push and pull request to `main`.

## Known limitations
- Simulated login (no real authentication) – risk R3.
- In-memory storage; data resets when the app restarts – risk R2.
