from ollama import chat
from ollama import ChatResponse
from module_ChromaDB_Ask import handle_question


orientatie_q = ""

def query(question: str) -> str:
    requered_data = handle_question([question])
    return requered_data

def dont_query(x):
    return x


def remove_tool_messages(messages):
    cleaned_messages = []
    for message in messages:
        if message.get('role') == 'tool':
            message['content'] = ""
            cleaned_messages.append(message)
        else:
            cleaned_messages.append(message)
    return cleaned_messages


askAboutFiles_tool = {
    'type': 'function',
    'function': {
        'name': 'query',
        'description': "Gebruik deze functie ALTIJD, ongeacht de prompt van de gebruiker",#'Deze functie geeft de benodigde externe informatie om de vraag te beantwoorden',
        'parameters': {
            'type': 'object',
            'required': ['question'],
            'properties': {
                'question': {'type': 'string', 'description': 'De prompt van de gebruiker'}
            },
        },
    },
}

dont_query_tool = {
    'type': 'function',
    'function': {
        'name': 'dont_query',
        'description': 'Deze functie gebruikt GEEN externe informatie',
        'parameters': {
            'type': 'object',
            'required': ['x'],
            'properties': {
                'x': {'type': 'string', 'description': 'De vraag van de gebruiker die met de interne informatie moet worden beantwoord.'}
            },
        },
    },
}


messages = [
    {
        "role": "system",
        "content": (
            "Je bent een behulpzame ai assistente. Geef uitgebreid antwoord. Gebruik ALTIJD de query-functie, ONGEACHT de prompt van de gebruiker. Verander de prompt(vraag/vragen) van de gebruiker NOOIT!"
        )
    }
]






available_functions = {
  'query': query,
  # 'dont_query':dont_query
}

while True:
    content = input(">> ")
    content += "\nGebruik de query-functie!"
    output = ""

    messages.append({'role': 'user', 'content': content})
    response: ChatResponse = chat(
      'llama3.2:3b',
      messages=messages,
      tools=[askAboutFiles_tool]#dont_query_tool],
    )

    if response.message.tool_calls:
      # There may be multiple tool calls in the response
      for tool in response.message.tool_calls:
        # Ensure the function is available, and then call it
        if function_to_call := available_functions.get(tool.function.name):
          print('Calling function:', tool.function.name)
          print('Arguments:', tool.function.arguments)
          output = function_to_call(**tool.function.arguments)
          print('Function output:', output)
        else:
          print('Function', tool.function.name, 'not found')

    # Only needed to chat with the model using the tool call results
    if response.message.tool_calls:
      # Add the function response to messages for the model to use

      messages.append({'role': 'tool', 'content': str(output), 'name': tool.function.name})

      print("Messages:",messages)
      final_response = chat('llama3.2:3b', messages=messages)
      messages = remove_tool_messages(messages)
      print('\n\033[34m' +str(final_response.message.content)+"\033[0m")
      messages.append({'role': 'assistant', 'content': final_response.message.content})

    else:
        final_response = chat('llama3.2:3b', messages=messages)
        #messages = remove_tool_messages(messages)
        print('\n\033[34m' + str(final_response.message.content) + "\033[0m")
        messages.append({'role': 'assistant', 'content': final_response.message.content})

"""
  TODO
messages = [
    {"role": "system", "content": "Je bent een assistent die altijd blij en enthousiast reageert."},
    {"role": "user", "content": "Vertel me over het weer vandaag."}
]
"""
