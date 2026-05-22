FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel && \
    pip install numpy==1.26.4 && \
    pip install scikit-surprise==1.1.3 --no-build-isolation && \
    pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app1.py"]
