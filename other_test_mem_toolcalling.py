from ollama import chat
from ollama import ChatResponse

import module_ChromaDB_Ask
from module_ChromaDB_Ask import handle_question
import ast
module_ChromaDB_Ask.initializeModelAndDatabase("ChromaVectorDB", "Collection")

orientatie_q = ""

# TODO: Deze kan meer dan de gene die we nu hebben

def string_to_list(input_string):
    return ast.literal_eval(input_string)

def query(query_questions: list, questions_user: list) -> str:
    print(type(query_questions), ":: \033[35mTYPE\033[0m")
    print(len(query_questions), ":: \033[35mLEN\033[0m")
    print(query_questions,":: \033[35mCONTENT\033[0m")

    if type(query_questions) == str:
       query_questions = string_to_list(query_questions)

    print(type(questions_user), ":: \033[35mTYPE Qu\033[0m")
    print(len(questions_user), ":: \033[35mLEN Qu\033[0m")
    print(questions_user,":: \033[35mCONTENT Qu\033[0m")

    if type(questions_user) == str:
       questions_user = string_to_list(questions_user)

    requered_data = handle_question(query_questions, questions_user)
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
            'required': ['query_questions', 'questions_user'],
            'properties': {
                'query_questions': {'type': 'list', 'description': 'Bedenk de benodigde zoekzinnen om de juiste gegevens te krijgen voor het beantwoorden van de vraag(vragen) uit de prompt'},
                'questions_user': {'type': 'list', 'description': 'Geef de vraag(vragen) van de gebruiker die in de pompt staat'},
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
            "Je bent een behulpzame ai assistente. Geef uitgebreid antwoord. Gebruik ALTIJD de query-functie, ONGEACHT de prompt van de gebruiker. Verander de prompt van de gebruiker NOOIT!"
        )
    }
]






available_functions = {
  'query': query,
  # 'dont_query':dont_query
}

while True:
    content = input(">> ")
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
