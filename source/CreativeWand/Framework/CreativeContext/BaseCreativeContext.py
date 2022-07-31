"""
BaseCreativeContext.py

This file contains the base class BaseCreativeContext, a representation for content generator interface.
"""

from abc import ABC, abstractmethod


class ContextQuery:
    """
    A query embedding a dict used to get specific information from a CreativeContext.
    """

    def __init__(self):
        # Query content
        self.query = {}


class BaseCreativeContext(ABC):
    """
    An abstracted generator context.
    """

    @abstractmethod
    def get_generated_content(self) -> object:
        """
        Get the content currently generated.
        :return: The content generated.
        """

        pass

    @abstractmethod
    def execute_query(self, query: ContextQuery) -> object:
        """
        Get information from CreativeContext using a query.
        :param query: query specifying what to find.
        :return: Query result.
        """

        pass