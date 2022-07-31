"""
endpoint.py

Endpoint for Plug & Blend Tool.
"""
from CreativeWand.Addons.Toolbox.CARP.carp_service.carp import CARPWorkflow


class CARPTool:
    def __init__(self, config):
        self.workflow = CARPWorkflow(config)

    def __call__(self, body):
        if "stories" not in body or "reviews" not in body:
            raise AttributeError("Bad request.")
        return self.workflow(stories=body['stories'], reviews=body["reviews"])
