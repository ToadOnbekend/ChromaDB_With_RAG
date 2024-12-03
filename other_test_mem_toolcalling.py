from ollama import chat
from ollama import ChatResponse
from module_ChromaDB_Ask import handle_question



def askAboutFiles(question: str) -> str:
    """
    Gebruik de geuploade pdf om het antwoord van de gebruiker te beantwoorden
    """
    requered_data = handle_question(question)
    return requered_data

askAboutFiles_tool = {
  'type': 'function',
  'function': {
    'name': 'askAboutFiles',
    'description': 'Bevraag de bestanden om de vraag van de gebruiker te beantwoorden',
    'parameters': {
      'type': 'object',
      'required': ['question'],
      'properties': {
        'question': {'type': 'str', 'description': 'De vraag voor de bestanden'}
      },
    },
  },
}
messages = []

available_functions = {
  'askAboutFiles': askAboutFiles
}

while True:
    content = input(">> ")

    messages.append({'role': 'user', 'content': content})
    response: ChatResponse = chat(
      'llama3.2:3b',
      messages=messages,
      tools=[askAboutFiles_tool],
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
      messages.append(response.message)
      messages.append({'role': 'tool', 'content': str(output), 'name': tool.function.name})

      # Get final response from model with function outputs
      final_response = chat('llama3.2:3b', messages=messages)
      print('Final response:', final_response.message.content)

    else:
      print('No tool calls returned from model')