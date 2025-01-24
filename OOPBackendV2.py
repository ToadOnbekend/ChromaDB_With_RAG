from flask import Flask, render_template
from flask_socketio import SocketIO, emit

import classLLMv2
import moduleLoadInChromaDB
import classQuery
import classDatabase
import os



app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# TODO: OPEN IN "http://localhost:5000/"

# TODO: Vergeet NIET. Dit moet in juiste class komen. Dit is tijdelijk

FOLDERPdf = "tempTestUpload"
agent = ""
DataBase = ""
VECTOR_DATABASE_FOLDER = "VectorDBStoreFolder"
@app.route('/')
def index():
    return render_template('index.html')  # Serve the frontend


@socketio.on('askLLM')
def give_awnser(data):
    socketio.emit('AwnserSystem', {'message': f"Received prompt {data['text']}"})
    awnserLLM = agent.handle_input(data['text'])
    # awnserLLM = "wfeferofjerfjgiwoerjgoeiprgoiergjoirgeriogjperogjewrpiogjweir"
    # output = ollama.generate(
    #     model="llama3.1:8b",
    #     prompt=f"Geef uitgebreid antwoord op de prompt:\n{data['text']}",
    #     options={'temperature': 0.5}
    #     ## PAS de willekeurigheid van model aan. Tussen 0.1 en 1.  0.1, consistent en 1 creatief, minder consistent.
    # )
    # awnserLLM = output["response"]
    # awnserLLM = "# TEST: Er si eiojwefijewrgfiwergpierughpuierghiuerhqpowekfwoekfpwoefwefiwei[fjwofijwefgperuighuieorghuioerhgiuwerhgerwiuoghwieruhguiewrhguiewrhg"
    socketio.emit('AwnserLLM', {'message': f'{awnserLLM}'})

@socketio.on('upload_file')
def handle_file(data, callback = None):
    file_name = data['fileName']
    file_data = data['fileData']


    file_path = os.path.join(FOLDERPdf, file_name)
    with open(file_path, 'wb') as f:
        f.write(bytearray(file_data))

    socketio.emit('AwnserSystem', {'message': f"Bestand **{file_name}** succesvol geüpload!"})

def remove_files():
    try:
        for filename in os.listdir(FOLDERPdf):
            file_path = os.path.join(FOLDERPdf, filename)
            os.remove(file_path)
            print(f"Bestand verwijderd: {file_path}")
    except:
        print("ERROR Removing FILES ------- ")

@socketio.on("ChangeVectorDBonCommand")
def changeVectorDB(data):

    NAME_VectorDB = data["name"]
    chats = agent.SETUP(NAME_VectorDB)
    socketio.emit("AwnserSystem", {"message": f"Changed chatID and collection<br>ChatID: **{NAME_VectorDB}**\nCollection"})
    socketio.emit("LoadinComming", {"message": chats})

@socketio.on("LoadInVectorDB")
def LoadPDF_TO_VectorDB(data):
    try:
        agent.createNewChatIndex(data["nameChat"], data["collection"])
        agent.makeVectorDB()
        socketio.emit("AwnserSystem",
                      {"message": f"Changed chatID and collection<br>ChatID: **{data["nameChat"]}**\nCollection"})
        remove_files()
        socketio.emit("AwnserSystem", {"message": f"**Successfully** {data}"})

    except:
        remove_files()
        socketio.emit("AwnserSystem", {"message": "**Failed**"})

@socketio.on("goGetChatNames")
def GetChatNames():
    chat_names = agent.retriveChatCollections("")
    print(chat_names)
    socketio.emit("getChatNames", {"chatNames": chat_names["name"], "models": chat_names["model"],"collections": chat_names["collection"], "modelr":chat_names["modelreranking"], "modele": chat_names["modelembeding"], "dimensionsd":chat_names["embeddingdemensions"], "topn": chat_names["topnresults"], "nquery": chat_names["nqueryresults"], "chunkoverlap": chat_names["chunkoverlap"], "chunksize": chat_names["chunksize"], "datecreated": chat_names["datacreated"]})

if __name__ == '__main__':
    agent = classLLMv2.LLMAgent()
    database = classDatabase.StorageManager("chatIndex")
    vectordb = classQuery.QueryEngine()

    agent.initialize(vectordb, database, moduleLoadInChromaDB)
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, host="0.0.0.0", port=5000)
