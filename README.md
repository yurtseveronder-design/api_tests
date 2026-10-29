\# Production-Grade API Automation Framework



An automated API test suite targeting JSONPlaceholder endpoints built using Python, pytest, and Requests.



\## Key Features

\- \*\*Modular Architecture\*\*: Clean separation of test cases, global fixtures (`conftest.py`), client helpers, and central configuration.

\- \*\*APIClient Abstraction\*\*: Encapsulated HTTP request wrapper methods (`GET`, `POST`, `PUT`, `DELETE`).

\- \*\*Data-Driven Testing\*\*: Parametrized negative tests validating error status codes (`404`).

\- \*\*Schema \& Type Validation\*\*: Strict assertions on JSON key presence and data types.

\- \*\*Reporting\*\*: Automated execution dashboard generation via `pytest-html`.



\## Project Structure

```text

api\_tests/

├── config.py            # Central configuration (BASE\_URL)

├── conftest.py          # Pytest fixtures \& APIClient injection

├── requirements.txt     # Dependency management file

├── .gitignore           # Git ignore rules

├── utils/

│   └── api\_client.py   # HTTP client wrapper class

└── tests/

&#x20;   └── test\_users.py    # Full CRUD \& schema test suite

