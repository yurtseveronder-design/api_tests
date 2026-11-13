FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN useradd -m tester && mkdir -p reports && chown -R tester /app
USER tester

# Offline + public-API tests by default. For the ai-sentinel tests, run a gateway
# and pass SENTINEL_BASE_URL / SENTINEL_API_KEY (see README).
CMD ["python", "-m", "pytest", "-v", "--html=reports/report.html", "--self-contained-html"]
