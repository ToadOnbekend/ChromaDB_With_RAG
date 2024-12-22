from sqlalchemy import create_engine
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text


class Storage:
    def __init__(self, database):
        self.database = database
        self.engine = create_engine(f'sqlite:///databses/{database}.db')
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def makeNewChatIdex(self, name_x, vectordb, collection, model, modelembedding, modelreranking, embeddingdemensions, topnresults, nqueryresults, chunkoverlap, loadmodellocal, datecreated, chunksize):
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
        print("made")

    def addMessage(self, userrole, chat,message, sources, date):
        self.session.execute(text("""
            INSERT INTO messages (id_userrole, id_chat, inhoud, recourses, datamde)
            VALUES (:userrole, :chat, :message, :sources, :date);
        """), {
            "userrole": userrole,
            "chat": chat,
            "message": message,
            "sources": sources,
            "date": date
        })
        self.session.commit()
        print("made")



s = Storage('chatIndex')

s.makeNewChatIdex("c", "c", "c","c","c","c",4,4,4,4,"T","382",930)
s.addMessage(4,4, "r", "f", "r")
