FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

# Zainstaluj libpq-dev i inne wymagane pakiety
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*  # Oczyść po instalacji

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt  # Zainstaluj wymagane pakiety

COPY . .

# Run the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]