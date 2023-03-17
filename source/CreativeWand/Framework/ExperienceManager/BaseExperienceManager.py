"""
BaseExperienceManager.py

Describe the base experience manager.

A Frontend will be in charge of using this manager, so this manager is passive.

Three main functions are used to activate suitable communications, both from human
and agent side:

(1) interrupt_activate(): This is used mainly when human wish to communication in an idle state;
(2) wish_to_interupt_with_preferred(): This is used for expressing the intent for the agent to follow up with a communication. (Counterpart of (1))
(3) activate_preferred(): This is used to actually let the agent start a communication.

Note that even if (2) is False meaning that the agent does not want to interrupt,
it doesn't mean that the agent does not have a preferred interaction;
Indeed, suggestions can be implemented using this, so that the suggestions are not forced to be shown
to a human designer, but when they request the agent to "say something" they get the suggestions.

"""
import datetime, os
from copy import deepcopy

import deepdiff
from deepdiff import DeepDiff

from CreativeWand.Framework.Communications.BaseCommunication import BaseCommunication
from CreativeWand.Framework.Communications.CommunicationGroupManager import CommunicationGroupManager
from abc import ABC, abstractmethod

from CreativeWand.Framework.CreativeContext.BaseCreativeContext import BaseCreativeContext
from CreativeWand.Framework.Frontend.BaseFrontEnd import BaseFrontend

from typing import Union, Type

from CreativeWand.Utils.Misc.FileUtils import write_obj, relative_path


