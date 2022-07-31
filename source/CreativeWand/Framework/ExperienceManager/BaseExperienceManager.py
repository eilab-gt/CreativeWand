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

from CreativeWand.Framework.Communications.BaseCommunication import BaseCommunication
from CreativeWand.Framework.Communications.CommunicationGroupManager import CommunicationGroupManager
from abc import ABC, abstractmethod

from CreativeWand.Framework.CreativeContext.BaseCreativeContext import BaseCreativeContext
from CreativeWand.Framework.Frontend.BaseFrontEnd import BaseFrontend

from typing import Union

from CreativeWand.Utils.Misc.FileUtils import write_obj, relative_path


class BaseExperienceManager(ABC):
    """
    Base Experience Manager abstract class.
    """

    # default place to save logs, related to file util script
    default_log_location = relative_path("../../../logs")

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

        self.state = {}
        self.log_items = []
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
    def wish_to_interrupt_with_preferred(self) -> bool:
        """
        Return whether this experience manager wish to initiate a preferred communication.
        :return: Whether this is the case.
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
        :param value: value of the state.
        :return: None.
        """
        self.state[key] = value

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

    def refresh_state(self):
        """
        Request the experience manager to refresh states, if necessary.
        Used if something has to always keep fresh but we still want to lazy update them.
        :return:
        """
        pass

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
        now = datetime.now()
        current_time = now.strftime("%m/%d/%Y, %H:%M:%S.%f")
        result = log_item
        if type(log_item) is dict and 'time' not in log_item:
            result['time'] = current_time
        elif type(log_item) is not dict:
            result = {"time": current_time, "obj": log_item}
        self.log_items.append(result)

    def save_logs(self):
        """
        Save the log stored in the frontend to a file.
        :return: None
        """
        full_logs = {
            "session_id": self.session_id,
            "session_type": self.session_type,
            "session_code": self.session_code,
            "created_at": self.created_at,
            "version": "2022.06.08.1",
            "frontend_logs": self.frontend.logs,
            "manager_logs": self.log_items,
        }
        os.makedirs(self.default_log_location + "/log-%s" % self.session_type, exist_ok=True)
        log_path = self.default_log_location + "/log-%s/session-%s-%s.json" % (
            self.session_type, self.session_code, self.created_at)
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
