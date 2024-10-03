from typing import List, Optional
from openai_client import OpenAI
import json
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion import ChatCompletion
import logging
from modules.detailed_book.detailed_book import DetailedBookServices

logger = logging.getLogger(__name__)

class StudyPlanWritter:

    def __init__(self, openai_client: OpenAI) -> None:
        self.openai_client = openai_client
        self.messages : List[ChatCompletionMessageParam] = [
            {
                "role": "system",
                "content": "Monte uma trilha de estudo com livros da biblioteca o'reilly com base na necessidade do usuário",
            },
        ]

    def generate_study_plan(self, requirements: str) -> str:

        message : ChatCompletionMessageParam = {
            "role": "user",
            "content": requirements,
        }

        response = self.send(message)

        if not response.choices[0].message.tool_calls:
            logger.error("Não foi possível gerar a trilha de estudo pois não houve chamadas de ferramentas")
            return "Não foi possível gerar a trilha de estudo"

        for call in response.choices[0].message.tool_calls:
            arguments = json.loads(call.function.arguments)
            book_query = arguments.get('query')

            result = DetailedBookServices.get_detailed_book(book_query)

            function_call_result_message : ChatCompletionMessageParam = {
                "role": "tool",
                "content": json.dumps({
                    "result": str(result)
                }),
                "tool_call_id": call.id
            }

            self.messages.append(function_call_result_message)

        response = self.send()

        if not response.choices[0].message.content:
            logger.error("Não foi possível gerar a trilha de estudo pois não houve conteúdo na resposta")
            return "Não foi possível gerar a trilha de estudo"

        return response.choices[0].message.content

    def extend_messages(self, messages: List[ChatCompletionMessageParam]) -> None:
        self.messages.extend(messages)
    
    def send(self, message: Optional[ChatCompletionMessageParam] = None) -> ChatCompletion:

        if message:
            self.messages.append(message)

        for msg in self.messages:
            logger.debug(f"Message: {msg}")

        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=self.messages,
            temperature=1,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "get_book_data",
                        "description": "Get a O'Really Book",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "The name of the book, or topic",
                                }
                            },
                            "additionalProperties": False,
                            "required": ["query"],
                        },
                        "strict": True,
                    },
                }
            ],
            response_format={"type": "text"},
        )

        self.messages.append(response.choices[0].message) # type: ignore

        return response
