# from ollama import chat
# from ollama import ChatResponse
# import ast
#
#
# #from module_ChromaDB_Ask import handle_question
# from Module_Query import handle_question
#
# orientatie_q = ""
#
# def askAboutFiles(questions: list) -> str:
#     """
#     Gebruik de bestanden om de vraag (vragen) van de gebruiker te beantwoorden
#     retuns:
#         requered_data (string): Bevat de benodigde bestanden om de vraag(vragen) van de gebruiker te beantwoorden
#     """
#
#     def string_to_list(input_string):
#         try:
#             # Verwijder witruimte aan de randen
#             input_string = input_string.strip()
#             # Converteer de string naar een lijst met ast.literal_eval voor veiligheid
#             result = ast.literal_eval(input_string)
#             # Controleer of de output daadwerkelijk een lijst is
#             if isinstance(result, list):
#                 return result
#             else:
#                 raise ValueError("De invoer is geen geldige lijst-string.")
#         except Exception as e:
#             return f"Fout bij het converteren: {e}"
#
#
#     resultaat = string_to_list(questions)
#     if len(resultaat )-1 >= 10:
#         resultaat = [questions]
#
#         print("STRING: ",resultaat)
#
#     requered_data = handle_question(resultaat)
#     return requered_data
# # def askAboutFiles(questions: list) -> str:
# #     """
# #     Gebruik de geuploade pdf om het antwoord(en) van de gebruiker te beantwoorden
# #     """
# #
# #     requered_data = ""
# #     return requered_data
#
# def dont_query(x):
#     """
#     Wanneer uit de prompt blijkt dat de bestanden bevragen niet nodig is of niet relevant is
#     """
#     return x
#
# # askAboutFiles_tool ={
# #         'type': 'function',
# #         'function': {
# #            'name': 'askAboutFiles',
# #            'description': 'Bevraag de bestanden om de vraag van de gebruiker te beantwoorden',
# #                  'parameters': {
# #                      'type': 'object',
# #                      'required': ['question'],
# #                      'properties': {
# #                      'question': {'type': 'str', 'description': 'De vraag voor de bestanden'}
# #          },
# #         },
# #      },
# # }
# # askAboutFiles_tool ={
# #         'type': 'function',
# #         'function': {
# #            'name': 'askAboutFiles',
# #            'description': 'Bevraag de bestanden om de vraag of vragen van de gebruiker te beantwoorden. Verbeter de spelling NIET van de  vraag en laat de vraag zoals hij is gesteld. Vertaal NOOIT de vraag(vragen) van de gebruiker.',
# #                  'parameters': {
# #                      'type': 'object',
# #                      'required': ['questions'],
# #                      'properties': {
# #                      'questions': {'type': 'list', 'description': 'De vraag(en) voor de bestanden'}
# #          },
# #         },
# #      },
# # }
# askAboutFiles_tool = {
#     'type': 'function',
#     'function': {
#         'name': 'askAboutFiles',
#         'description': (
#             'Bevraag de bestanden om de vraag of vragen van de gebruiker te beantwoorden. '
#             'Gebruik deze functie voor alle vragen die betrekking hebben op schoolgerelateerde onderwerpen zoals vakken, roosters, huiswerk, regels, klachtenregeling, schoolactiviteiten (zoals ouderavonden), '
#             'en andere zaken die specifiek zijn voor de middelbare school Ashram Alphen. '
#             'Zelfs als de vraag niet expliciet naar schoolgerelateerde zaken verwijst, veronderstel dat de vraag binnen dit domein valt en beantwoord deze door de bestanden te raadplegen. '
#             'Verbeter de spelling NIET van de vraag en laat de vraag zoals deze is gesteld. Vertaal NOOIT de vraag(vragen) van de gebruiker.'
#         ),
#         'parameters': {
#             'type': 'object',
#             'required': ['questions'],
#             'properties': {
#                 'questions': {
#                     'type': 'list',
#                     'description': 'De vraag(en) voor de bestanden'
#                 }
#             }
#         }
#     }
# }
#
#
#
# dont_query_tool = {
#     'type': 'function',
#     'function': {
#         'name': 'dont_query',
#         'description': (
#             'Bevraag de bestanden niet. Gebruik deze functie alleen als de vraag **absoluut niet** betrekking heeft op schoolgerelateerde onderwerpen zoals vakken, roosters, huiswerk, regels, klachtenregeling, '
#             'of andere zaken die specifiek zijn voor de middelbare school Ashram Alphen. '
#             'Dit zou het geval zijn bij algemene vragen die geen betrekking hebben op de school zelf of haar organisatie, bijvoorbeeld vragen over algemene informatie of persoonlijke zaken die buiten het schooldomein vallen.'
#         ),
#         'parameters': {
#             'type': 'object',
#             'required': ['x'],
#             'properties': {
#                 'x': {
#                     'type': 'str',
#                     'description': 'De vraag die geen betrekking heeft op de school en dus niet de bestanden hoeft te raadplegen'
#                 }
#             }
#         }
#     }
# }
#
#
#
# messages = [
#     {"role": "system", "content": (
#         "Je bent een digitale assistent van de middelbare school Ashram Alphen, en hebt toegang tot alle documenten en bestanden van de school. "
#         "Wanneer iemand een vraag stelt die mogelijk betrekking heeft op schoolgerelateerde onderwerpen zoals vakken, roosters, huiswerk, regels, klachtenregeling, schoolactiviteiten (zoals ouderavonden), of andere zaken die specifiek zijn voor de school, "
#         "moet je altijd de bestanden raadplegen om het juiste antwoord te geven. "
#         "Zelfs als de vraag niet expliciet verwijst naar schoolgerelateerde zaken, veronderstel dan dat de vraag betrekking heeft op de school en gebruik de bestanden om een accuraat antwoord te geven. "
#         "Je kunt deze functie ook gebruiken om toegang te krijgen tot de benodigde documenten en biedt vervolgens een nauwkeurig antwoord op basis van de gegevens in de schoolbestanden."
#     )}
# ]
#
#
# available_functions = {
#   'askAboutFiles': askAboutFiles,
#   'dont_query':dont_query
# }
#
# while True:
#     content = input(">> ")
#
#     messages.append({'role': 'user', 'content': content})
#     response: ChatResponse = chat(
#       'llama3.2:3b',
#       messages=messages,
#       tools=[askAboutFiles_tool, dont_query_tool],
#     )
#
#     if response.message.tool_calls:
#       # There may be multiple tool calls in the response
#       for tool in response.message.tool_calls:
#         # Ensure the function is available, and then call it
#         if function_to_call := available_functions.get(tool.function.name):
#           print('Calling function:', tool.function.name)
#           print('Arguments:', tool.function.arguments)
#           output = function_to_call(**tool.function.arguments)
#           print('Function output:', output)
#         else:
#           print('Function', tool.function.name, 'not found')
#
#     # Only needed to chat with the model using the tool call results
#     if response.message.tool_calls:
#       # Add the function response to messages for the model to use
#       #messages.append(response.message)
#
#
#       messages.append({'role': 'tool', 'content': str(output), 'name': tool.function.name})
#
#       # Get final response from model with function outputs
#       final_response = chat('llama3.2:3b', messages=messages)
#       print('\nFinal response:\033[34m', final_response.message.content,"\033[0m")
#       messages.pop(len(messages)-1)
#     else:
#         final_response = chat('llama3.2:3b', messages=messages)
#         print('\nFinal response [NO TOOLS]:', final_response.message.content)
#
# """
#   TODO
# messages = [
#     {"role": "system", "content": "Je bent een assistent die altijd blij en enthousiast reageert."},
#     {"role": "user", "content": "Vertel me over het weer vandaag."}
# ]
# """
from ollama import chat
from ollama import ChatResponse
import ast
from Module_Query import handle_question

