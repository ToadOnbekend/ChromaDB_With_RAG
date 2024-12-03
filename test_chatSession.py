# from langchain.chains import ConversationChain
# from langchain.memory import ConversationBufferMemory
from langchain_ollama import OllamaLLM
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.prompts.chat import (
#     ChatPromptTemplate,
#     HumanMessagePromptTemplate,
#     MessagesPlaceholder,
# )
from langchain_core.messages import HumanMessage
from langgraph.graph import START, MessagesState, StateGraph

workflow = StateGraph(state_schema=MessagesState)
llm = OllamaLLM(model="llama3.2:3b")
memory = MemorySaver()

def call_model(state: MessagesState):
    response = llm.invoke(state["messages"])
    # We return a list, because this will get added to the existing list
    return {"messages": response}


# Define the two nodes we will cycle between
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)


app = workflow.compile(
    checkpointer=memory
)

THREAD_ID = "172"
config = {"configurable": {"thread_id": THREAD_ID}}

while True:
    user_input = input("Jij: ")
    if user_input.lower() == "stop":
        break

    for event in app.stream({"messages": [user_input]}, config, stream_mode="values"):
       try:
        print(event["messages"][1].content)
        print(event)
       except:
           pass


#TODO: Bekijk ConversationBufferWindowMemory or ConversationTokenBufferMemory
#TODO: De LLM_WithChromaDB.py moet eigen module worden, importeer deze.
#TODO:    >>> https://python.langchain.com/docs/versions/migrating_memory/conversation_buffer_window_memory
#TODO:Function calling: https://zilliz.com/blog/function-calling-ollama-llama-3-milvus