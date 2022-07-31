"""
CreativeContextConfig.py

Configurations (default values, etc.) used by creative contexts.

Environment specific: need to change them for installation.

"""

available_configs = {
    "sample":
        {
            "default_server_addr": "http://localhost:5000",
            "generate_api_route": "/api/pnb-gptj",
        },
    "local":
        {
            "default_server_addr": "http://localhost:5000",
            "generate_api_route": "/api/pnb"
        }
}

available_carp_configs = {
    "local":
        {
            "default_server_addr": "http://localhost:5000",
            "carp_api_route": "/api/carp"
        }
}

"""
Legacy.
"""
default_server_addr = "http://localhost:5000"
generate_api_route = "/api/pnb"

# Use rp(...) for model locations.
highlighter_model_path = ""  # /encoder/infersent%s.pkl
highlighter_w2v_path = ""  # fastText/crawl-300d-2M.vec
