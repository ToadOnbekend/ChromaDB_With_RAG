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

thread_id ="0832"
config = {"configurable": {"thread_id": thread_id}}
app = workflow.compile(
    checkpointer=memory
)
# input_message = HumanMessage(content="hi! I'm bob")
# for event in app.stream({"messages": [input_message]}, config, stream_mode="values"):
#     event["messages"][-1].pretty_print()

while True:
    message = input(">> ")

    output_list = []
    for event in app.stream({"messages": [message]}, config, stream_mode="values"):
        output_list.insert(0,event["messages"][-1].content)

    print(output_list[0])