orientatie_q = ""

def askAboutFiles(questions: list) -> str:
    """
    Gebruik de bestanden om de vraag (vragen) van de gebruiker te beantwoorden
    retuns:
        requered_data (string): Bevat de benodigde bestanden om de vraag(vragen) van de gebruiker te beantwoorden
    """

    def string_to_list(input_string):
        try:
            # Verwijder witruimte aan de randen
            input_string = input_string.strip()
            # Converteer de string naar een lijst met ast.literal_eval voor veiligheid
            result = ast.literal_eval(input_string)
            # Controleer of de output daadwerkelijk een lijst is
            if isinstance(result, list):
                return result
            else:
                raise ValueError("De invoer is geen geldige lijst-string.")
        except Exception as e:
            return f"Fout bij het converteren: {e}"

    # Converteer de vraag naar een lijst
    resultaat = string_to_list(questions)
    if isinstance(resultaat, list) and len(resultaat) > 10:
        resultaat = [questions]  # In geval van te lange vragenlijst, stuur terug als één vraag

    print("Vragen: ", resultaat)
    # Verwerk de vragen door de externe functie handle_question aan te roepen
    requered_data = handle_question(resultaat)
    return requered_data

def dont_query(x):
    """
    Wanneer uit de prompt blijkt dat de bestanden bevragen niet nodig is of niet relevant is
    """
    return x

