"""
BaseCapability.py

This file describes "capabilites", or what a creative context can support.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from CreativeWand.Framework.CreativeContext.BaseCreativeContext import BaseCreativeContext


class BaseCapability:
    def __init__(self, parent: Type[BaseCreativeContext]):
        """
        Initialize this capability by adding a link to its parent CreativeContext.
        :param parent: parent creative context.
        """
        self.parent = parent

    @abstractmethod
    def __call__(self, *args, **kwargs):
        """
        Use this capability.
        :param args:
        :param kwargs:
        :return:
        """
        pass
