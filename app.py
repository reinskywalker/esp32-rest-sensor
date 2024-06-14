from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>ESP32 Flask Test</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                html { font-family: sans-serif; text-align: center; }
                body { display: inline-flex; flex-direction: column; align-items: center; }
                h1 { margin-bottom: 1.2em; }
                div { display: flex; flex-direction: column; align-items: center; margin-top: 20px; }
                input, .btn { font-size: 1.5em; margin: 10px; padding: 0.25em; }
                .btn { background-color: #4CAF50; border: none; color: white; padding: 15px 32px; text-align: center; }
                .btn:hover { background-color: #45a049; }
            </style>
        </head>
        <body>
            <h1>ESP32 Flask Server</h1>
            <div>
                <form id="dataForm">
                    <input type="text" id="temperature" placeholder="Enter temperature" required>
                    <input type="text" id="humidity" placeholder="Enter humidity" required>
                    <input type="submit" value="Submit" class="btn">
                </form>
            </div>
            <script>
                document.getElementById('dataForm').onsubmit = function(event) {
                    event.preventDefault();
                    var temperature = document.getElementById('temperature').value;
                    var humidity = document.getElementById('humidity').value;

                    fetch('/data', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ 'temperature': temperature, 'humidity': humidity })
                    })
                    .then(response => response.json())
                    .then(data => {
                        alert('Data sent: ' + JSON.stringify(data));
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('Failed to send data');
                    });
                };
            </script>
        </body>
    </html>
    """
    return html_content

@app.route('/data', methods=['POST'])
def sensor_data():
    data = request.get_json(force=True)  
    temperature = data.get('temperature')
    humidity = data.get('humidity')

    print(f"Received temperature: {temperature}°C, humidity: {humidity}%")

    response = {
        "message": "Data received successfully",
        "temperature": temperature,
        "humidity": humidity
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
