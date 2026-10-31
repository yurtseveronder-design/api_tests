# API Test Automation Framework

A lightweight Python test automation framework built with `pytest` for validating REST APIs, request schemas, and basic endpoint behavior.

## What it does
* **Structured API Testing**: Uses `pytest` and custom fixtures (`conftest.py`) for clean test execution.
* **Schema Validation**: Checks response formats and data structures.
* **Containerized Setup**: Includes a `Dockerfile` for running tests in an isolated container.

## Getting Started

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt