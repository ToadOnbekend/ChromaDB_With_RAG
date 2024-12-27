from ollama import chat
from ollama import ChatResponse
from datetime import datetime
import ast


class LLMAgent:
    model = ""
    mappings = {"system": "1",
                "assistant": "2",
                "user": "3",
                "tool": "4"} #omgeerkde van mappings-database
    use_tool = True
    memory_chat = []
    askAboutFiles_tool = {
        'type': 'function',
        'function': {
            'name': 'query',
            'description': "Gebruik deze functie ALTIJD, ongeacht de prompt van de gebruiker",
            # 'Deze functie geeft de benodigde externe informatie om de vraag te beantwoorden',
            'parameters': {
                'type': 'object',
                'required': ['query_questions', 'questions_user'],
                'properties': {
                    'query_questions': {'type': 'list',
                                        'description': 'Bedenk de benodigde zoekzinnen om de juiste gegevens te krijgen voor het beantwoorden van de vraag(vragen) uit de prompt', "items": { "type": "string" }},
                    'questions_user': {'type': 'list',
                                       'description': 'Geef de vraag(vragen) van de gebruiker die in de pompt staat',  "items": { "type": "string" }},
                },
            },
        },
    }
    query_collection = ""
    configuration = ""
    storage_m = ""
    current_chat_c = 0
    current_chat_name = ""

    def __init__(self):
        self.available_tools = {'query': self.query}
        print("LLM Agent gemaakt!")

    def initialize(self, query_collection, storage_m):
        self.query_collection = query_collection
        self.storage_m = storage_m

    def SETUP(self, chat_name):
        information = self.storage_m.getMessages(chat_name)
        print(information["messages"])
        self.setMemory(information["messages"])
        self.current_chat_c = information["id_chat"]
        self.current_chat_name = information["init_info"]["nameChat"]
        self.model = information["init_info"]["model"]
        self.query_collection.initialize(information["init_info"])


    def string_to_list(self, input_string):
        return ast.literal_eval(input_string)

    def getCurrentTime(self):
        return datetime.now().isoformat()

    def query(self, query_questions: list, questions_user: list) -> str:
        # print(type(query_questions), ":: \033[35mTYPE\033[0m")
        # print(len(query_questions), ":: \033[35mLEN\033[0m")
        # print(query_questions, ":: \033[35mCONTENT\033[0m")

        if type(query_questions) == str:
            # print(query_questions, ":: \033[35m<<<<<\033[0m")
            query_questions = self.string_to_list(query_questions)
        #
        # print(type(questions_user), ":: \033[35mTYPE Qu\033[0m")
        # print(len(questions_user), ":: \033[35mLEN Qu\033[0m")
        # print(questions_user, ":: \033[35mCONTENT Qu\033[0m")

        if type(questions_user) == str:
            questions_user = self.string_to_list(questions_user)

        requered_data = self.query_collection.handle_question(query_questions, questions_user)  # Database
        return requered_data

    def remove_tool_messages(self,messages):
        cleaned_messages = []
        for message in messages:
            if message.get('role') == 'tool':
                message['content'] = ""
                cleaned_messages.append(message)
            else:
                cleaned_messages.append(message)
        return cleaned_messages

    def mapself(self, w):
        print(self.mappings[w])

    def handle_input(self, prompt):
        tempchatMsg =  {
             "userrole_ids": [],
             "current_chat_id": [],
             "messages": [],
             "sources_used": [],
             "date":[]
        }

        content = prompt
        ct = self.getCurrentTime()

        output = ""
        self.memory_chat.append({'role': 'user', 'content': content})
        tempchatMsg['userrole_ids'].append(self.mappings["user"]); tempchatMsg['current_chat_id'].append(self.current_chat_c); tempchatMsg['messages'].append(prompt); tempchatMsg['sources_used'].append(""); tempchatMsg['date'].append(ct)
        if self.use_tool:
                response: ChatResponse = chat(
                    self.model,
                    messages=self.memory_chat,
                    tools=[self.askAboutFiles_tool])

                if response.message.tool_calls:
                    for tool in response.message.tool_calls:
                        if function_to_call := self.available_tools.get(tool.function.name):
                            print('Arguments:', tool.function.arguments)
                            output = function_to_call(**tool.function.arguments)
                        else:
                            pass

                if response.message.tool_calls:

                    self.memory_chat.append({'role': 'tool', 'content': str(output), 'name': tool.function.name})
                    final_response = chat(self.model, messages=self.memory_chat)
                    ct = self.getCurrentTime()
                    self.memory_chat = self.remove_tool_messages(self.memory_chat)
                    self.memory_chat.append({'role': 'assistant', 'content': final_response.message.content})
                    messageAI = final_response.message.content + "\n> USED TOOL"

                else:
                    final_response = chat(self.model, messages=self.memory_chat)
                    ct = self.getCurrentTime()
                    self.memory_chat.append({'role': 'assistant', 'content': final_response.message.content})
                    messageAI = final_response.message.content + "\n> NO TOOL USED"
        else:
            final_response = chat(self.model, messages=self.memory_chat)
            ct = self.getCurrentTime()
            self.memory_chat.append({'role': 'assistant', 'content': final_response.message.content})
            messageAI = final_response.message.content + "\n> TOOLS DISABLED"

        tempchatMsg['userrole_ids'].append(self.mappings["assistant"]);tempchatMsg['current_chat_id'].append(self.current_chat_c);tempchatMsg['messages'].append(final_response.message.content);tempchatMsg['sources_used'].append("Nog niks");tempchatMsg['date'].append(ct)

        self.saveToDatabase(tempchatMsg)
        return messageAI


    def saveToDatabase(self, content):
        for i in range(len(content["userrole_ids"])):
            self.storage_m.addMessage(content["userrole_ids"][i], content["current_chat_id"][i], content["messages"][i], content["sources_used"][i], content["date"][i])

    def resetMemory(self):
        self.memory_chat = []

    def setMemory(self, chatHistrory):
        self.memory_chat = chatHistrory

    def changeDatabse(self, pathDb, collectionName):
        self.query_collection.initialize(pathDb, collectionName)


import classDatabase
import classQuery


agent = LLMAgent()
databasemanager = classDatabase.StorageManager("chatIndex")
vectordb = classQuery.QueryEngine()
#
agent.initialize(vectordb, databasemanager)

agent.SETUP("GoombaBase12")

while True:
    prompt = input("Message: ")
    if prompt[0] == "\\":
        nameChat = prompt[1:]
        agent.SETUP(nameChat)
        print("Selected: \033[33m"+nameChat+"\033[0m")
        continue

    awnser = agent.handle_input(prompt)
    print(awnser)