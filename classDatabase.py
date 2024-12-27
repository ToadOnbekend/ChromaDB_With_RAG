
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text



class StorageManager:
    mappings = {"1":"system",
                "2":"assistant",
                "3":"user",
                "4":"tool"}

    def __init__(self, database):
        self.database = database
        self.engine = create_engine(f'sqlite:///databses/{database}.db')
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()


    def makeNewChatIdex(self, name_x, vectordb, collection, model, modelembedding, modelreranking, embeddingdemensions, topnresults, nqueryresults, chunkoverlap, loadmodellocal, chunksize, datecreated):
        current_id = 0;

        self.session.execute(text("""
            INSERT INTO indexBase (name, vectordb, collection, model, modelembeding, modelreranking, embeddingdemensions, topnresults, nqueryresults, chunkoverlap, loadmodellocal, datacreated, chunksize)
            VALUES (:name_x, :vectordb, :collection, :model, :modelembedding, :modelreranking, :embeddingdemensions, :topnresults, :nqueryresults, :chunkoverlap, :loadmodellocal, :datecreated, :chunksize);
        """), {
            "name_x": name_x,
            "vectordb": vectordb,
            "collection": collection,
            "model": model,
            "modelembedding": modelembedding,
            "modelreranking": modelreranking,
            "embeddingdemensions": embeddingdemensions,
            "topnresults": topnresults,
            "nqueryresults": nqueryresults,
            "chunkoverlap": chunkoverlap,
            "loadmodellocal": loadmodellocal,
            "datecreated": datecreated,
            "chunksize": chunksize
        })

        self.session.commit()
        result_initalization_pre = self.session.execute(text("""
                        SELECT  id_chat
                        FROM indexBase
                        WHERE name = :chatName
                        LIMIT 1;
                    """), {
            "chatName": name_x
        }).fetchall()

        for result in result_initalization_pre:
            current_id = result[0]

        print("made")
        return current_id

    def getChatCollections(self):
        chatCollections = {"name":[], "date":[], "id":[]}
        result_initalization_pre = self.session.execute(text("""
                                SELECT  name, id_chat, datacreated
                                FROM indexBase
                                ORDER BY datacreated;
                            """)).fetchall()

        for result in result_initalization_pre:
            chatCollections["name"].append(result[0])
            chatCollections["date"].append(result[2])
            chatCollections["id"].append(result[1])

        return chatCollections


    def addMessage(self, userrole_ids, chat_ids,message, sources, date):
        self.session.execute(text("""
            INSERT INTO messages (id_userrole, id_chat, inhoud, recourses, datamde)
            VALUES (:userrole_id, :chat_id, :message, :sources, :date);
        """), {
            "userrole_id": userrole_ids,
            "chat_id": chat_ids,
            "message": message,
            "sources": sources,
            "date": date
        })
        self.session.commit()
        # print("made")

    def getMessages(self, chatName):
        message_collection = []
        sendInfo = []
        id_current_chat = 0

        result = self.session.execute(text("""
                SELECT messages.id_chat, messages.inhoud, messages.recourses, users.id_userrole,messages.datamde
                FROM messages
                JOIN indexBase ON messages.id_chat = indexBase.id_chat
                JOIN users ON messages.id_userrole = users.id_userrole
                WHERE indexBase.name = :chatName
                ORDER BY messages.datamde;
            """), {
                "chatName": chatName
        }).fetchall()

        result_initalization_pre = self.session.execute(text("""
                SELECT name, vectordb, collection, model, modelembeding, modelreranking, embeddingdemensions, topnresults, nqueryresults, chunkoverlap, loadmodellocal, datacreated, chunksize 
                FROM indexBase
                WHERE name = :chatName
                LIMIT 1;
            """), {
                "chatName": chatName
        }).fetchall()

        for result_initalization in result_initalization_pre:
            result_init = {
                "nameChat": result_initalization[0],
                "vectordb": result_initalization[1],
                "collection": result_initalization[2],
                "model": result_initalization[3],
                "modelembedding": result_initalization[4],
                "modelreranking": result_initalization[5],
                "embeddingdemensions": result_initalization[6],
                "topnresults": result_initalization[7],
                "nqueryresults": result_initalization[8],
                "chunkoverlap": result_initalization[9],
                "loadmodellocal": result_initalization[10],
                "datecreated": result_initalization[11],
                "chunksize": result_initalization[12]
            }


        for message in result:
            id_chat = message[0]
            content = message[1]
            recourses = message[2]
            userrole = message[3]
            datamde = message[4]

            message_collection.append({"role": self.mappings[str(userrole)], "content": content})
            sendInfo.append([recourses, datamde])
            id_current_chat = id_chat

        result_database = {
            "id_chat": id_current_chat,
            "messages": message_collection,
            "sendInfo": sendInfo,
            "init_info": result_init
        }

        return result_database

    def getLoadconfig(self, chatId):
        result_init = {}
        result_initalization_pre = self.session.execute(text("""
                        SELECT name, vectordb, collection, model, modelembeding, modelreranking, embeddingdemensions, topnresults, nqueryresults, chunkoverlap, loadmodellocal, datacreated, chunksize 
                        FROM indexBase
                        WHERE id_chat = :chatID
                        LIMIT 1;
                    """), {
            "chatID": chatId
        }).fetchall()

        for result_initalization in result_initalization_pre:
            result_init = {
                "nameChat": result_initalization[0],
                "vectordb": result_initalization[1],
                "collection": result_initalization[2],
                "model": result_initalization[3],
                "modelembedding": result_initalization[4],
                "modelreranking": result_initalization[5],
                "embeddingdemensions": result_initalization[6],
                "topnresults": result_initalization[7],
                "nqueryresults": result_initalization[8],
                "chunkoverlap": result_initalization[9],
                "loadmodellocal": result_initalization[10],
                "datecreated": result_initalization[11],
                "chunksize": result_initalization[12]
            }

        return result_init




# current_time = datetime.now().isoformat()
# print(current_time)

# id_sf = s.makeNewChatIdex("GoombaBase12", "f", "f", "f", "f","d","f",2, 2, 2, "T", 3)
#
# for i in range(20):
#     current_time = datetime.now().isoformat()
#     s.addMessage(2, id_sf, f"Hello -- {i} --", "Toad is cool",)
#     time.sleep(1)
#
#
#         import pprint
#         pp = pprint.PrettyPrinter(indent=4, underscore_numbers=True)
#         pp.pprint(result_database)
# TODO: