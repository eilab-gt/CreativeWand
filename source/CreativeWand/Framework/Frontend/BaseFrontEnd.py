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

    def __init__(self, message="", cast_to: type = None):
        """
        Build a request object.
        :param message: Message to be used when presenting this request.
        :param cast_to: If requesting information, the information should be casted in this format.
        """
        self.message = message
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
            self.logs.append(
                {
                    "id": self.seq_id,
                    "time": current_time,
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
