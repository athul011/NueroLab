
FROM python:3.11.9-slim-bullseye

WORKDIR /app


RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .


RUN pip install --no-cache-dir --upgrade pip==24.0 && \
    pip install --no-cache-dir -r requirements.txt


COPY . .


RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser


EXPOSE 8000


HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/docs')" || exit 1


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
