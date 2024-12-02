from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

# Laad het LLaMA-model
model_name = "openai-community/gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype=torch.float16)

# Maak een Hugging Face pipeline
hf_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Gebruik LangChain's LLM wrapper
llm = HuggingFacePipeline(pipeline=hf_pipeline)

# Configureer LangChain met geheugen
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory)

# Start een gesprek
print("Start een gesprek! Typ 'stop' om te stoppen.")
while True:
    user_input = input("Jij: ")
    if user_input.lower() == "stop":
        break
    response = conversation.run(input=user_input)
    print(f"Assistant: {response}")
