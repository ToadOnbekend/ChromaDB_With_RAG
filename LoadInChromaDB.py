from multiprocessing.queues import Queue
import chromadb
from chromadb.utils import embedding_functions
import time
import multiprocessing as mp
import re
import os
import pymupdf

PDF_FOLDER_PATH = "pdfstore" #"FolderNulPuntBepalenInfo"
QUEUE_BATCH_SIZE = 250
PATH_ChromaDB = "ChromaVectorDBTester"
COLLECTION_NAME = "Col2"
PROCESS_DEVICE = "cuda" # Of "cpu"
MODEL_EMBEDDING = "NetherlandsForensicInstitute/robbert-2022-dutch-sentence-transformers" # Zie Hugging Face voor meer modellen
EMBEDDING_DEMENSIONS = 768
CHUNK_SIZE = 65
CHUNK_OVERLAP = 10
LOAD_MODEL_LOCAL = True  #Als je model lokaal is, zet op True. Dus voor het eerst op False!!


def extract_years(filename):
    match = re.search(r'(\d{4}(?:_\d{4})?)', filename)
    return match.group(1) if match else "Not Given"

# def truncate_sentence(sentence, max_length=99999999999, visible_ends=100):
#     if len(sentence) > max_length:
#         return sentence[:visible_ends] + " .... " + sentence[-visible_ends:]
#     else:
#         return sentence

def extract_sentences_custom(text):
    sentence_pattern = r'[^.!?]*[.!?]'
    sentences = re.findall(sentence_pattern, text)
    return [sentence.strip() for sentence in sentences if sentence.strip()]


##TODO: !!Beoordeel eigen document, kijk naar indexen. Voeg toe aan lijst over verwijder deze
MARKDOWN_SEPARATORS = [
    r"\n#{1,6} ",
    r"```\n",
    r"\n\*\*\*+\n",
    r"\n\n",
]

def sliding_window_chunk(text, chunk_size=70, overlap=10):
    min_i_index = 0
    words = text.split()
    chunks = []
    chunks_sending = []

    # Maak regex-patroon voor alle markdown-separatoren
    separator_pattern = re.compile("|".join(MARKDOWN_SEPARATORS))

    # Verdeel de tekst in chunks
    for i in range(0, len(words), chunk_size - overlap):
        chunks.append(" ".join(words[i:i + chunk_size]))

    # Verwerk de chunks
    for i in range(len(chunks)):
        current_chunk = chunks[i - min_i_index]

        if separator_pattern.search(current_chunk):
            chunks_sending.append(current_chunk)

            ##
            # TODO: !!Zie eigen document hoe deze eruit zien, voeg toe of verwijder
            ##
        elif "..................." in current_chunk or "____" in current_chunk or "           " in current_chunk:
            chunks.pop(i - min_i_index)
            min_i_index += 1
        else:
            if current_chunk not in chunks_sending:
                chunks_sending.append(current_chunk)

    return chunks_sending

def producer(pdf_file, batch_size, queue):
    id = 1
    documents = []
    metadatas = []
    ids = []
    pdf_files = [f for f in os.listdir(pdf_file) if f.endswith('.pdf')]

    for i in range(len(pdf_files)):
        doc = pymupdf.open(f"{pdf_file}\\{pdf_files[i]}")
        text = ""

        for page_num in range(len(doc)):
            page = doc[page_num]
            text += page.get_text().replace("\n", " ") + " "

        segments = sliding_window_chunk(text, CHUNK_SIZE, CHUNK_OVERLAP)

        for x in range(len(segments)):
            documents.append(segments[x])
            metadatas.append({"segment_pos": x + 1,
                              "full_title": pdf_files[i],
                              "datum_year": extract_years(pdf_files[i]),
                              "title": pdf_files[i].replace("_" + extract_years(pdf_files[i]) + ".pdf", "") if extract_years(
                                  pdf_files[i]) in pdf_files[i] else pdf_files[i].replace(".pdf", ""),
                              "meta_id": id})
            ids.append(str(id))

            print("  \033[34;1m--DEBUG :::::::::::::::::::::::::::::\033[0m")
            print("FULL TITLE:\033[1;4m", pdf_files[i],"\033[0m")
            print("SEGMENT:\033[1m",segments[x])#truncate_sentence(segments[x]))
            print("\033[0mID\033[1m;", id)
            print("  \033[0m\033[34;1m--DEBUG :::::::::::::::::::::::::::::\033[0m\n\n")

            if len(ids) >= batch_size:
                queue.put((documents, metadatas, ids))
                documents = []
                metadatas = []
                ids = []
            id += 1

    if len(ids) > 0:
            queue.put((documents, metadatas, ids))


def consumer(use_cuda, queue):
    chroma_client = chromadb.PersistentClient(path=PATH_ChromaDB)

    device = PROCESS_DEVICE

    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=MODEL_EMBEDDING,
        device=device,
        trust_remote_code=True,
        truncate_dim = EMBEDDING_DEMENSIONS,
        local_files_only = LOAD_MODEL_LOCAL
    )
    collection = chroma_client.get_collection(name=COLLECTION_NAME, embedding_function=sentence_transformer_ef)

    while True:
        batch = queue.get()
        if batch is None:
            break

        collection.add(
            documents=batch[0],
            metadatas=batch[1],
            ids=batch[2]
        )


if __name__ == "__main__":

    chroma_client = chromadb.PersistentClient(path=PATH_ChromaDB)
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=MODEL_EMBEDDING,
        trust_remote_code=True,
        truncate_dim = EMBEDDING_DEMENSIONS,
        device = PROCESS_DEVICE,
        local_files_only = LOAD_MODEL_LOCAL
    )

    try:
        chroma_client.get_collection(name=COLLECTION_NAME)
        chroma_client.delete_collection(name=COLLECTION_NAME)
    except Exception as err:
        print(err)

    collection = chroma_client.create_collection(name=COLLECTION_NAME, embedding_function=sentence_transformer_ef, metadata={"hnsw:space": "cosine"})

    queue = mp.Queue()

    producer_process = mp.Process(target=producer, args=(PDF_FOLDER_PATH,QUEUE_BATCH_SIZE, queue,))
    consumer_process = mp.Process(target=consumer, args=(True, queue,))

    start_time = time.time()

    producer_process.start()
    consumer_process.start()

    producer_process.join()

    queue.put(None)

    consumer_process.join()

    print(f"Elapsed seconds: {time.time() - start_time:.0f} Record count: {collection.count()}")
