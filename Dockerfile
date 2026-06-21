FROM python:3.12-slim

WORKDIR /app

# Install deps first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app/ ./app/

# Run as non-root
RUN useradd -r -u 1000 appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

# Health endpoints so Kubernetes can probe
HEALTHCHECK --interval=10s --timeout=2s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/healthz')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
