import classQuery
import classLLM

agent = classLLM.LLMAgent()
agent2 = classLLM.LLMAgent()
collectionB = classQuery.QueryEngine()

collectionB.initialize("ChromaVectorDBTester", "Collection")
agent.initialize("llama3.2:3b",[
    {
        "role": "system",
        "content": (
            "Je bent een behulpzame ai assistente. Geef uitgebreid antwoord. Gebruik ALTIJD de query-functie, ONGEACHT de prompt van de gebruiker. Verander de prompt van de gebruiker NOOIT!"
        )
    }
], collectionB)
agent2.initialize("llama3.2:3b",[
    {
        "role": "system",
        "content": (
            "Je bent een behulpzame ai assistente. Geef uitgebreid antwoord. Gebruik ALTIJD de query-functie, ONGEACHT de prompt van de gebruiker. Verander de prompt van de gebruiker NOOIT!"
        )
    }
], collectionB)

while True:
    response = responds =  agent.handle_input(responds)
    print("\n\033[45;1mLLM 1\033[0m\n"+response+"\n")
    print("\033[34m > Continue \033[0m")
    response = responds =  agent2.handle_input(response)
    print("\n\033[46;1mLLM 2\033[0m\n"+response+"\n")
    print("\033[34m > Continue \033[0m")

