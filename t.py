import ollama

def chat_with_ollama_no_functions(user_question):
    response = ollama.chat(
        model='llama3.2:3b',
        messages=[
            {'role': 'user', 'content': user_question}
        ]
    )
    return response

x_r = chat_with_ollama_no_functions("hoe is Toad")
print(x_r)