askAboutFiles_tool = {
    'type': 'function',
    'function': {
        'name': 'askAboutFiles',
        'description': (
            'Bevraag de bestanden om de vraag of vragen van de gebruiker te beantwoorden. '
            'Gebruik deze functie voor alle vragen die betrekking hebben op schoolgerelateerde onderwerpen zoals vakken, roosters, huiswerk, regels, klachtenregeling, schoolactiviteiten (zoals ouderavonden), '
            'en andere zaken die specifiek zijn voor de middelbare school Ashram Alphen. '
            'Zelfs als de vraag niet expliciet naar schoolgerelateerde zaken verwijst, veronderstel dat de vraag binnen dit domein valt en beantwoord deze door de bestanden te raadplegen. '
            'Verbeter de spelling NIET van de vraag en laat de vraag zoals deze is gesteld. Vertaal NOOIT de vraag(vragen) van de gebruiker.'
        ),
        'parameters': {
            'type': 'object',
            'required': ['questions'],
            'properties': {
                'questions': {
                    'type': 'list',
                    'description': 'De vraag(en) voor de bestanden'
                }
            }
        }
    }
}

dont_query_tool = {
    'type': 'function',
    'function': {
        'name': 'dont_query',
        'description': (
            'Bevraag de bestanden niet. Gebruik deze functie alleen als de vraag **absoluut niet** betrekking heeft op schoolgerelateerde onderwerpen zoals vakken, roosters, huiswerk, regels, klachtenregeling, '
            'of andere zaken die specifiek zijn voor de middelbare school Ashram Alphen. '
            'Dit zou het geval zijn bij algemene vragen die geen betrekking hebben op de school zelf of haar organisatie, bijvoorbeeld vragen over algemene informatie of persoonlijke zaken die buiten het schooldomein vallen.'
        ),
        'parameters': {
            'type': 'object',
            'required': ['x'],
            'properties': {
                'x': {
                    'type': 'str',
                    'description': 'De vraag die geen betrekking heeft op de school en dus niet de bestanden hoeft te raadplegen'
                }
            }
        }
    }
}

messages = [
    {"role": "system", "content": (
        "Je bent een digitale assistent van de middelbare school Ashram Alphen, en hebt toegang tot alle documenten en bestanden van de school. "
        "Wanneer iemand een vraag stelt die mogelijk betrekking heeft op schoolgerelateerde onderwerpen zoals vakken, roosters, huiswerk, regels, klachtenregeling, schoolactiviteiten (zoals ouderavonden), of andere zaken die specifiek zijn voor de school, "
        "moet je altijd de bestanden raadplegen om het juiste antwoord te geven. "
        "Zelfs als de vraag niet expliciet verwijst naar schoolgerelateerde zaken, veronderstel dan dat de vraag betrekking heeft op de school en gebruik de bestanden om een accuraat antwoord te geven. "
        "Je kunt deze functie ook gebruiken om toegang te krijgen tot de benodigde documenten en biedt vervolgens een nauwkeurig antwoord op basis van de gegevens in de schoolbestanden."
    )}
]

available_functions = {
    'askAboutFiles': askAboutFiles,
    'dont_query': dont_query
}

while True:
    content = input(">> ")

    messages.append({'role': 'user', 'content': content})
    response: ChatResponse = chat(
      'llama3.2:3b',
      messages=messages,
      tools=[askAboutFiles_tool, dont_query_tool],
    )

    if response.message.tool_calls:
        # Er kunnen meerdere functieaanroepen zijn in de respons
        for tool in response.message.tool_calls:
            # Zorg ervoor dat de functie beschikbaar is, en roep deze dan aan
            if function_to_call := available_functions.get(tool.function.name):
                print('Calling function:', tool.function.name)
                print('Arguments:', tool.function.arguments)
                output = function_to_call(**tool.function.arguments)
                print('Function output:', output)
            else:
                print('Function', tool.function.name, 'not found')

        # Voeg de output van de functie toe aan de berichten voor de modelantwoorden
        messages.append({'role': 'tool', 'content': str(output), 'name': tool.function.name})

        # Krijg het uiteindelijke antwoord van het model na het aanroepen van de functie
        final_response = chat('llama3.2:3b', messages=messages)
        print('\nFinal response:\033[34m', final_response.message.content,"\033[0m")
        messages.pop(len(messages)-1)
    else:
        final_response = chat('llama3.2:3b', messages=messages)
        print('\nFinal response [NO TOOLS]:', final_response.message.content)
