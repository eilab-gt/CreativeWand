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

    def __init__(self):
        self.state = {}

    def reset(self):
        """
        Reset the internal state of this Creative Context.
        :return: None
        """
        self.state = {}

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

    # region state management

    def set_state(self, key: str, value: object) -> None:
        """
        Set the state to a specific value.
        These values can be later extracted using get_state.
        Note that communications are allowed to change them too!
        :param key: key of the state.
        :param value: value of the state.
        :return: None.
        """
        self.state[key] = value

    def get_state(self, key: str) -> object:
        """
        Get the state using a key.
        If that state value does not exist yet, return None.
        :param key:
        :return: state value, or None if that value does not exist yet.
        """
        if key not in self.state:
            return None
        return self.state[key]

    def get_state_for_checkpoint(self) -> dict:
        """
        Returns the state dictionary. Can be used later to recover the states.
        :return: The state dictionary.
        """
        return self.state

    def set_state_from_checkpoint(self, state: dict) -> bool:
        """
        Replaces current state with one given.
        This can be used when state has to be overwritten (ex. from history)
        :param state: the new state.
        :return: Whether operation is successful.
        """
        self.state = state
        return True

    # endregion state management
