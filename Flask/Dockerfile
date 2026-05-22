FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install numpy==1.26.4 && \
    pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app1.py"]
