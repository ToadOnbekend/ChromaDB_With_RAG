import ollama


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

response = ollama.chat(
  'llama3.2:3b',
  messages=[{'role': 'user', 'content': 'get  a random name'}],
  tools=[add_two_numbers, get_random_name], # Actual function reference
)

available_functions = {
  'add_two_numbers': add_two_numbers,
  'get_random_name': get_random_name
}

for tool in response.message.tool_calls or []:
  function_to_call = available_functions.get(tool.function.name)
  if function_to_call:
    print('Function output:', function_to_call(**tool.function.arguments))
  else:
    print('Function not found:', tool.function.name)
