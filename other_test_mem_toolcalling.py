from ollama import chat
from ollama import ChatResponse
from module_ChromaDB_Ask import handle_question


orientatie_q = ""

def askAboutFiles(question: str) -> str:
    """
    gebruik de query voor het beantwoordne van de vraag
    """
    requered_data = handle_question([question])
    return requered_data

def dont_query(x):
    """
    gebruik niet de query om de vraag te beantwoorden
    """
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
        'name': 'askAboutFiles',
        'description': '',#'Bevraag de bestanden om de vraag van de gebruiker te beantwoorden',
        'parameters': {
            'type': 'object',
            'required': ['question'],
            'properties': {
                'question': {'type': 'string', 'description': 'beantwoord de vraag met de query'}
            },
        },
    },
}

dont_query_tool = {
    'type': 'function',
    'function': {
        'name': 'dont_query',
        'description': '',#'Bevraag niet de bestanden als de prompt niet met schoolzaken te maken heeft of niet gerelateerd is aan het Ashram College',
        'parameters': {
            'type': 'object',
            'required': ['x'],
            'properties': {
                'x': {'type': 'string', 'description': 'beantwoord niet de vraag met de query'}
            },
        },
    },
}

messages = [
    {
        "role": "system",
        "content": (
                f"Query ALTIJD wat de vraag ook is. Geef een hulpvol antwoord die de vraag van de gebruiker uitgebreid beantwoord."
        )
    }
]



available_functions = {
  'askAboutFiles': askAboutFiles,
  'dont_query':dont_query
}

while True:
    content = input(">> ")

    messages.append({'role': 'user', 'content': content})
    response: ChatResponse = chat(
      'llama3.2:3b',
      messages=messages,
      tools=[askAboutFiles_tool, dont_query_tool],
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

      # Get final response from model with function outputs
      print("Messages:",messages)
      final_response = chat('llama3.2:3b', messages=messages)
      messages = remove_tool_messages(messages)
      print('\n\033[34m' +str(final_response.message.content)+"\033[0m")
      messages.append({'role': 'assistant', 'content': final_response.message.content})

    else:
      print('No tool calls returned from model')

"""
  TODO
messages = [
    {"role": "system", "content": "Je bent een assistent die altijd blij en enthousiast reageert."},
    {"role": "user", "content": "Vertel me over het weer vandaag."}
]
"""
