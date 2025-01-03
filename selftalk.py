import classLLMv2
import classDatabase
import classQuery
import moduleLoadInChromaDB
content = "Speel de bekende show My 600LB-life "


if __name__ == "__main__":
    agent = classLLMv2.LLMAgent()
    agent2 = classLLMv2.LLMAgent()
    database = classDatabase.StorageManager("chatIndex")
    vectordb = classQuery.QueryEngine()

    agent.initialize(vectordb, database, moduleLoadInChromaDB)
    agent2.initialize(vectordb, database, moduleLoadInChromaDB)

    agent.createNewChatIndex("MyPoundffa","FfWA9d1ww", "Jij bent acteur 1 van de bekende show My 600LB-life. Jij ben de afval dokter")
    agent.makeVectorDB()
    agent2.createNewChatIndex("MyPoundaaaa","FfWs9d1ww", "Je bent acteur 2 van de bekende show My 600LB-life. Jij bent een patient die 600lb weegt en NIET wilt afvallen en hier alles aandoet om sporten,gezond eten en bewegen te ontlopen")
    agent2.makeVectorDB()


    print(f"  \033[41m\033[1m START \033[0m\n{content}\n\n")

    while True:
        response1 = agent.handle_input(content)
        print(f"Agent 1: {response1}")

        response2 = agent2.handle_input(response1)
        print(f"Agent 2: {response2}")

        content = response2
