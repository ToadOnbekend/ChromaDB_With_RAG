# from langchain_core.messages import AIMessage
# from langchain_core.tools import tool
# from langgraph.prebuilt import ToolNode
# from langchain_ollama import OllamaLLM

import ollama
OLLAMA_MODEL ="llama3.2:3b"

storage = ""

#  HumanInput: ---
#  GeneratedOutput: ---

storage = ""

# Loop voor voortdurende interactie
while True:
    # Vraag om input van de gebruiker
    prompt_ollama = input("PROMPT: ")

    # Voeg de input van de gebruiker toe aan de opslag
    storage += f"HumanInput: {prompt_ollama}\n"

    # Genereer output met Ollama, gebruikmakend van de volledige context
    output = ollama.generate(
        model=OLLAMA_MODEL,
        prompt=(
            f"Je bent een taalmodel dat de berichtgeschiedenis bewaart.\n"
            f"De geschiedenis van de interactie tussen jou en de gebruiker staat hieronder:\n"
            f"Wat jij hebt gezegd, staat onder 'GeneratedOutput', en wat de gebruiker heeft gezegd, staat onder 'HumanInput'.\n"
            f"Gebruik deze context om eerdere antwoorden en vragen te begrijpen:\n{storage}\n"
            f"Zet NOOIT: 'GeneratedOutput' en 'HumanInput' in je antwoord"
            f"Beantwoord de volgende prompt: {prompt_ollama}"
        ),
        options={'temperature': 0.5}  # Pas willekeurigheid aan tussen 0.1 (consistent) en 1 (creatief, minder consistent)
    )

    # Voeg de gegenereerde output toe aan de opslag
    storage += f"GeneratedOutput: {output['response']}\n"

    # Toon het antwoord van Ollama
    print("OLLAMA:", output["response"])
