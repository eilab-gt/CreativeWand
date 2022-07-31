"""
AddonServer.py

This file contains a simple interface for setting up API calls
for addon tools to be used by the Application.
"""
from __future__ import annotations

from importlib import import_module

from flask import Flask, request, make_response, jsonify, json
from CreativeWand.Addons.AddonConfig import tool_config

"""
Internal variables.
"""
app = Flask(__name__)

tools = {}

# Common class prefix appended to every tool definition to find them
# In Addons/Toolbox folder.
tool_common_prefix = "CreativeWand.Addons.Toolbox."


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/api/<name>", methods=["POST"])
def call_api(name: str):
    data = request.data
    try:
        data = json.loads(data)
    except:
        return make_response(
            jsonify({"message": "Invalid Input"}),
            400,
        )
    print("%s is called with data %s." % (name, data))
    if name not in tools:
        return make_response(
            jsonify({"message": "Unknown Tools"}),
            404,
        )
    else:
        print(tools[name])
        result = tools[name]['object'](data)
        print(result)
        return make_response(
            jsonify(result),
            200,
        )


if __name__ == '__main__':

    import sys

    tools_to_enable = None
    if len(sys.argv) > 1:
        print("Received list of tools, will only enable these tools.")
        tools_to_enable = sys.argv[1:]

    # Load config file and use them to load tools needed for the server.
    for k, v in tool_config.items():

        if tools_to_enable is not None and k not in tools_to_enable:
            print("Skipping loading tool %s." % k)
            continue

        filename = v['file']
        classname = v['class']

        if 'config' in v:
            config = v['config']
        else:
            config = None
        if 'func' in v:
            funcname = v['func']
            if funcname is not None:
                print("WARNING - funcname is not supported yet. Only __call__() will be used.")
        else:
            funcname = None
        python_filepath = tool_common_prefix + filename
        module = import_module(python_filepath)
        tool_class = getattr(module, classname)

        if config:
            tool_object = tool_class(config)
        else:
            tool_object = tool_class()
        tools[k] = {
            "object": tool_object,
            "func": funcname,
        }
    print("Loaded tool objects: %s" % tools)

    app.run(host="0.0.0.0")
