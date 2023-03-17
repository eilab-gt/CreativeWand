"""
CommunicationGroupManager.py

This file describes a manager that manages all communications available to external agent.
"""
from __future__ import annotations

import operator

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

    def get_available_communications(self, threshold=0.5, sort_by="confidence") -> list:
        """
        Return a list of available communications.
        :param threshold: The threshold of determining how much confidence is needed to be included.
        :param sort_by: confidence | description: The criteria for sorting the communications.
        :return: list of available communications at this context.
        """

        comms_by_sort_key = {}
        for comm in self._communications:
            confidence = comm.confidence_to_activate()
            description = comm.description
            if confidence > threshold:
                if sort_by == "confidence":
                    comms_by_sort_key[comm] = -confidence  # As we sort in reverse
                elif sort_by == "description":
                    comms_by_sort_key[comm] = description

        # Sort comms
        sorted_cbc = sorted(comms_by_sort_key.items(), key=operator.itemgetter(1))

        # Then only take the comms
        sorted_cbc = list(x[0] for x in sorted_cbc)

        return sorted_cbc

    def get_all_communications(self) -> List[BaseCommunication]:
        """
        Return a list of all communications whether they are available.
        :return: list of all communications.
        """
        return self._communications

    def get_interrupt_communications(self, threshold=0.5) -> list:
        """
        Return a list of available communications that wish to interrupt.
        :param threshold: The threshold of determining how much confidence is needed to be included.
        :return: list of available communications that wants to interrupt at this context.
        """
        comms_by_confidence = {}
        for comm in self._communications:
            confidence = comm.confidence_to_interrupt_activate()
            if confidence > threshold:
                comms_by_confidence[comm] = confidence
        # Sort comms by confidence
        sorted_cbc = sorted(comms_by_confidence.items(), key=operator.itemgetter(1), reverse=True)

        # Then only take the comms
        sorted_cbc = list(x[0] for x in sorted_cbc)

        return sorted_cbc

    def suppress_all_interrupts(self) -> bool:
        """
        Suppress all interrupts from all communications.
        :return: Whether operation is successful.
        """
        for comm in self._communications:
            comm.suppress_interrupt()
        return True
