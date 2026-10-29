!\[API Test Suite CI](https://github.com/yurtseveronder-design/api\_tests/actions/workflows/tests.yml/badge.svg)



\# Production-Grade API Automation Framework



A modular, enterprise-ready API test automation framework built with \*\*Python\*\*, \*\*Pytest\*\*, and \*\*Requests\*\*, integrated with continuous integration via \*\*GitHub Actions\*\* and containerized with \*\*Docker\*\*.



\---



\## 🛠️ Key Features



\- \*\*Modular Architecture\*\*: Clean separation of test cases (`tests/`), API client wrappers (`utils/`), dynamic environment setup (`conftest.py`), and target settings.

\- \*\*Full CRUD \& Schema Assertions\*\*: Validates `GET`, `POST`, `PUT`, `DELETE` operations and validates response contracts and JSON types.

\- \*\*Multi-Environment Support\*\*: Switch target environments dynamically using pytest CLI flags (`--env=dev|staging|prod`).

\- \*\*CI/CD Pipeline\*\*: GitHub Actions workflows run tests automatically on push/PR and archive HTML execution reports as build artifacts.

\- \*\*Docker Ready\*\*: Fully containerized for instant execution in any environment.



\---



\## 🚀 Quick Start (Local Setup)



1\. \*\*Clone the repository\*\*:

&#x20;  ```bash

&#x20;  git clone \[https://github.com/yurtseveronder-design/api\_tests.git](https://github.com/yurtseveronder-design/api\_tests.git)

&#x20;  cd api\_tests

