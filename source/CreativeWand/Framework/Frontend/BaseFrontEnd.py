"""
BaseFrontend.py

Describes the prototype interface the creative wand uses to get/present information.
"""
from abc import ABC, abstractmethod
from datetime import datetime


class BaseRequest:
    """
    A request carrying information to be transferred between user and agent.
    """

    def __init__(self, message="", info=None, cast_to: type = None):
        """
        Build a request object.
        :param message: Message to be used when presenting this request.
        :param info: any other info this request will carry.
        :param cast_to: If requesting information, the information should be casted in this format.
        """
        if info is None:
            info = {}
        self.message = message
        self.info = info
        self.cast_to = cast_to
        """
        Message to be printed to the screen, as revealed information or input request.
        """

    def __str__(self):
        return self.message


class BaseFrontend(ABC):
    """
    Base class of Frontend.
    """

    def __init__(self):
        """
        Initialize this Frontend.
        """
        self.logs = []
        self.seq_id = 0

        # Used for storing internal states unique to the frontend.
        self.state = {}

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
        :param key: key in the state.
        :return: state value, or None if that value does not exist yet.
        """
        if key not in self.state:
            return None
        return self.state[key]

    def set_log_keywords(self, keywords):
        """
        Set keywords to highlight in logs.
        :param keywords:
        :return:
        """
        self.log_keywords = keywords

    @staticmethod
    def save_logs(func):
        """
        Create a decorated function that save operational logs to the frontend.
        :param func: function to decorate.
        :return: decorated function.
        """

        def decorated_func(self, *args, **kwargs) -> object:
            name = func.__name__
            returned = func(self, *args, **kwargs)
            request = {}
            pos_arg_idx = 0
            for item in args:
                request["args%s" % pos_arg_idx] = str(item)
                pos_arg_idx += 1
            for key in kwargs:
                request[key] = str(kwargs[key])
            now = datetime.now()
            current_time = now.strftime("%m/%d/%Y, %H:%M:%S.%f")
            current_timestamp = now.timestamp()
            self.logs.append(
                {
                    "id": self.seq_id,
                    "time": current_time,
                    "timestamp": current_timestamp,
                    "type": name,
                    "args0": str(request['args0']) if 'args0' in request else "",
                    "request": request,
                    "returned": str(returned),
                }
            )

            self.seq_id += 1
            # print(self.logs)
            return returned

        return decorated_func

    def save_logs_manually(self, event_type="misc", request: list = None):
        """
        Write a log object manually.
        :param event_type: type of event, that will be recorded as `type` key in the logs.
        :param request: will be recorded as `request` key.
        :return: None
        """
        if request is None:
            request = []
        contents = {}
        now = datetime.now()
        current_time = now.strftime("%m/%d/%Y, %H:%M:%S.%f")
        current_timestamp = now.timestamp()
        contents["id"] = self.seq_id
        contents["time"] = current_time
        contents["timestamp"] = current_timestamp
        contents["type"] = event_type
        contents["args0"] = ""
        contents["request"] = request
        self.logs.append(contents)
        self.seq_id += 1

    @abstractmethod
    def get_information(self, request: object) -> object:
        """
        Request information from this frontend.
        :param request: Information describing this request.
        :return: Requested information.
        """
        pass

    @abstractmethod
    def send_information(self, info: object):
        """
        Deliver information to this frontend.
        :param info: Information to present to the frontend.
        :return: None.
        """
        pass

    @abstractmethod
    def set_information(self, info: object):
        """
        When user give information in the frontend, deliver it to backend.
        This information is not initially asked by the AI, hence
        it's not replying to a request.
        :param info: Information that is retrieved from user.
        :return: None.
        """
        pass
