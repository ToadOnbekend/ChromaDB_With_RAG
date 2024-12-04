import ollama

MODEL = 'llama3.2:3b'


def add_two_numbers(a: int, b: int) -> int:
    """
    Add two numbers

    Args:
      a: The first integer number
      b: The second integer number

    Returns:
      int: The sum of the two numbers
    """
    return int(a) + int(b)


def get_random_name() -> str:
    """
    Gets a random name

    Returns:
     str: random name
    """
    return "Henk"


available_functions = {
    'add_two_numbers': add_two_numbers,
    'get_random_name': get_random_name
}


# class AIchatAgent():
#     def __init__(self, tools, tool_functions, model):
#         self.memory = []
#         self.tools = tools
#         self.tool_functions = tool_functions
#         self.tools["self_generate"] = self.internal_generate
#         self.model = model
#
#     def add_to_memory_U(self, role, content):
#         self.memory.append({'role': role, 'content': content})
#
#     def internal_generate(self) -> str:
#         """
#         Awnsers the question of the user
#
#         Returns:
#           str: response generated
#         """
#         response = ollama.chat(
#             model=self.model,
#             messages=self.memory
#         )
#         return response["response"]
#
#     def function_calling(self, prompt):
#         self.add_to_memory_U('user', prompt)
#         response = ollama.chat(
#             self.model,
#             messages=self.memory,
#             tools=self.tool_functions,  # De werkelijke tools
#         )
#         for tool in response.message.tool_calls or []:
#             function_to_call = self.tools.get(tool.function.name)
#             if function_to_call:
#                 ant = "Function output:" + str( function_to_call(**tool.function.arguments))
#                 print(ant)
#                 self.add_to_memory_U('assistant', ant)
#             else:
#                 print('Function not found:', tool.function.name)

class AIchatAgent():
    def __init__(self, tools, tool_functions, model):
        self.memory = []
        self.tools = tools
        self.tool_functions = tool_functions
        self.model = model

    def add_to_memory(self, role, content):
        """
        Voegt een bericht toe aan het geheugen.
        """
        self.memory.append({'role': role, 'content': content})

    def chat(self, prompt):
        """
        Chat met het model waarbij het model zelf bepaalt of tools worden gebruikt.

        Args:
          prompt (str): De input van de gebruiker.

        Returns:
          str: Het antwoord van de assistant of de uitvoer van een tool.
        """
        # Voeg de input van de gebruiker toe aan het geheugen
        self.add_to_memory('user', prompt)

        # Vraag een antwoord op van het model
        response = ollama.chat(
            model=self.model,
            messages=self.memory,
            tools=self.tool_functions  # Geef tools door aan het model
        )

        # Check of het model een function call wil uitvoeren
        if 'tool_calls' in response['message'] and response['message']['tool_calls']:
            for tool in response["message"]["tool_calls"]:
                # Zoek het gevraagde tool in de tools-lijst
                function_to_call = self.tools.get(tool["function"]["name"])
                if function_to_call:
                    # Voer de tool-functie uit met de meegegeven argumenten
                    tool_output = function_to_call(**tool["function"]["arguments"])
                    formatted_response = f"Function output: {tool_output}"

                    # Voeg de tooluitvoer toe aan het geheugen
                    self.add_to_memory('assistant', formatted_response)

                    # Stuur de tooluitvoer terug als antwoord
                    return formatted_response
                else:
                    print(f"Tool not found: {tool['function']['name']}")
        else:
            # Als er geen tools nodig zijn, geef het directe modelantwoord
            response = ollama.chat(
                model=self.model,
                messages=self.memory, # Geef tools door aan het model
            )
            return response

llamaA = AIchatAgent(available_functions, [add_two_numbers, get_random_name], MODEL)

awns = llamaA.chat("5+5 en 3+2")
print(awns)
print("---------------------")
llamaA.chat("hoe heet ik?")