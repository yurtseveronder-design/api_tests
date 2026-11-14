# api_tests

A compact pytest framework for API testing: one HTTP client, strict Pydantic contracts, offline self-tests, and integration tests for the [ai-sentinel](https://github.com/yurtseveronder-design/ai-sentinel) gateway.

## Layout
| Path | Purpose |
| --- | --- |
| `framework/client.py` | The only HTTP client: timeouts, retries with backoff (idempotent methods only), bearer / basic / API-key auth, status assertions, logging |
| `framework/config.py` | Environment and gateway settings, all overridable via env vars |
| `schemas/` | Pydantic contracts (`jsonplaceholder.py`, `sentinel.py`); unknown fields are rejected |
| `schemas/petstore_generated.py` | Pydantic models generated from the Swagger Petstore spec (not used by tests yet) |
| `tests/unit/` | Offline tests of the client and schemas against a local stub server |
| `tests/jsonplaceholder/` | Contract, CRUD and negative tests against the public JSONPlaceholder API |
| `tests/semantic/` | Contract, auth and validation tests for the sentinel-semantic service |
| `tests/stack/` | End-to-end: client → sentinel-ui → ai-sentinel → sentinel-semantic |
| `scripts/stack.sh` | Starts / stops the whole stack for local runs and CI |
| `tests/sentinel/` | Health, auth, injection-blocking, payload-limit and rate-limit tests for the ai-sentinel gateway |

## Run
```bash
pip install -r requirements.txt

pytest -m unit            # offline, no network
pytest -m external        # public JSONPlaceholder API
pytest                    # everything (gateway tests skip if no gateway is running)
```

### ai-sentinel gateway tests
```bash
pip install -e /path/to/ai-sentinel
AI_SENTINEL_API_KEY=test-api-key uvicorn ai_sentinel.api.gateway:app &
SENTINEL_API_KEY=test-api-key pytest -m sentinel

# Rate-limit test exhausts the gateway's 50 req/min limit: restart the gateway, then
pytest -m rate_limit
```
Set `SENTINEL_REQUIRED=1` to fail instead of skip when the gateway is unreachable (CI does this).

### Whole stack (end to end)
```bash
git clone https://github.com/yurtseveronder-design/ai-sentinel .sut/ai-sentinel
git clone https://github.com/yurtseveronder-design/sentinel-semantic .sut/sentinel-semantic
git clone https://github.com/yurtseveronder-design/sentinel-ui .sut/sentinel-ui
pip install -e .sut/ai-sentinel -e .sut/sentinel-semantic fastapi uvicorn pydantic

scripts/stack.sh start            # semantic :8100, ai-sentinel :8000, sentinel-ui :8200
pytest -m "semantic or sentinel or stack"
scripts/stack.sh stop
```
Keys default to test values (`SEMANTIC_API_KEY`, `SENTINEL_API_KEY`, `UI_API_KEY`); override them with environment variables.

### Other environments
`pytest --env staging` reads `STAGING_BASE_URL` (likewise `prod` / `PROD_BASE_URL`); `--base-url URL` overrides directly. See `.env.example` for all settings.

### Reports
```bash
pytest --cov=framework --cov-report=term-missing
pytest --html=reports/report.html --self-contained-html
pytest --alluredir=reports/allure-results   # view with: allure serve reports/allure-results
```

### Docker
```bash
docker build -t api-tests .
docker run --rm api-tests                       # unit + public-API tests
docker run --rm --network host -e SENTINEL_API_KEY=test-api-key api-tests pytest -m sentinel
```

## CI
`.github/workflows/ci.yml` checks out and starts the ai-sentinel gateway, runs the whole suite with a 80% coverage gate on `framework/`, runs a Bandit security scan, runs the rate-limit test against a restarted gateway, uploads the HTML/Allure reports, and builds the Docker image and runs the unit tests inside it.
