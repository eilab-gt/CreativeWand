"""
AddonServer.py

This file contains a simple interface for setting up API calls
for addon tools to be used by the Application.
"""
from __future__ import annotations

from importlib import import_module

from flask import Flask, request, make_response, jsonify, json
from CreativeWand.Addons.AddonConfig import tool_config as default_tool_config
import inspect

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


def run_addon_server(tools_to_enable=None, tool_config=None):
    """
    Start the addon server.
    tool_config should be in this format:
        "pnb": { # Name of the tool (matched with `tools_to_enable`)
            "class": PNBTool, # A class that has __call__(self, body) => return_value
            "config": { # They are directly passed as `config` parameter for `__init__()`
                "key1": "value1",
                "key2": "value2",
            }
        },
    :param tools_to_enable: (list) if not None, will ignore any tool in `tool_config` that is not in it.
    :param tool_config: (dict) tool config dictionary (see main comment)

    :return:
    """
    import sys
    if tools_to_enable is None:
        if len(sys.argv) > 1:
            print("Using arguments from command line, will only enable these tools.")
            tools_to_enable = sys.argv[1:]

    if tool_config is None:
        tool_config = default_tool_config

    # Load config file and use them to load tools needed for the server.
    for k, v in tool_config.items():

        # If "external-name" is set in tool config, use that name instead. Otherwise use entry name.
        tool_external_name = v['external-name'] if 'external-name' in v else k

        if tools_to_enable is not None and k not in tools_to_enable:
            print("Skipping loading tool %s." % k)
            continue

        filename = v['file'] if 'file' in v else None
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

        if inspect.isclass(classname):
            tool_class = classname
        elif type(classname) is str:
            # Creating using str - Will only work with specific dir structure, deprecated
            python_filepath = tool_common_prefix + filename
            module = import_module(python_filepath)
            tool_class = getattr(module, classname)
        else:
            raise AttributeError("classname not a str or class: %s" % classname)

        if config:
            tool_object = tool_class(config)
        else:
            tool_object = tool_class()
        if tool_external_name in tools:
            raise AttributeError("Trying to create two services with the same external name: %s !" % tool_external_name)
        tools[tool_external_name] = {
            "object": tool_object,
            "func": funcname,
        }
    print("Loaded tool objects: %s" % tools)

    app.run(host="0.0.0.0", port=8765)


if __name__ == '__main__':
    run_addon_server()
