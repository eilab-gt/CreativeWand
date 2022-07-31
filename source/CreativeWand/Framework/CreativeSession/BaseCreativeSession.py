"""
BaseCreativeSession.py

=== This framework object is DEPRECATED.

This file contains the base class BaseCreativeSession which represents a whole process of human an AI collaborating on a document.
"""
from warnings import warn

from CreativeWand.Framework.ExperienceManager.BaseExperienceManager import BaseExperienceManager

from abc import ABC, abstractmethod


class BaseCreativeSession(ABC):
    """
    a whole process of human an AI collaborating on a document.
    """

    # Experience Manager that control this session
    manager: BaseExperienceManager

    # Recordings of this creative session, needed for replaying / analyzing.
    records: dict

    def __init_subclass__(cls, **kwargs):
        """This throws a deprecation warning on subclassing."""
        warn(f'{cls.__name__} will be deprecated.', DeprecationWarning, stacklevel=2)
        super().__init_subclass__(**kwargs)

    def __init__(self, manager: BaseExperienceManager):
        """
        Initialize this session object with reference to the experience manager.
        :param manager: experience manager to bind to.
        """

        warn(f'{self.__class__.__name__} will be deprecated.', DeprecationWarning, stacklevel=2)
        self.manager = manager
        self.records = {"log": [], "meta": {}}

    @abstractmethod
    def record_log_item(self, log_item) -> None:
        """
        Add a log item to the records.
        :param log_item: Log items to be added.
        :return: None
        """
        pass

    @abstractmethod
    def start_session(self) -> None:
        """
        Start the creative session.
        :return: None
        """
        pass

    @abstractmethod
    def end_session(self):
        """
        End the current session and trigger end session activities.
        :return:
        """
        pass
