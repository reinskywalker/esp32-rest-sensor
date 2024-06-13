from flask import Flask, request, jsonify
from datetime import datetime
from os import environ
import logging

logging.basicConfig(level=logging.DEBUG) # set debug

app = Flask(__name__)

@app.route('/') # base route
def getTime():
    now = datetime.now()
    fTime = now.strftime("%d %b %Y %H %M %S")

    return f"Time : {fTime}"

@app.route('/sensor-data', methods=['POST'])
def sensorData():
    try:
        data = request.get_json()
        temperature = data.get('temperature')
        humidity = data.get('humidity')

        if temperature is None or humidity is None:
            raise ValueError("Missing temperature or humidity in the received data")

        logging.info(f"Received temperature: {temperature}°C, humidity: {humidity}%")

        response = {
            "message": "Data received successfully",
            "temperature": temperature,
            "humidity": humidity
        }

        logging.info(f"Sending response: {response}")

        return jsonify(response), 200
    except ValueError as e:
        logging.error(str(e))
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error("An error occurred: " + str(e))
        return jsonify({"error": "An error occurred while processing the data"}), 500

if __name__ == '__main__':
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
