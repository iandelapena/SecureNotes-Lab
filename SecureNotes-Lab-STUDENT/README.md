# SecureNotes API — Combined Lab (Student Starter)

One lab, two halves:
- **Part A** — make the app's security real (JWT auth + authorization).
- **Part B** — write the tests that prove Part A works and won't silently break.

## Setup
```bash
python -m venv venv
# Windows:  venv\Scripts\activate   ·   macOS/Linux:  source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload     # run the API with JWT and bcrypt security
pytest -q                         # run the 11 security and API tests
```
Open http://127.0.0.1:8000/docs. Accounts: `admin/admin123`, `alice/alicepass` (note 1), `bob/bobpass` (note 2).

> **Keep the bcrypt pin.** `requirements.txt` pins `bcrypt==4.0.1` — newer bcrypt breaks passlib.

## What you edit
- **Part A:** `app/main.py`, only inside the `>>> TASK n ... <<< END TASK n` markers.
- **Part B:** `tests/test_api.py` and `tests/test_security.py` — the suite proves the required
  authentication, authorization, ownership, and password-hash protections.
  (`tests/conftest.py` gives you the `client` fixture and `login` / `auth` helpers.)

**The payoff:** the tests in Part B are executable proof that the authentication and authorization
rules remain enforced. See the handout and `TASKS.md`.

## Part C — peer review on GitHub
The required peer review and LMS submission links must be completed separately. Do not mark the
peer review complete until a classmate's pull request has been reviewed with comments and an
Approve or Request changes verdict.
