# ESP32_Weather_Station

Stacja pogodowa odczytująca temperaturę, ciśnienie oraz wilgotność

## Wymagania

- VSCode
- Rozszerzenie PlatformIO
- Python
- PostgreSQL

## Instalacja

### Mac

Dla kodu pythona trzeba zainstalować biblioteki flask oraz psycopg2-binary, pip3 można zainstalować przez brew. pip3 należy uruchomić by móc korzystać z bibliotek pythona załączonych do projektu

```sh
python3 -m venv venv
source venv/bin/activate
pip3 install flask psycopg2-binary
```

Bazę PostgreSQL można postawić np. na dockerze

```sh
docker run --name weather_db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=your_password -e POSTGRES_DB=Weather_Data -p 5432:5432  -d postgres:latest
```

W projekcie ustawione wartości dla bazy to:
user_name: `postgres`
password: `your_password`
postgres_db: `Weather_Data`
port: `5432`

## Uruchomienie

Na samym początku należy zbudować oraz wgrać program dla płytki na samą płytkę w VSCode. Następnie należy uruchomić bazę danych do zapisu odczytywanych wartości do bazy.  Kolejnym krokiem jest uruchomienie kodu pythona dla wyświetlenia wyników z bazy danych poprzez przeglądarkę (localhost:5000)
