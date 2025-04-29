FROM python:3.12-slim

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg build-essential libsndfile1 curl git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install PyTorch CPU-only build
RUN pip install --no-cache-dir torch==2.3.1+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html

# Install the rest of the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8001

# Run app
CMD ["python", "asr_api.py"]