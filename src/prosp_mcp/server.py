"""
Prosp MCP Server — Main Server

A FastMCP server for the Prosp.ai LinkedIn automation API.

Usage:
  # stdio mode (local Claude Desktop / Claude Code)
  prosp-mcp

  # With API key override
  prosp-mcp --api-key YOUR_KEY
"""

from __future__ import annotations

import json
import os
import signal
import sys
from typing import Any

from fastmcp import FastMCP

from .client import get_client, set_api_key
from .tools import get_all_tools, get_requested_categories, is_lazy_loading_enabled

# Server metadata
SERVER_NAME = "prosp-mcp"
SERVER_VERSION = "0.1.0"
SERVER_INSTRUCTIONS = """Prosp.ai LinkedIn Automation MCP Server.

Manage LinkedIn outreach leads and campaigns programmatically.

Tools: add_lead, check_api_key, get_server_info

Use check_api_key first to verify your connection before adding leads.
"""

# Initialize FastMCP server
mcp = FastMCP(
    name=SERVER_NAME,
    version=SERVER_VERSION,
    instructions=SERVER_INSTRUCTIONS,
)


def register_tools():
    """Register all tools with MCP annotations."""
    tools = get_all_tools()

    TOOL_ANNOTATIONS: dict[str, dict[str, Any]] = {
        "add_lead": {"destructiveHint": False},
        "check_api_key": {"readOnlyHint": True},
    }

    for tool_func in tools:
        tool_name = tool_func.__name__
        annotations = TOOL_ANNOTATIONS.get(tool_name, {})
        mcp.tool(name=tool_name, annotations=annotations)(tool_func)

    print(f"[Prosp MCP] Registered {len(tools)} tools", file=sys.stderr)


# Register tools at import time
register_tools()


@mcp.tool(
    name="get_server_info",
    annotations={"readOnlyHint": True},
)
async def get_server_info() -> str:
    """Get Prosp MCP server version, config status, and loaded tools."""
    client = get_client()
    categories = get_requested_categories()

    info = {
        "server": SERVER_NAME,
        "version": SERVER_VERSION,
        "api_key_configured": client.has_api_key,
        "lazy_loading_enabled": is_lazy_loading_enabled(),
        "loaded_categories": categories,
        "total_tools": len(get_all_tools()) + 1,  # +1 for get_server_info
    }

    return json.dumps(info, indent=2)


def _handle_shutdown(signum: int, frame: Any) -> None:
    """Handle graceful shutdown."""
    print(f"\n[Prosp MCP] Shutting down (signal {signum})", file=sys.stderr)
    sys.exit(0)


def main():
    """Main entry point for the Prosp MCP server."""
    import argparse

    # Graceful shutdown
    signal.signal(signal.SIGINT, _handle_shutdown)
    signal.signal(signal.SIGTERM, _handle_shutdown)

    parser = argparse.ArgumentParser(description="Prosp MCP Server")
    parser.add_argument(
        "--api-key",
        help="Prosp API key (overrides PROSP_API_KEY env var)",
    )

    args = parser.parse_args()

    if args.api_key:
        set_api_key(args.api_key)

    client = get_client()
    print(f"[Prosp MCP] Starting server v{SERVER_VERSION}", file=sys.stderr)
    print(
        f"[Prosp MCP] API key: {'configured' if client.has_api_key else 'NOT SET'}",
        file=sys.stderr,
    )

    if not client.has_api_key:
        print(
            "[Prosp MCP] WARNING: No API key set. Set PROSP_API_KEY or use --api-key",
            file=sys.stderr,
        )

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
