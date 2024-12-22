from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

# Maak de database-engine
engine = create_engine('sqlite:///databses/aiconversations.db')
connection = engine.connect()
#%%
Base = declarative_base()
transaction = connection.begin()
#%%
connection.execute(text("""
CREATE TABLE indexBase (
    id_chat INTEGER PRIMARY KEY AUTOINCREMENT,  
    name VARCHAR(255),
    vectordb VARCHAR(255),
    collection VARCHAR(255),
    model VARCHAR(255),
    modelembeding VARCHAR(255),
    modelreranking VARCHAR(255),
    embeddingdemensions INTEGER,
    topnresults INTEGER,
    nqueryresults INTEGER,
    chunkoverlap INTEGER,
    loadmodellocal VARCHAR(255),
    datacreated VARCHAR(255)
);
"""))

connection.execute(text("""
CREATE TABLE users (
    id_userrole INTEGER PRIMARY KEY AUTOINCREMENT,
    userrole VARCHAR(255)                                            
);
"""))


connection.execute(text("""
CREATE TABLE messages (
    id_m INTEGER PRIMARY KEY AUTOINCREMENT,
    id_userrole INT,
    id_chat INT,
    FOREIGN KEY (id_chat) REFERENCES indexBase (id_chat),
    FOREIGN KEY (id_userrole) REFERENCES users (id_userrole),
    inhoud VARCHAR(255),
    recourses VARCHAR(255),
    datamde VARCHAR(255)
)
"""))
transaction.commit()



