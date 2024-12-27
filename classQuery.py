import chromadb
from chromadb.utils import embedding_functions
from transformers import AutoModelForSequenceClassification
import pprint

class QueryEngine():
    PROCESS_DEVICE = "cuda"
    MODEL_EMBEDDING = "NetherlandsForensicInstitute/robbert-2022-dutch-sentence-transformers"
    RERANKER_MODEL = "jinaai/jina-reranker-v2-base-multilingual"
    EMBEDDING_DEMENSIONS = 768
    TOP_N_RESULTS = 6
    N_RESULTS_QUERY = 25
    CHUNK_OVERLAP = 10
    LOAD_MODEL_LOCAL = True

    chroma_client = ""
    sentence_transformer_ef = ""
    collection = ""
    model = ""

    def __init__(self):
        pass

    def initialize(self, information):

        pp = pprint.PrettyPrinter(indent=4, underscore_numbers=True)
        print(f"\033[34m{pp.pprint(information)}\033[0m")
        print("\033[36mInitializing...\033[0m")
        print("SET \033[1mPathChromaDB {}\033[0m".format(information["vectordb"]))
        print("SET \033[1mCollectionNameV {}\033[0m\n".format(information["collection"]))
        self.chroma_client = chromadb.PersistentClient(path=information["vectordb"])
        self.MODEL_EMBEDDING = information["modelembedding"]
        self.RERANKER_MODEL = information["modelreranking"]
        self.EMBEDDING_DEMENSIONS = information["embeddingdemensions"]
        self.TOP_N_RESULTS = information["topnresults"]
        self.N_RESULTS_QUERY = information["nqueryresults"]
        self.CHUNK_OVERLAP = information["chunkoverlap"]
        self.LOAD_MODEL_LOCAL = True if information["loadmodellocal"] == "True" else False
        self.sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=self.MODEL_EMBEDDING, device=self.PROCESS_DEVICE, trust_remote_code=True,
            truncate_dim=self.EMBEDDING_DEMENSIONS,
            local_files_only=self.LOAD_MODEL_LOCAL)
        self.collection = self.chroma_client.get_collection(name=information["collection"],
                                                            embedding_function=self.sentence_transformer_ef)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.RERANKER_MODEL, torch_dtype="auto",
                                                                        trust_remote_code=True,
                                                                        local_files_only=self.LOAD_MODEL_LOCAL)



        self.model.to('cuda')  # ⇐ ALS op CPU, haal deze regel weg

    def merge_multiple_lists_of_texts_with_split(self, text_lists):
        def find_exact_overlap(words1, words2, overlap_size=self.CHUNK_OVERLAP):
            if len(words1) >= overlap_size and len(words2) >= overlap_size:
                return words1[-overlap_size:] == words2[:overlap_size]
            return False

        all_texts = [{"index": i, "words": text.split()} for text_list in text_lists for i, text in
                     enumerate(text_list)]
        unmerged_texts = set(range(len(all_texts)))
        merged_groups = []
        while unmerged_texts:
            current_text_index = unmerged_texts.pop()
            current_group = [current_text_index]
            added = True
            while added:
                added = False
                for other_index in list(unmerged_texts):
                    current_words = all_texts[current_group[-1]]["words"]
                    other_words = all_texts[other_index]["words"]
                    if find_exact_overlap(current_words, other_words):
                        current_group.append(other_index)
                        unmerged_texts.remove(other_index)
                        added = True
                    elif find_exact_overlap(other_words, all_texts[current_group[0]]["words"]):
                        current_group.insert(0, other_index)
                        unmerged_texts.remove(other_index)
                        added = True
            merged_words = all_texts[current_group[0]]["words"]
            for i in range(1, len(current_group)):
                overlap = self.CHUNK_OVERLAP
                merged_words += all_texts[current_group[i]]["words"][overlap:]
            merged_groups.append(" ".join(merged_words))

        return merged_groups

    def handle_question(self, questionS, q_user_p):
        vragen = ""
        responds_return = "\n"
        len_q = len(questionS)
        # print(len(questionS), "TYPE TYPE")
        for i in range(len(questionS)):
            questionP = questionS[i]
            vragen += questionP + "? "
            responds_return += "Query opdracht: " + questionP + "\nBijhorende bestanden:\n\n"
            results = self.collection.query(
                query_texts=questionP,
                n_results=self.N_RESULTS_QUERY,
                include=["documents", "metadatas"]
            )
            to_rerank_inhoud = []
            for i in range(len(results["documents"][0])):
                inhoud = results["documents"][0][i]
                if inhoud not in to_rerank_inhoud:
                    to_rerank_inhoud.append(inhoud)
            rankings = self.model.rerank(
                questionP,
                to_rerank_inhoud,
                max_query_length=512,
                max_length=1024,
                top_n=self.TOP_N_RESULTS
            )
            add = []
            for i in range(len(rankings)):
                add.append(rankings[i]["document"])
            structured_data_combine = []
            # TODO: Haal dit weg en haal de bestands namen op die  zijn gebruikt
            for i in range(len(results["documents"][0])):
                if results["documents"][0][i] in add:
                    # file_name = results["metadatas"][0][i]["full_title"]
                    # name = (file_name.replace("_" + extract_years(file_name) + ".pdf", "") if extract_years(file_name) in file_name else file_name.replace(".pdf", "")).replace("_"," ")
                    add_Q = results["documents"][0][i]
                    structured_data_combine.append([add_Q])
                    # print("[ \033[32;1m+\033[0m ] File Relevant:\033[4;1m", file_name, "\033[0m\033[1m\n >> \033[0m", truncate_sentence(results["documents"][0][i]), "\n")
            merged_result = self.merge_multiple_lists_of_texts_with_split(structured_data_combine)
            for i in range(len(merged_result)):
                responds_return += merged_result[i] + "\n----\n"

            if len_q > 1 and i != len_q:
                responds_return += "\n\n"
            to_rerank_inhoud = []
            add = []
            structured_data_combine = []

        responds_return += f"Gebruik deze bestanden om de vraag(vragen) van de gebruiker te beantwoorden: {'? '.join(q_user_p)}"  # \nBedenk altijd of de prompt de bestanden nodig heeft, bijvoorbeeld een conversationele prompt of bij een statement. Gebruik dan absoluut NIET de behorende bestanden!"
        return responds_return


