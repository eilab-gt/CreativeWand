"""
Sample.py

A sample simple tool, that its __call__() is used when handling requests.
"""


class SampleTool:
    def __call__(self, body):
        return body  # echoing
