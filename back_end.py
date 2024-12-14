from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from moduleToolCalling import questionRAG
from moduleLoadInChromaDB import loadPDFVectorDB
from module_ChromaDB_Ask import initializeModelAndDatabase
import os
import shutil
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# TODO: OPEN IN "http://localhost:5000/"

# TODO: Vergeet NIET. Dit moet in juiste class komen. Dit is tijdelijk
# TODO: Hij moet bestanden wegooien
FOLDERPdf = "tempTestUpload"
VECTOR_DATABASE_FOLDER = "VectorDBStoreFolder"
NAME_VectorDB = "Tt1"
NAME_Collection = "STO"
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
    file_path = os.path.join(FOLDERPdf, file_name)
    with open(file_path, 'wb') as f:
        f.write(bytearray(file_data))

    # Verstuur een bevestiging terug naar de client
    socketio.emit('upload_status', {'message': f"Bestand {file_name} succesvol geüpload!"})

def setName_c_d(data):
    global NAME_VectorDB, NAME_Collection
    print("HIER -------------\n HIER\n----------")
    NAME_Collection = data["collection"]
    NAME_VectorDB = data["vectordb"]
    socketio.emit('ReceivedRequest', {"message": f"\nChanged database name to {NAME_VectorDB}\nChanged collection name to {NAME_Collection}  "})

@socketio.on("LoadInVectorDB")
def LoadPDF_TO_VectorDB(data):
    setName_c_d(data)

    socketio.emit('ReceivedRequest', {"message": f'ProcessingFiles\nCol {NAME_Collection}\nVec {NAME_VectorDB}'})
    try:
        loadPDFVectorDB(NAME_VectorDB, NAME_Collection, FOLDERPdf)
        socketio.emit("ReceivedRequest", {"message":"Succeed! Now initializing Retriever Module'"})
        try:
            initializeModelAndDatabase(VECTOR_DATABASE_FOLDER+"\\"+NAME_VectorDB, NAME_Collection)
            socketio.emit("ReceivedRequest", {"message": "inintialized!"})

        except:
            socketio.emit("ReceivedRequest", {"message": "Failed at initializing Retriever Module"})

    except:
        socketio.emit("ReceivedRequest", {"message": "Failed"})

    finally:
        for filename in os.listdir(FOLDERPdf):
            file_path = os.path.join(FOLDERPdf, filename)
            os.remove(file_path)
            print(f"Bestand verwijderd: {file_path}")

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, host="0.0.0.0", port=5000)
