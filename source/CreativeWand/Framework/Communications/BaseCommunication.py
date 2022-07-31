"""
BaseCommunication.py

This file contains the base class BaseCommunication, an abstracted Communication.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
# Fix circular import on type hints.
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from CreativeWand.Framework.Communications.CommunicationGroupManager import CommunicationGroupManager
    from CreativeWand.Framework.ExperienceManager.BaseExperienceManager import BaseExperienceManager


class BaseCommunication(ABC):
    """
    an abstracted Communication.
    """

    def __init__(self, description=""):
        super(BaseCommunication, self).__init__()
        self.description = description
        """
        Description of this communication method.
        """
        self.manager = None
        """
        CommunicationManager this communication belong to.
        """

    def register_manager(self, manager: CommunicationGroupManager) -> None:
        """
        Associate this communication with a CommunicationGroupManager.
        :param manager: manager instance.
        :return: None
        """
        self.manager = manager

    def get_experience_manager(self) -> BaseExperienceManager:
        """
        Get the experience manager that this communication belong to.
        :return: Experiencemanager for this communication.
        """
        if self.manager is None:
            raise ValueError("Communication does not have manager binded.")
        return self.manager.get_experience_manager()

    @abstractmethod
    def can_activate(self) -> bool:
        """
        Providing the current context, is this communication available?
        :return: True if this communication is available.
        """
        pass

    @abstractmethod
    def activate(self) -> bool:
        """
        Activate this communication.
        :return: True if this operation is successful.
        """
        pass

    def confidence_to_activate(self) -> float:
        """
        How strong of a wish does this communication want to activate?
        :return: number from 0 to 1 while 1 means it really want to get activated.
        """
        if self.can_activate():
            return 1.0
        else:
            return 0.0

    def confidence_to_interrupt_activate(self) -> float:
        """
        How strong of a wish this communication wanna trigger with priority?
        :return: number from 0 to 1 while 1 means it really want to get activated.
        """
        return 0.0

    def suppress_interrupt(self):
        """
        Suppress possible interrupt from this communication.
        :return:
        """
        pass
