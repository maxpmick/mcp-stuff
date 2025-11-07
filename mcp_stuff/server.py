import json
from typing import Any, Dict, Mapping, Optional
from dotenv import load_dotenv
import requests
import os
from pathlib import Path
from urllib.parse import urljoin
from fastmcp import FastMCP

# Load env variables
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(ENV_PATH)

CANVAS_API_KEY = os.getenv("CANVAS_API_KEY", "null")
CANVAS_BASE_URL = os.getenv("CANVAS_BASE_URL", "null")
AUTH_HEADER = {"Authorization": f"Bearer {CANVAS_API_KEY}"}


GUARD_PREFIX = "while(1);"
JSONObj = Dict[str, Any]


def parse_response(response: requests.Response) -> JSONObj:
    payload = response.text.lstrip()
    if payload.startswith(GUARD_PREFIX):
        payload = payload[len(GUARD_PREFIX) :].lstrip()

    parsed = json.loads(payload)
    return parsed


def check_health(base_url: str, auth: Mapping) -> str:
    parsed = make_canvas_request(
        endpoint="users/self", base_url=base_url, auth_header=auth
    )
    pretty_response = json.dumps(parsed, indent=4)

    return pretty_response


def make_canvas_request(
    endpoint: str,
    params: Optional[Mapping[str, Any]] = None,
    *,
    base_url: str = CANVAS_BASE_URL,
    auth_header: Mapping[str, str] = AUTH_HEADER,
) -> JSONObj:
    url = urljoin(base_url, endpoint)
    response = requests.get(url, headers=auth_header, params=params)
    response.raise_for_status()

    parsed = parse_response(response)
    return parsed


# # Init MCP Server
# mcp = FastMCP("My MCP Server")


# @mcp.tool
# def greet(name: str) -> str:
#     return f"Hello, {name}!"


def main():
    print("Hello, testing authentication...\n")

    health = check_health(CANVAS_BASE_URL, AUTH_HEADER)

    print(health)


if __name__ == "__main__":
    # mcp.run(transport="http", port=8000)
    main()
