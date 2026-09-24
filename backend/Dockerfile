# =========================
# Stage 1: Builder
# =========================
FROM python:3.12-slim AS builder

WORKDIR /app

# Create virtual environment
RUN python -m venv /opt/venv

# Use virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


# =========================
# Stage 2: Production
# =========================
FROM python:3.12-slim AS production

WORKDIR /app

# Copy only the virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Use virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Copy application
COPY main.py .

# Application port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]