# Wybieramy obraz Pythona 3.10
FROM python:3.10

# Ustawiamy katalog roboczy w kontenerze
WORKDIR /app

# Kopiujemy plik requirements.txt do kontenera
COPY requirements.txt /app/

# Instalujemy zależności (FastAPI i Uvicorn)
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy resztę plików z katalogu roboczego na komputerze do kontenera
COPY . /app/

# Ustawiamy domyślną komendę do uruchomienia aplikacji FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
