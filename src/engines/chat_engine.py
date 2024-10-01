"""
ChatEngine: A class designed to facilitate conversation using a language model.
"""
import re
import json
from typing import List
from llama_index.llms.openai import OpenAI

from src.prompt.instruction_prompt import (PROMPT,
                                           CONVERSATION_TRACKING,
                                           REASONING_PROMPT)
from src.prompt.funny_chat_prompt import PROMPT_FUNNY_FLOW
from src.storage.weaviatedb import WeaviateDB
from src.repositories.suggestion_repository import SuggestionRepository


class ChatEngine:
    """
    A class to generate responses for user queries using a language model and manage conversations.
    """

    def __init__(
        self,
        prompt_template: str = PROMPT,
        language_model: OpenAI = None,
        complex_model: OpenAI = None,
        weaviate_db: WeaviateDB = None,
        suggestion_repository: SuggestionRepository = None
    ):
        """
        Initializes the ChatEngine with a prompt template, language model, and Weaviate database.

        Args:
            prompt_template (str): Template for formatting prompts.
            language_model (OpenAI): The language model for generating responses.
            weaviate_db (WeaviateDB): The Weaviate database instance for storing suggestions.
        """
        self._prompt_template = prompt_template
        self._language_model = language_model
        self._complex_model = complex_model
        self._weaviate_dbs = weaviate_db
        self._suggestion_repository = suggestion_repository

    async def generate_response(
        self,
        user_query: str,
        relevant_information: List[str],
        history: str
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
            query=user_query,
            history=history
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
            query (str): The user's query.

        Returns:
            str: The humorous response.
        """
        prompt = PROMPT_FUNNY_FLOW.format(query=query)
        response = await self._language_model.acomplete(prompt)
        nodes = await self._weaviate_dbs.suggestion_config(
            question=query,
            answer=response.text
        )
        await self._weaviate_dbs.insert_suggestion_nodes(nodes=nodes)
        self._suggestion_repository.add_suggestion(
            question=query,
            answer=response.text
        )
        return response.text

    async def conversation_tracking(
        self,
        history: str,
        query: str
    ) -> str:
        """
        """
        prompt = CONVERSATION_TRACKING.format(
            history=history,
            query=query
        )
        response = await self._complex_model.acomplete(prompt)
        try:
            string_processed = re.sub(r"```json|```", "", response.text)
            print(string_processed)
            query_processed = json.loads(string_processed)
        except json.JSONDecodeError as e:
            print("JSON Error:", e)
            query_processed = query
        return query_processed

    async def reasoning_query(
        self,
        query: str,
        context: str,
        history: str
    ) -> str:
        """
        """
        prompt = REASONING_PROMPT.format(
            query=query,
            context=context,
            history=history
        )
        response = await self._complex_model.acomplete(prompt)
        return response.text
