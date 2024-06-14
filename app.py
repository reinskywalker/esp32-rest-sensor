from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

@app.route('/')
def index():
    htmlContent = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>ESP32 Flask Test</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                html { font-family: sans-serif; text-align: center; }
                body { display: inline-flex; flex-direction: column; }
                h1 { margin-bottom: 1.2em; }
                h2 { margin: 0; }
                div { display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: auto auto; grid-auto-flow: column; grid-gap: 1em; }
                .btn { background-color: #5B5; border: none; color: #fff; padding: 0.5em 1em;
                       font-size: 2em; text-decoration: none }
                .btn.OFF { background-color: #333; }
                input[type='text'], input[type='submit'] {
                    font-size: 1.5em; margin: 0.5em; padding: 0.25em;
                }
            </style>
        </head>
        
        <body>
            <h1>ESP32 Flask Server</h1>

            <div>
                <h2>Temperature and Humidity</h2>
                <form id="dataForm">
                    <input type="text" id="temperature" placeholder="Enter temperature" required>
                    <input type="text" id="humidity" placeholder="Enter humidity" required>
                    <br>
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
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            'temperature': temperature,
                            'humidity': humidity
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log('Success:', data);
                        alert('Data sent: ' + JSON.stringify(data));
                    })
                    .catch((error) => {
                        console.error('Error:', error);
                    });
                };
            </script>
        </body>
    </html>
    """
    return htmlContent

@app.route('/data', methods=['POST'])
def sensor_data():
    data = request.get_json()
    t = data.get('temperature')
    h = data.get('humidity')

    print(f"Received temperature: {t}°C, humidity: {h}%")

    res = {
        "message": "Data received successfully",
        "temperature": t,
        "humidity": h
    }

    return jsonify(res), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)