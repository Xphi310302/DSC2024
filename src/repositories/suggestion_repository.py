"""
This module provides a repository class for managing suggestions
"""

from src.storage.suggestion_crud import CRUDSuggestionCollection
from src.models.suggestion import Suggestion
from src.utils.utility import (create_new_id,
                               get_datetime)


class SuggestionRepository:
    """
    A repository for managing suggestion data.
    """

    def __init__(
        self
    ):
        """
        Initialize the SuggestionRepository.
        """
        self.collection = CRUDSuggestionCollection()
        self.data = self.load_all_data()

    def load_all_data(self):
        """
        Load all documents from the collection.

        Args:
            None

        Returns:
            list: A list of documents with '_id' field as a string.
        """
        self.data = list(self.collection.find_all_doc())
        for doc in self.data:
            doc['_id'] = str(doc['_id'])
        return self.data

    def add_one_record(
        self,
        suggestion: Suggestion = None
    ) -> None:
        """
        Insert a single suggestion record into the collection.

        Args:
            file (File): A `suggestion` instance containing the data to be inserted.

        Returns:
            None
        """
        self.collection.insert_one_doc(suggestion.__dict__)

    def add_suggestion(
        self,
        question: str = None,
        answer: str = None
    ) -> None:
        """
        Add a new suggestion to the collection.

        Args:
            question (str, optional): The question part of the suggestion.
            answer (str, optional): The answer part of the suggestion.

        Returns:
            None
        """
        suggestion_id = create_new_id(prefix="suggestion")
        timestamp = get_datetime()
        suggestion_instance = Suggestion(
            Id=suggestion_id,
            question=question,
            answer=answer,
            time=timestamp
        )
        self.add_one_record(
            suggestion=suggestion_instance
        )

    def delete_suggestion_by_id(
        self,
        suggestion_id: str = None
    ) -> None:
        """
        Delete a suggestion from the collection by its ID.

        Args:
            suggestion_id (str, optional): The unique ID of the suggestion 

        Returns:
            None

        Raises:
            Exception: If an error occurs during the deletion process
        """
        try:
            result = self.collection.delete_one_doc({'Id': suggestion_id})
            if result.deleted_count > 0:
                print(
                    f"Suggestion with id = {suggestion_id} deleted successfully.")
            else:
                print(f"No suggestion with id = {suggestion_id} found.")
        except Exception as e:
            print(
                f"Error deleting suggestion with id = {suggestion_id}: {e}")
            raise

    def get_suggestion_by_question(
        self,
        suggestion_question: str = None
    ) -> str:
        """
        Retrieve a suggestion by its question.

        Args:
            suggestion_question (str, optional): The question

        Returns:
            dict: A dictionary containing the suggestion document
        """
        document = self.collection.find_one_doc(
            {
                'question': suggestion_question
            }
        )
        if document:
            document["_id"] = str(document["_id"])
        return document
