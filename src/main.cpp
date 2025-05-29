#include <WiFi.h>
#include <HTTPClient.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <ArduinoJson.h>
#include "time.h"  // biblioteka do obsługi czasu

#define SEALEVELPRESSURE_HPA (1013.25)

const char* ssid = "PK.Internet";
const char* password = "";

const char* serverName = "http://127.0.0.1:5000//api/weather";

Adafruit_BME280 bme;

// Strefa czasowa, np. Polska (CET/CEST)
const char* ntpServer = "ntp1.tp.pl	";
const long gmtOffset_sec = 3600;  // +1 godzina dla CET
const int daylightOffset_sec = 3600; // +1 godzina na czas letni

void setup() {
  Serial.begin(115200);
  if (!bme.begin(0x76)) {
    Serial.println("Nie znaleziono czujnika BME280!");
    while (1);
  }

  WiFi.begin(ssid, password);
  Serial.print("Łączenie z WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nPołączono z WiFi!");

  // Synchronizacja czasu z NTP
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    // Pobierz aktualny czas
    struct tm timeinfo;
    if (!getLocalTime(&timeinfo)) {
      Serial.println("Błąd pobierania czasu");
      return;
    }

    char dateStr[11]; // YYYY-MM-DD + null
    char timeStr[9];  // HH:MM:SS + null

    strftime(dateStr, sizeof(dateStr), "%Y-%m-%d", &timeinfo);
    strftime(timeStr, sizeof(timeStr), "%H:%M:%S", &timeinfo);

    // Tworzymy JSON z pomiarami i czasem
    StaticJsonDocument<256> jsonDoc;
    jsonDoc["temperature"] = bme.readTemperature();
    jsonDoc["pressure"] = bme.readPressure() / 100.0F;
    jsonDoc["humidity"] = bme.readHumidity();
    jsonDoc["date"] = dateStr;
    jsonDoc["time"] = timeStr;

    String jsonData;
    serializeJson(jsonDoc, jsonData);

    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    int httpResponseCode = http.POST(jsonData);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Odpowiedź serwera: " + response);
    } else {
      Serial.println("Błąd podczas wysyłania POST: " + String(httpResponseCode));
    }

    http.end();
  } else {
    Serial.println("Brak połączenia z WiFi");
  }

  delay(60000);  // Wysyłaj co 60 sekund
}
