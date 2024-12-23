from ollama import chat
from ollama import ChatResponse
import classQuery
import ast


class LLMAgent():
    model = ""
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
    storage_m = ""
    current_chat_c = 0

    def __init__(self):
        self.available_tools = {'query': self.query}
        print("LLM Agent gemaakt!")

    def initialize(self, model, memory_chat, query_collection):
        self.model = model
        self.memory_chat = memory_chat
        self.query_collection = query_collection

        print("Initialized!")

    def string_to_list(self, input_string):
        return ast.literal_eval(input_string)

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

    def handle_input(self, prompt):
        content = prompt
        output = ""

        self.memory_chat.append({'role': 'user', 'content': content})
        response: ChatResponse = chat(
            'llama3.2:3b',
            messages=self.memory_chat,
            tools=[self.askAboutFiles_tool]
        )

        if response.message.tool_calls:
            for tool in response.message.tool_calls:

                if function_to_call := self.available_tools.get(tool.function.name):
                    # print('Calling function:', tool.function.name)
                    print('Arguments:', tool.function.arguments)
                    output = function_to_call(**tool.function.arguments)
                    # print('Function output:', output)
                else:
                    pass
                    # print('Function', tool.function.name, 'not found')


        if response.message.tool_calls:

            self.memory_chat.append({'role': 'tool', 'content': str(output), 'name': tool.function.name})

            # print("Messages:", self.memory_chat)
            final_response = chat('llama3.2:3b', messages=self.memory_chat)
            self.memory_chat = self.remove_tool_messages(self.memory_chat)
            self.memory_chat.append({'role': 'assistant', 'content': final_response.message.content})
            return final_response.message.content + "\n> USED TOOL"

        else:
            final_response = chat('llama3.2:3b', messages=self.memory_chat)

            self.memory_chat.append({'role': 'assistant', 'content': final_response.message.content})
            return final_response.message.content

    def resetMemory(self):
        self.memory_chat = []

    def setMemory(self, chatHistrory):
        self.memory_chat = chatHistrory

    def changeDatabse(self, pathDb, collectionName):
        self.query_collection.initialize(pathDb, collectionName)

