"""
WebFrontend.py

Describes the prototype interface the creative wand uses to get/present information.
"""

from CreativeWand.Framework.Frontend.BaseFrontEnd import BaseFrontend, BaseRequest


class WebFrontend(BaseFrontend):
    def __init__(self, server_object, id):
        super().__init__()
        self.server_obj = server_object
        # self.send_chat_message = send_chat_message
        # self.send_object = send_object
        self.id = id

    @BaseFrontend.save_logs
    def get_information(self, request: BaseRequest) -> object:
        msg = self.server_obj.send_chat_message(request.message, self.id, wait=True)
        if request.cast_to is not None:
            msg = request.cast_to(msg)
        return msg

    @BaseFrontend.save_logs
    def send_information(self, info: BaseRequest):
        self.server_obj.send_chat_message(info.message, self.id, wait=False)

    def set_information(self, info: object):
        raise NotImplementedError("This frontend does not support user providing information without a request.")
        pass

    @BaseFrontend.save_logs
    def set_doc(self, doc: dict):
        # self.send_object(doc, sketch, self.id)
        obj = {}
        if "id" in doc:
            raise AttributeError("Conflicting keys for set_doc; id")
        for key in doc:
            obj[key] = doc[key]
        obj["id"] = self.id
        self.server_obj.send_object(event="document", obj=obj)
        # self.send_object(event='document', obj={"document": doc, "sketch": sketch, "id": self.id})

    def send_kill_to_react(self):
        print("Attemptiong to kill react session %s" % self.id)
        self.server_obj.send_object(event="kill_session", obj={"id": self.id})
