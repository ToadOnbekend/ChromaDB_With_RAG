// app.js

// Connect to the server
// const socket = io();
// Client-side code
/*
TODO
TODO Ga naar [LAN]  : http://192.168.2.71:5000/ 
TODO Ga naar [WiFi] : http://192.168.2.69:5000/
TODO
 */

current_chat = "D99F1A1A-1D1A-4D1A-9D1A-1D1A1D1A1D1A"
addedmodel= []
addedmodelR = []
addedmodelE = []
collections = []

const socket = io("http://192.168.2.69:5000/", {
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

function userMSG(data){
     const messagess = document.getElementById('messages');
    const element_message_user = document.createElement('li');
    element_message_user.classList.add('humanQuestion');
    element_message_user.innerHTML = data
    messagess.appendChild(element_message_user);

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
    socket.emit("LoadInVectorDB", {collection: collectionName, nameChat:databaseName})


}



function llmawnserMSG(data){
         const messages = document.getElementById('messages');
     const newMessage = document.createElement('li');
     newMessage.innerHTML = marked.parse(data)
     // Hier toepassen

     newMessage.classList.add('LLMresponds');
     messages.appendChild(newMessage);
}
socket.on('ReceivedRequest', (data) => {
    alert("FROM SERVER: " + data.message);
})

 socket.on('AwnserLLM', (data) => {
  llmawnserMSG(data.message);
 });

function getCnames(data,idE){
      const messages = document.getElementById('chatsL');
         const newMessage = document.createElement('li');
         const button = document.createElement('button')
              button.textContent = data
              button.addEventListener('click', () => {
                  setVectorDB_button(data,idE); // Roep de functie aan bij klikken

              });

              // newMessage.classList.add('system');
              newMessage.appendChild(button);
              messages.appendChild(newMessage);
}


 socket.on('AwnserSystem', (data) => {
     const messages = document.getElementById('messages');
     const newMessage = document.createElement('li');
     newMessage.innerHTML = marked.parse(data.message)
     // Hier toepassen

     newMessage.classList.add('system');
     messages.appendChild(newMessage);
 });



 socket.on("getChatNames", (data) => {

    for (let i = 0; i < data.chatNames.length; i++) {
         getCnames(data.chatNames[i])

         m = data.models[i]
         if (!addedmodel.includes(m)){
             addedmodel.push(m)
             addOptionToDropdown(m, "dropdown1");


         }
         v = data.modele[i]
         if (!addedmodelE.includes(v)){
             addedmodelE.push(v)
             addOptionToDropdown(v, "dropdown2");
         }
         r = data.modelr[i]
            if (!addedmodelR.includes(r)){
                addedmodelR.push(r)
                addOptionToDropdown(r, "dropdown3");
            }


    }

 })

  socket.on("LoadinComming", (data) => {
    data = data.message
    for (let i = 0; i < data.sendInfo.length; i++) {
        let v = data.messages[i]
        if (v.role == "assistant"){
            llmawnserMSG(v.content);
        } else if (v.role == "user") {
            userMSG(v.content);
        }

    }
    scrollOnNewMSG();


 })



socket.emit('goGetChatNames');


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

    socket.emit("ChangeVectorDBonCommand", { name: databaseName})

    input_C.textContent = "";
    input_D.textContent = "";
}

function setVectorDB_button(ch){
    if (ch != current_chat) {
        const input_C = document.getElementById('collectionNaming');
        const collectionName = input_C.textContent.trim();

        const input_D = document.getElementById('dataBaseNaming');
        const databaseName = input_D.textContent.trim();
        const messages = document.getElementById('messages');
        messages.innerHTML = ''; // Verwijdert alle <li>-elementen binnen de lijst

        socket.emit("ChangeVectorDBonCommand", {name: ch})
        current_chat = ch;
        input_C.textContent = "";
        input_D.textContent = "";
    }
}
socket.on('upload_status', (data) => {
            alert("FROM SERVER: "+data.message)
});

function scrollOnNewMSG(){
    const messagesContainer = document.getElementById('messages');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function sideBar() {
    const sidebar = document.getElementById('sidebar');
    const content = document.getElementById('content');
    const toggleButton = document.getElementById('toggleButton');


    const isHidden = sidebar.classList.toggle('hidden');
    content.classList.toggle('hidden', isHidden);
    toggleButton.textContent = isHidden ? '⮞' : '⮜';
}


// Dropdown menu
// document.getElementById('modelpicker').addEventListener('focus', () => {
//     document.getElementById('dropdownOptions').classList.remove('hidden');
// });
//
// document.getElementById('modelpicker').addEventListener('blur', () => {
//     setTimeout(() => { // Tijdelijke vertraging om klikken op opties mogelijk te maken
//         document.getElementById('dropdownOptions').classList.add('hidden');
//     }, 200);
// });
//
// // Filter opties op basis van input
// function filterOptions() {
//     const input = document.getElementById('modelpicker').value.toLowerCase();
//     const options = document.querySelectorAll('#dropdownOptions li');
//     options.forEach(option => {
//         if (option.textContent.toLowerCase().includes(input)) {
//             option.style.display = 'block';
//         } else {
//             option.style.display = 'none';
//         }
//     });
// }
//
// // Kies een optie en vul deze in het inputveld
// function selectOption(element) {
//     document.getElementById("modelpicker").value = element.textContent;
//     document.getElementById('dropdownOptions').classList.add('hidden');
// }

function addOptionToDropdown(optionText, dropdownId) {
    const dropdown = document.getElementById(dropdownId);
    if (dropdown) {
        const newOption = document.createElement('li');
        newOption.textContent = optionText; // Stel de tekst van de nieuwe optie in
        newOption.addEventListener('click', () => {
            selectOption(newOption); // Koppel de `selectOption`-functie
        });
        dropdown.appendChild(newOption); // Voeg de optie toe aan de dropdown
    } else {
        console.error(`Dropdown met ID '${dropdownId}' niet gevonden.`);
    }
}

 document.querySelectorAll('.modelpicker').forEach(picker => {
        picker.addEventListener('focus', () => {
            const dropdownId = picker.dataset.dropdown;
            if (dropdownId) {
                document.getElementById(dropdownId).classList.remove('hidden');
            }
        });

        picker.addEventListener('blur', () => {
            const dropdownId = picker.dataset.dropdown;
            if (dropdownId) {
                setTimeout(() => { // Tijdelijke vertraging om klikken op opties mogelijk te maken
                    document.getElementById(dropdownId).classList.add('hidden');
                }, 200);
            }
        });

        picker.addEventListener('input', () => {
            const dropdownId = picker.dataset.dropdown;
            if (dropdownId) {
                filterOptions(picker, dropdownId);
            }
        });
    });

    // Voeg event listeners toe aan dropdown opties
document.querySelectorAll('.dropdownOptions').forEach(dropdown => {
    dropdown.addEventListener('click', (event) => {
        if (event.target.tagName === 'LI') {
            selectOption(event.target);
        }
    });
});

// Filter opties op basis van input
function filterOptions(inputElement, dropdownId) {
    const input = inputElement.value.toLowerCase();
    const options = document.querySelectorAll(`#${dropdownId} li`);
    options.forEach(option => {
        if (option.textContent.toLowerCase().includes(input)) {
            option.style.display = 'block';
        } else {
            option.style.display = 'none';
        }
    });
}

// Kies een optie en vul deze in het inputveld
function selectOption(element) {
    const pickerId = element.closest('.dropdownOptions').dataset.picker;
    if (pickerId) {
        document.getElementById(pickerId).value = element.textContent;
    }
    element.closest('.dropdownOptions').classList.add('hidden');
}



// Dynamisch toevoegen van opties

// function showModels() {
//     const input = document.getElementById('chatName');
//     input.setAttribute('list', 'chatNames');
// }