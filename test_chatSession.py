from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.llms import HuggingFaceHub

# Gebruik Hugging Face of een lokaal model
from langchain.llms import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# Laad een lokaal model via Hugging Face
model_name = "gpt2"  # Gebruik een geavanceerd model indien nodig
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_length=512, temperature=0.7)
llm = HuggingFacePipeline(pipeline=pipe)

# Gespreksgeschiedenis met memory
memory = ConversationBufferMemory()

# Maak een ConversationChain
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True  # Schakel uit als je geen debuginformatie wilt
)

# Start een gesprek
if __name__ == "__main__":
    print("Begin een gesprek met de chatbot (type 'stop' om te stoppen):")

    while True:
        user_input = input("Jij: ")
        if user_input.lower() == "stop":
            break

        # Vraag de LLM om een antwoord
        response = conversation.run(input=user_input)
        print(f"Bot: {response}")
