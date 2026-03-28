
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first (separate from source code for better layer caching)

COPY requirements.txt .

# Install dependencies — no cache dir keeps the image smaller
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the source code
COPY . .

# Install the app itself so the 'secure' CLI command is available
RUN pip install --no-cache-dir .

# Declare the env var — value is supplied at runtime, never hardcoded here
ENV MISTRAL_API_KEY=""

# Create and switch to a non-root user — good security practice
RUN useradd --create-home appuser
USER appuser

# The container IS the 'secure' command
# Default behaviour (no args): print help
ENTRYPOINT ["secure"]
CMD ["--help"]
