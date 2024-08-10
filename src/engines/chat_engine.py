"""
ChatEngine: A class designed to facilitate conversation using a language model.
"""

from typing import List
from llama_index.llms.openai import OpenAI

from src.prompt.instruction_prompt import PROMPT
from src.prompt.funny_chat_prompt import PROMPT_FUNNY_FLOW


class ChatEngine:
    """
    ChatEngine is a class that utilizes a language model (LLM) to generate
    responses based on a given prompt template and user query.

    Attributes:
        _prompt_template (str): The template used to format the prompt.
        _llm (OpenAI): An instance of the OpenAI language model for generating responses.
    """

    def __init__(
        self,
        prompt_template: str = PROMPT,
        language_model: OpenAI = None
    ):
        """
        Initializes a new instance of the ChatEngine class.

        Args:
            prompt_template (str): The template for formatting the prompt.
            language_model (OpenAI): An instance of the OpenAI 
                                    language model for generating responses.
        """
        self._prompt_template = prompt_template
        self._language_model = language_model

    async def generate_response(
        self,
        user_query: str,
        relevant_information: List[str]
    ) -> str:
        """
        Generates a response to a user query using the language model.

        Args:
            user_query (str): The user's query.
            relevant_information (List[str]): A list of relevant information or context nodes.
            query (str): The user's query.
            retrieved_nodes (List[str]): A list of relevant information or context nodes.

        Returns:
            str: The generated response from the language model.
        """
        prompt = self._prompt_template.format(
            context=relevant_information,
            query=user_query
        )
        response = await self._language_model.acomplete(prompt)
        return response.text

    async def funny_chat(
        self,
        query: str
    ) -> str:
        """
        Generates a humorous response based on the user's query.

        Args:
            query (str): The input query from the user.

        Returns:
            str: A humorous response generated by the language model.
        """
        prompt = PROMPT_FUNNY_FLOW.format(query=query)
        response = await self._language_model.acomplete(prompt)
        return response.text
