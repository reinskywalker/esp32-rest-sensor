#include <WiFi.h>
#include <HTTPClient.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

#define WIFI_SSID "Wokwi-GUEST"
#define WIFI_PASSWORD ""

#define SERVER_URL "http://127.0.0.1:5000/data"

#define DHTPIN 4
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  connectToWiFi();
  dht.begin();
}

void loop() {
  static unsigned long lastMeasurementTime = 0;
  if (millis() - lastMeasurementTime > 2000) {
    lastMeasurementTime = millis();
    if (WiFi.status() != WL_CONNECTED) {
      connectToWiFi();
    }
    sendSensorData();
  }
}

void connectToWiFi() {
  int retryCount = 0;
  while (WiFi.status() != WL_CONNECTED && retryCount < 10) {
    delay(500);
    Serial.print(".");
    retryCount++;
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("Connected to WiFi");
  } else {
    Serial.println("Failed to connect to WiFi");
  }
}

void sendSensorData() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi is not connected!");
    return;
  }

  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  HTTPClient http;
  http.begin(SERVER_URL);
  http.addHeader("Content-Type", "application/json");

  String postData = "{\"temperature\": " + String(temperature) + ", \"humidity\": " + String(humidity) + "}";
  int httpResponseCode = http.POST(postData);

  if (httpResponseCode > 0) {
  String response = http.getString();
  Serial.println("Response code: " + String(httpResponseCode));
  Serial.println("Response: " + response);
} else {
  Serial.println("Error on sending POST: " + String(httpResponseCode));
  Serial.println("HTTP error: " + http.errorToString(httpResponseCode));
}

  http.end();
}