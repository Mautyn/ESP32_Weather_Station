from flask import Flask, request, jsonify, render_template_string, render_template
import psycopg2
from datetime import datetime

app = Flask(__name__)

# Połączenie z bazą – dostosuj dane logowania
def get_connection():
    return psycopg2.connect(
        dbname="Weather_Data",
        user="postgres",
        password="xKontakt0",
        host="localhost",   # lub IP serwera PostgreSQL
        port=5432
    )

@app.route('/')
def home():
    return '<h2>Serwer działa! Sprawdź dane pod /weather</h2>'

@app.route('/weather')
def weather():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT date, time, value FROM temperature ORDER BY date DESC, time DESC LIMIT 1")
    temp_row = cursor.fetchone()

    cursor.execute("SELECT date, time, value FROM humidity ORDER BY date DESC, time DESC LIMIT 1")
    hum_row = cursor.fetchone()

    cursor.execute("SELECT date, time, value FROM pressure ORDER BY date DESC, time DESC LIMIT 1")
    pres_row = cursor.fetchone()

    # Dodatkowo: dane do wykresów (30 ostatnich rekordów)
    cursor.execute("SELECT date, time, value FROM temperature ORDER BY date DESC, time DESC LIMIT 30")
    temp_data = cursor.fetchall()

    cursor.execute("SELECT date, time, value FROM humidity ORDER BY date DESC, time DESC LIMIT 30")
    hum_data = cursor.fetchall()

    cursor.execute("SELECT date, time, value FROM pressure ORDER BY date DESC, time DESC LIMIT 30")
    pres_data = cursor.fetchall()

    cursor.close()
    conn.close()

    temp_data.reverse()
    hum_data.reverse()
    pres_data.reverse()

    labels = [f"{row[0]} {row[1]}" for row in temp_data]
    temp_values = [row[2] for row in temp_data]
    hum_values = [row[2] for row in hum_data]
    pres_values = [row[2] for row in pres_data]

    return render_template("weather.html",
                           temp_row=temp_row,
                           hum_row=hum_row,
                           pres_row=pres_row,
                           labels=labels,
                           temp_values=temp_values,
                           hum_values=hum_values,
                           pres_values=pres_values)



# Endpoint API do odbierania danych (jak masz obecnie)
@app.route('/api/weather', methods=['POST'])
def receive_weather():
    data = request.get_json()
    temperature = data.get("temperature")
    humidity = data.get("humidity")
    pressure = data.get("pressure")

    now = datetime.now()
    date = now.date()
    time = now.time().replace(microsecond=0)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO temperature (date, value, time) VALUES (%s, %s, %s)", (date, temperature, time))
    cursor.execute("INSERT INTO humidity (date, value, time) VALUES (%s, %s, %s)", (date, humidity, time))
    cursor.execute("INSERT INTO pressure (date, value, time) VALUES (%s, %s, %s)", (date, pressure, time))

    conn.commit()
    cursor.close()
    conn.close()

    return "Dane zapisane", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
