from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from moduleToolCalling import questionRAG
import os
app = Flask(__name__)
socketio = SocketIO(app)

# TODO: OPEN IN "http://localhost:5000/"

@app.route('/')
def index():
    return render_template('index.html')  # Serve the frontend


@socketio.on('askLLM')
def give_awnser(data):
    socketio.emit('ReceivedRequest', {'message': f"Received prompt {data['text']}"})
    awnserLLM = questionRAG(data['text'])
    socketio.emit('AwnserLLM', {'message': f'{awnserLLM}'})

@socketio.on('upload_file')
def handle_file(data):
    file_name = data['fileName']
    file_data = data['fileData']

    # Bestand opslaan in de uploads map
    file_path = os.path.join("tempTestUpload", file_name)
    with open(file_path, 'wb') as f:
        f.write(bytearray(file_data))

    # Verstuur een bevestiging terug naar de client
    socketio.emit('upload_status', {'message': f"Bestand {file_name} succesvol geüpload!"})

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
