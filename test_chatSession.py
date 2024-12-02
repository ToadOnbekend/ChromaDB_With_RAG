from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_ollama import OllamaLLM

# Initialiseer de Ollama LLM met het LLaMA 3.2-model
llm = OllamaLLM(model="llama3.2:3b")

# Configureer het geheugen voor de gespreksgeschiedenis
memory = ConversationBufferMemory()

# Maak een conversatieketen met het LLM en het geheugen
conversation = ConversationChain(llm=llm, memory=memory)

# Start een gesprek
print("Begin een gesprek met de assistent. Typ 'stop' om te beëindigen.")
while True:
    user_input = input("Jij: ")
    if user_input.lower() == "stop":
        break
    response = conversation.run(input=user_input)
    print(f"Assistent: {response}")

#TODO: Bekijk ConversationBufferWindowMemory or ConversationTokenBufferMemory
#TODO: De LLM_WithChromaDB.py moet eigen module worden, importeer deze.
#TODO:    >>> https://python.langchain.com/docs/versions/migrating_memory/conversation_buffer_window_memory/