class BaseExperienceManager(ABC):
    """
    Base Experience Manager abstract class.
    """



    # Bookkeeping variables.
    session_id: str
    session_code: str
    session_type: str

    # region init

    def __init__(
            self,
            creative_context: BaseCreativeContext = None,
            frontend: BaseFrontend = None,
            info: dict = None,
    ):
        """
        Initialize this experience manager.
        :param creative_context: creative context it binds to.
        :param frontend: frontend it interact with.
        :param info: any additional info for bookkeeping.
            may contain:
            session_id - UUID of the session;
            session_code - external code of the session;
            session_type - type of the experiment carrying out.
        """

        self.frontend = frontend
        """
        Frontend this experience manager use to communicate.
        """

        self.history_states = []

        self.state = {}
        self.log_items = []
        self.session_ended = False

        # default place to save logs, related to file util script
        self.default_log_location = relative_path("../../../logs")
        # default_log_location = "/"

        """
        State this experience manager is keeping.
        """

        self.creative_context: BaseCreativeContext

        self._fill_session_info(info=info)

        if creative_context is not None:
            self.bind_creative_context(creative_context=creative_context)

        self.comm_group_manager = CommunicationGroupManager()
        """
        Communication group manager this experience manager is using.
        """
        self.comm_group_manager.bind_experience_manager(self)

    def bind_frontend(self, frontend: Type[BaseFrontend]):
        """
        Bind a frontend (or substitute a binded one).
        :param frontend: frontend to (re)bind.
        :return: None.
        """
        if self.frontend is not None:
            print("ExperienceManager: Frontend is going to be re-binded.")
        self.frontend = frontend

    def _fill_session_info(self, info: dict):
        """
        Fill in session info from the `info` parameter. Used when initializing.
        :param info: info parameter.
        :return: None.
        """
        self.info = info

        self.created_at = datetime.datetime.now().strftime("%b%d%H%M%S")

        if info is not None and 'session_id' in info:
            self.session_id = info['session_id']
        else:
            self.session_id = "local_noid"

        if info is not None and 'session_type' in info:
            self.session_type = info['session_type']
        else:
            self.session_type = "local_notype"

        if info is not None and 'session_code' in info:
            self.session_code = info['session_code']
        else:
            self.session_code = "local_nocode"

        if info is not None and 'session_mode' in info:
            self.session_mode = info['session_mode']
        else:
            self.session_mode = "MODE_UNKNOWN"

    # endregion init

    # region atomic actions

    def register_communication(self, communication: BaseCommunication) -> bool:
        """
        Register a communication so that the experience manager can use it.
        :param communication: Communication instance.
        :return: whether the operation succeeds.
        """
        self.comm_group_manager.bind_communication(communication)

    def bind_creative_context(self, creative_context: BaseCreativeContext) -> bool:
        """
        Bind a creative context to this experience manager.
        :param creative_context: context to bind to.
        :return: whether the operation succeeds.
        """
        self.creative_context = creative_context
        return True

    @abstractmethod
    def get_list_of_available_communications_for_user(self) -> list:
        """
        Present a list of available communications that can be initiated by the user.
        One use case is to allow user to give information when AI does not want to (yet).
        :return: List of available communications.
        """
        pass

    @abstractmethod
    def interrupt_activate(self, comm: BaseCommunication) -> bool:
        """
        Activate a specific communication.
        :param comm: Communication to be activated.
        :return: Whether this operation is successful.
        """
        pass

    @abstractmethod
    def wish_to_interrupt_with_preferred(self) -> BaseCommunication:
        """
        Return whether this experience manager wish to initiate a preferred communication.
        :return: None if this is not the case, or the communication object if it is to be activated.
        """
        pass

    @abstractmethod
    def activate_preferred(self) -> bool:
        """
        Activate a communication that is preferred by this experience manager.
        :return: Whether this operation is successful.
        """
        pass

    def set_state(self, key: str, value: object) -> None:
        """
        Set the state of the finite state machine to a specific value.
        These values can be later extracted using get_state.
        Note that communications are allowed to change them too!
        :param key: key of the state.
        :param value: value of the state, or None to unset the key.
        :return: None.
        """
        if value is not None:
            self.state[key] = value
        else:
            del self.state[key]

    def get_state(self, key: str) -> object:
        """
        Get the staet of the finite state machine.
        If that state value does not exist yet, return None.
        :param key:
        :return: state value, or None if that value does not exist yet.
        """
        if key not in self.state:
            return None
        return self.state[key]

    def trigger_event(self, event_name: str) -> bool:
        """
        "Trigger" an event so that it can be consumed later.
        :param event_name: Name of the event.
        :return: Whether this event got registered. False if it's already registered before.
        """
        internal_name = "__event__%s" % event_name
        if self.get_state(internal_name):
            return False
        self.set_state(internal_name, True)
        return True

    def consume_event(self, event_name: str, peek: bool = False) -> bool:
        """
        "Consume" an event so that it is removed.
        :param event_name: name of the event.
        :param peek: Whether to just check and not actually consume the event.
        :return: True if the event is consumed, False if this event does not exist at all.
        """
        internal_name = "__event__%s" % event_name
        if self.get_state(internal_name):
            if not peek:
                self.set_state(internal_name, None)
                return True
            else:
                return True
        else:
            return False

    # region Undo

    def save_state_checkpoint(self) -> bool:
        """
        Save a checkpoint of the state.
        :return: whether state is updated.
        """
        self.set_state("_cc_state_", self.creative_context.get_state_for_checkpoint())
        if len(self.history_states) == 0:
            self.history_states.append(deepcopy(self.state))
            return True
        else:
            last_element = self.history_states[-1]
            diff = deepdiff.DeepDiff(last_element, self.state)
            if len(diff.keys()) > 0:
                print("Detected changes, saving a checkpoint...")
                self.history_states.append(deepcopy(self.state))
                return True
            else:
                print("Detected no changes, skipping saving states...")
                # no change, do nothing
                return False

    def get_state_dump(self) -> dict:
        """
        Get the current state, but not applying any after effects that `save_state_checkpoint()` may have.
        :return: the newest state.
        """
        result = deepcopy(self.state)
        result["_cc_state_"] = self.creative_context.get_state_for_checkpoint()
        return result

    def can_undo_state(self) -> bool:
        """
        Return whether undo is possible.
        :return: True if possible.
        """
        # We need at least 2 checkpoints so we can recover to one before (minus one just saved)
        print(f"UNDO STACK SIZE:{len(self.history_states)}")
        return len(self.history_states) > 1

    def undo_state(self):
        """
        Reverse the state to the last one saved.
        :return: Whether the operation is successful.
        """
        if self.can_undo_state():
            self.history_states.pop()  # This is a copy of the current state
            self.state = deepcopy(self.history_states[-1])  # This is the one we wanna go back to
            old_cc_state = self.get_state("_cc_state_")
            self.creative_context.set_state_from_checkpoint(old_cc_state)
            return True
        else:
            return False

    # endregion Undo

    def suppress_all_interrupts(self):
        """
        call suppress interrupts on comm manager.
        :return: Whether operation is successful.
        """
        return self.comm_group_manager.suppress_all_interrupts()

    # endregion atomic actions

    # region Logging

    def add_log_item(self, log_item: Union[dict, object]):
        """
        Add a log item to the log storage of this manager.
        :param log_item: log item to add.
        :return: None
        """
        now = datetime.datetime.now()
        current_time = now.strftime("%m/%d/%Y, %H:%M:%S.%f")
        current_timestamp = now.timestamp()
        result = log_item
        if type(log_item) is dict and 'time' not in log_item:
            result['time'] = current_time
            result['timestamp'] = current_timestamp
        elif type(log_item) is not dict:
            result = {"time": current_time, "timestamp": current_timestamp, "obj": log_item}
        self.log_items.append(result)

    def save_logs(self, path: str = None):
        """
        Save the log stored in the frontend to a file.
        :return: None
        """
        full_logs = {
            "session_id": self.session_id,
            "session_type": self.session_type,
            "session_code": self.session_code,
            "session_mode": self.session_mode,
            "session_ended": self.session_ended,
            "created_at": self.created_at,
            "version": "2022.12.21.2",
            "frontend_logs": self.frontend.logs,
            "manager_logs": self.log_items,
        }
        if path is None:
            path = self.default_log_location
        os.makedirs(path + f"/log-{self.session_mode}", exist_ok=True)
        log_path = path + f"/log-{self.session_mode}/session-{self.session_code}-{self.created_at}.json"
        # print("Attempting to save logs to log path %s" % log_path)
        write_obj(log_path, full_logs)
        print("Saved logs to %s" % log_path)

    # endregion Logging

    # region session management

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
        End the current session and do cleanup.
        :return:
        """
        pass

    # endregion session management
