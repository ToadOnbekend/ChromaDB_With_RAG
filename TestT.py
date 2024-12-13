from phi.agent import Agent
from phi.model.ollama import Ollama
from phi.tools.duckduckgo import DuckDuckGo
import chromadb
from chromadb.utils import embedding_functions
from transformers import AutoModelForSequenceClassification
import re
PROMPT  = "" #Zet hier de vraag die je wilt stellen
PATH_ChromaDB = "ChromaVectorDB"
COLLECTION_NAME = "Collection"
PROCESS_DEVICE = "cuda" # Of "cpu"
MODEL_EMBEDDING = "NetherlandsForensicInstitute/robbert-2022-dutch-sentence-transformers" #Zie Hugging Face voor meer modellen, zoek onder "sentence transformers"
RERANKER_MODEL = "jinaai/jina-reranker-v2-base-multilingual" #Zie Hugging Face voor meer modellen. Zoek onder "rerankers"
EMBEDDING_DEMENSIONS = 768 #Houd hetzelfde als bij "LoadInChromaDB.py"
TOP_N_RESULTS = 6
N_RESULTS_QUERY = 25 #!! TOP_N_RESULTS < N_RESULTS_QUERY !!
CHUNK_OVERLAP = 10 #Houd hetzelfde als bij "LoadInChromaDB.py"
OLLAMA_MODEL ="llama3.2:3b" #TODO: !!Runt ollama? Open ollama app.
#Installer met ollama "run llama3.2:3b", in CMD
LOAD_MODEL_LOCAL = True #Als je model lokaal is, zet op True. Dus voor het eerst op False!!


chroma_client = chromadb.PersistentClient(path=PATH_ChromaDB)
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
model_name=MODEL_EMBEDDING, device=PROCESS_DEVICE, trust_remote_code=True, truncate_dim=EMBEDDING_DEMENSIONS,
local_files_only=LOAD_MODEL_LOCAL)
collection = chroma_client.get_collection(name=COLLECTION_NAME, embedding_function=sentence_transformer_ef)
agent = Agent(
    model=Ollama(id="llama3.2:3b"),
    tools=[],
    vector_db=collection,
    markdown=True,
)

agent.print_response(
     "",

    #images=["https://upload.wikimedia.org/wikipedia/commons/b/bf/Krakow_-_Kosciol_Mariacki.jpg"],
    stream=True,
)