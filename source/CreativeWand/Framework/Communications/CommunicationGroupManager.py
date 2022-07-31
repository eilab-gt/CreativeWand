"""
CommunicationGroupManager.py

This file describes a manager that manages all communications available to external agent.
"""
from __future__ import annotations

from CreativeWand.Framework.Communications.BaseCommunication import BaseCommunication

# Fix circular import on type hints.
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from CreativeWand.Framework.ExperienceManager.BaseExperienceManager import BaseExperienceManager


class CommunicationGroupManager:
    """
    This class holds Communications up.
    """

    def __init__(self):
        self._communications = []
        self._exp_manager = None

    def bind_experience_manager(self, exp_manager: BaseExperienceManager) -> None:
        """
        Set the experience manager context of this manager
        :param exp_manager: manager context.
        :return:
        """
        self._exp_manager = exp_manager

    def get_experience_manager(self) -> BaseExperienceManager:
        """
        Get the experience manager binded to this manager.
        :return: experience manager.
        """
        return self._exp_manager

    def bind_communication(self, comm: BaseCommunication) -> None:
        """
        Register a communication and set up its context.
        :param comm: communication to set up.
        :return:
        """
        comm.register_manager(self)
        self._communications.append(comm)

    def get_available_communications(self, threshold=0.5) -> list:
        """
        Return a list of available communications.
        :param threshold: If a comm says a confidence higher than this then it can be activated.
        :return: list of available communications at this context.
        """
        result = []
        for comm in self._communications:
            if comm.confidence_to_activate() > threshold:
                result.append(comm)
        return result

    def get_all_communications(self) -> List[BaseCommunication]:
        """
        Return a list of all communications whether they are available.
        :return: list of all communications.
        """
        return self._communications

    def get_interrupt_communications(self) -> list:
        """
        Return a list of available communications that wish to interrupt.
        :return: list of available communications to interrupt at this context.
        """
        result = []
        for comm in self._communications:
            if comm.confidence_to_interrupt_activate() > 0.5:
                result.append(comm)
        return result

    def suppress_all_interrupts(self) -> bool:
        """
        Suppress all interrupts from all communications.
        :return: Whether operation is successful.
        """
        for comm in self._communications:
            comm.suppress_interrupt()
        return True
