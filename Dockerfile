# Użyj oficjalnego obrazu Pythona jako obrazu bazowego
FROM python:3.8-slim

# Ustaw katalog roboczy w kontenerze
WORKDIR /app

# Skopiuj plik requirements.txt do kontenera
COPY requirements.txt /app/requirements.txt

# Zainstaluj zależności
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj resztę kodu źródłowego aplikacji do kontenera
COPY . /app

# Ustaw zmienną środowiskową wskazującą na plik, który ma być uruchomiony
ENV FLASK_APP=app.py

# Informuj Docker, że kontener nasłuchuje na określonym porcie
EXPOSE 5000

# Uruchom aplikację
CMD ["flask", "run", "--host=0.0.0.0"]
