FROM python:3.10-slim

# Avoids Python buffering logs (useful for Cortex log visibility)
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /opt/analyzer

# Upgrade pip and install dependencies
COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove -y gcc \
    && apt-get autoremove -y && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the rest of the code
COPY . .

# Cortex will override this with the command in manifest.json, but good default
ENTRYPOINT ["python3", "NLP_Phishing_1_0.py"]
