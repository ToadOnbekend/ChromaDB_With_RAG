// app.js

// Connect to the server
const socket = io();


function SendMsg() {
    const input = document.getElementById('textInput');
    const message = input.value;
                // Stuur de invoerwaarde naar de server
    socket.emit('askLLM', { text: message });
        input.value = ''; // Leeg het tekstveld na het verzenden
}


function UploadFiles(){
            const files = document.getElementById('fileInput').files;

            if (files.length === 0) {
                alert("Selecteer minstens één bestand.");
                return;
            }

            // Itereer door elk bestand en verstuur het naar de server
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
                // if (uploadedFiles === files.length) {
                //      fileInput.value = ''; // Reset het inputveld

                reader.readAsArrayBuffer(file); // Lees het bestand als arraybuffer
            }
            fileInput.value = '';
            socket.emit("LoadInVectorDB", {message: 'Upload'})
}

socket.on('ReceivedRequest', (data) => {
    alert("FROM SERVER: " + data.message);
})

 socket.on('AwnserLLM', (data) => {
     const messages = document.getElementById('messages');
     const newMessage = document.createElement('li');
     newMessage.textContent = data.message;
     messages.appendChild(newMessage);
 });

socket.on('upload_status', (data) => {
            alert("FROM SERVER: "+data.message)

});