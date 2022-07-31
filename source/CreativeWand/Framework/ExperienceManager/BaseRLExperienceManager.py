"""
BaseRLExperienceManager.py

Describe an extension of base experience manager with regard to Reinforcement Learning agents.

Extends BaseExperienceManager with interfaces to be used with a gym env.
"""
import warnings
from abc import ABC, abstractmethod
from typing import Union
import gym
import numpy as np
from gym import spaces

from CreativeWand.Framework.CreativeContext.BaseCreativeContext import BaseCreativeContext
from CreativeWand.Framework.ExperienceManager.BaseExperienceManager import BaseExperienceManager
from CreativeWand.Framework.Frontend.BaseFrontEnd import BaseFrontend


class BaseRLExperienceManager(BaseExperienceManager, ABC):

    def __init__(self,
                 creative_context: BaseCreativeContext = None,
                 frontend: BaseFrontend = None,
                 info: dict = None,
                 rl_agent_mode: str = "enjoy",
                 rl_agent_info: dict = None,
                 ):
        """
        Initialize this experience manager.
        :param creative_context: passed to base init.
        :param frontend: passed to base init.
        :param info: passed to base init.
        :param rl_agent_mode: mode the agent should run in, for example "train" or "enjoy".
        :param rl_agent_info: information needed to set up the RL agent.
        """
        super().__init__(creative_context=creative_context,
                         frontend=frontend,
                         info=info)

        self.rl_agent_info = rl_agent_info
        self.rl_agent_mode = rl_agent_mode

    # region RL setup

    """
    Although some of the functions here is abstract we nevertheless
    provided some reference implementation to demonstrate its intended usages.
    """

    @abstractmethod
    def _reset(self):
        """
        Reset this environment, killing CreativeSession associated early.
        :return: None.
        """
        pass

    @abstractmethod
    def _get_action_list(self) -> list:
        """
        Get a list of actions. This is also used to determine the dimension of action space.
        This implementation assumes each communication get one and only one entry; This can be customized
        in inherited classes.
        :return: list of actions.
        """
        result = self.comm_group_manager.get_all_communications()
        result.append("Dummy_EndSession")  # hack to allow session ending actions.
        return result

    @abstractmethod
    def _get_current_observation(self, and_then_render=False) -> np.array:
        """
        Returns (generates) observation for the RL agent, under current situations.
        (Depending on when it is called can be before step() or after step().
        :param and_then_render: Once observation is created, render it. (Reserved interface)
        :return: current observation in np.array.
        """
        warnings.warn(
            "BaseRLExperienceManager: _get_current_observation() returning dummy obs. Implement this in the inherited class.")
        return np.zeros(1)

    @abstractmethod
    def _get_info(self) -> dict:
        """
        Get information that needs to append to gym env step returns.
        :return: info for gym environment.
        """
        return {}

    @abstractmethod
    def _execute_action_with_idx(self, idx) -> object:
        """
        Execute a given action with a certain index.
        This "base" implementation uses info from _get_action_list()
        but this can be customized in inherited classes.
        :param idx: index of the action.
        :return: result of this action.
        """
        list_of_actions = self._get_action_list()
        if idx == len(list_of_actions) - 1:  # last action, is EndSession
            return self._get_current_observation(), self._get_reward_by_last_action(), True, self._get_info()
        else:
            # Execute actions
            action_result = self.comm_group_manager.get_all_communications()[idx].activate()
            return self._get_current_observation(), self._get_reward_by_last_action(), False, self._get_info()

    @abstractmethod
    def _get_reward_by_last_action(self) -> float:
        """
        Grant rewards to the action just executed.
        :return: reward of the last action.
        """
        warnings.warn(
            "BaseRLExperienceManager: _get_reward_by_last_action() always returning 0. Implement this in the inherited class.")
        return 0

    @abstractmethod
    def _predict_next_action_under_observation(self, obs, mode="index") -> Union[np.array, int]:
        """
        Used when training is over, use the underlying model,
        what would be the best action to take
        :param obs: observation.
        :param mode: what to return ("index" or "logits").
        :return: single action index for "index" or logits array for "logits".
        """
        pass

    def _create_env(self):
        """
        Create a gym environment based on this experience manager, and
        save it to self.env .
        :return: created env object.
        """

        # save a copy of the reference as self is going to be shadowed
        outer_self = self

        class CreativeWandWrappedEnv(gym.Env):
            def reset(self):
                outer_self._reset()

            def render(self, mode="human"):
                outer_self._get_current_observation(and_then_render=True)

            def step(self, action):
                outer_self._execute_action_with_idx(action)

            def __init__(self):
                self.observation_shape = outer_self._get_current_observation().shape
                self.observation_space = spaces.Box(low=np.zeros(self.observation_shape),
                                                    high=np.ones(self.observation_shape),
                                                    dtype=np.float16)

                self.action_space = spaces.Discrete(len(outer_self._get_action_list()), )

        self.env = CreativeWandWrappedEnv()
        return self.env

    # endregion
