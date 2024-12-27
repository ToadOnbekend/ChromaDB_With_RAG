import classLLMv2
import moduleLoadInChromaDB
import classQuery
import classDatabase


if __name__ == "__main__":
        agent = classLLMv2.LLMAgent()
        database = classDatabase.StorageManager("chatIndex")
        vectordb = classQuery.QueryEngine()

        agent.initialize(vectordb, database, moduleLoadInChromaDB)

        while True:
            prompt = input("Message: ")
            if prompt[0] == "\\":
                nameChat = prompt[1:]
                agent.SETUP(nameChat)
                print("Selected: \033[33m" + nameChat + "\033[0m")
                continue
            elif prompt[0] == "+":
                name = prompt[1:]
                agent.createNewChatIndex(name)
                agent.makeVectorDB()
                print("Selected: \033[33m" + name + "\033[0m")
                continue

            try:
                awnser = agent.handle_input(prompt)
                print(awnser)
            except:
                print("\033[31m-- Selecteer een vectorDB\033[0m")
