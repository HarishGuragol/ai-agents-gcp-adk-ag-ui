FROM python:3.12-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy EVERYTHING from current folder (backend/)
COPY . .

# Install Python deps
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    pydantic \
    google-adk

ENV PORT=8080

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8080"]

