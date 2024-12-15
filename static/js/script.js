// app.js

// Connect to the server
// const socket = io();
// Client-side code
const socket = io("http://192.168.2.71:5000/", {
    transports: ["websocket"], // Forceer WebSocket als transport
    secure: false,             // Zorg dat het geen HTTPS probeert
});

const fileInput = document.getElementById('fileInput');
const customButton = document.getElementById('uploadedFiles');

// Voeg een eventlistener toe aan de knop
customButton.addEventListener('click', () => {
  fileInput.click(); // Simuleer een klik op het verborgen input element
});

// Optioneel: Toon de geselecteerde bestandsnamen
fileInput.addEventListener('change', () => {
  const fileList = fileInput.files;
  if (fileList.length > 0) {
    alert(`Geselecteerde bestanden: ${Array.from(fileList).map(file => file.name).join(', ')}`);
  }
});


function SendMsg() {
    // const input = document.getElementById('chat-input');
    // const message = input.value;
    const input_user = document.getElementById('messageUser');
    const message = input_user.textContent.trim();

    const messagess = document.getElementById('messages');

    const element_message_user = document.createElement('li');
    element_message_user.classList.add('humanQuestion');
    element_message_user.innerHTML = message
    messagess.appendChild(element_message_user);
                // Stuur de invoerwaarde naar de server
    socket.emit('askLLM', { text: message });
    input_user.textContent = "";
}

function sentNamings(){
    const input_C = document.getElementById('collectionNaming');
    const collectionName = input_C.textContent.trim();

    const input_D = document.getElementById('dataBaseNaming');
    const databaseName = input_D.textContent.trim();

    socket.emit("setNamingVectorDB", {collection:collectionName, vectordb:databaseName});
    input_C.textContent = "";
    input_D.textContent = "";

}

function UploadFiles() {
    const files = document.getElementById('fileInput').files;
    if (files.length === 0) {
        alert("Selecteer minstens één bestand.");
        return;
    }
    for (const file of files) {
        const reader = new FileReader();

        // Lees het bestand als een arraybuffer of base64 string
        reader.onload = (event) => {
            socket.emit('upload_file', {
                fileName: file.name,
                fileData: event.target.result,
                fileType: file.type,
            });
        };
        reader.readAsArrayBuffer(file);
    }

    fileInput.value = '';
}

function LoadInDatabase(){
    const input_C = document.getElementById('collectionNaming');
    const collectionName = input_C.textContent.trim();

    const input_D = document.getElementById('dataBaseNaming');
    const databaseName = input_D.textContent.trim();

    input_C.textContent = "";
    input_D.textContent = "";
    socket.emit("LoadInVectorDB", {collection: collectionName, vectordb:databaseName})
}




socket.on('ReceivedRequest', (data) => {
    alert("FROM SERVER: " + data.message);
})

 socket.on('AwnserLLM', (data) => {
     const messages = document.getElementById('messages');
     const newMessage = document.createElement('li');
     newMessage.innerHTML = marked.parse(data.message)
     // Hier toepassen

     newMessage.classList.add('LLMresponds');
     messages.appendChild(newMessage);
 });

function addQuestionMessage(){
    const input = document.getElementById('messageUser');
    const message = input.textContent.trim();

    const messages = document.getElementById('messages');
    const newMessage = document.createElement('li');

    newMessage.innerHTML = marked.parse(data.message)
    newMessage.classList.add('humanQuestion');
    messages.appendChild(newMessage);
}

function setVectorDB(){
    const input_C = document.getElementById('collectionNaming');
    const collectionName = input_C.textContent.trim();

    const input_D = document.getElementById('dataBaseNaming');
    const databaseName = input_D.textContent.trim();

    socket.emit("ChangeVectorDBonCommand", {collection: collectionName, vectordb: databaseName})

    input_C.textContent = "";
    input_D.textContent = "";
}

socket.on('upload_status', (data) => {
            alert("FROM SERVER: "+data.message)
});