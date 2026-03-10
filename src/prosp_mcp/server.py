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
import signal
import sys
from typing import Any

from fastmcp import FastMCP

from .client import get_client, set_api_key
from .tools import get_all_tools, get_requested_categories, is_lazy_loading_enabled

# Server metadata
SERVER_NAME = "prosp-mcp"
SERVER_VERSION = "0.2.0"
SERVER_INSTRUCTIONS = """Prosp.ai LinkedIn Automation MCP Server.

Manage LinkedIn outreach: leads, campaigns, messaging, and analytics.

Categories:
- leads: add, remove, delete, list leads; check API key
- campaigns: list, start, stop campaigns; get analytics
- messaging: send messages, voice notes; get conversations

Use check_api_key first to verify your connection.
"""

# Initialize FastMCP server with production settings
mcp = FastMCP(
    name=SERVER_NAME,
    version=SERVER_VERSION,
    instructions=SERVER_INSTRUCTIONS,
    on_duplicate="error",
    mask_error_details=True,
    strict_input_validation=True,
)

# Tool annotations keyed by function name
TOOL_ANNOTATIONS: dict[str, dict[str, Any]] = {
    # Leads — read
    "check_api_key": {"readOnlyHint": True},
    "get_leads_in_campaign": {"readOnlyHint": True},
    "get_lead_stage": {"readOnlyHint": True},
    # Leads — write
    "add_lead": {"destructiveHint": False},
    "add_lead_to_list": {"destructiveHint": False},
    "add_existing_lead_to_campaign": {"destructiveHint": False},
    "remove_lead_from_campaign": {"destructiveHint": True, "confirmationRequiredHint": True},
    "delete_lead": {"destructiveHint": True, "confirmationRequiredHint": True},
    # Campaigns — read
    "get_all_campaigns": {"readOnlyHint": True},
    "get_campaign_status": {"readOnlyHint": True},
    "get_analytics": {"readOnlyHint": True},
    # Campaigns — write
    "start_campaign": {"destructiveHint": False, "confirmationRequiredHint": True},
    "stop_campaign": {"destructiveHint": True, "confirmationRequiredHint": True},
    # Messaging — write
    "send_message": {"destructiveHint": False, "confirmationRequiredHint": True},
    "send_voice_message": {"destructiveHint": False, "confirmationRequiredHint": True},
    # Messaging — read
    "get_conversation": {"readOnlyHint": True},
}

TOOL_META: dict[str, dict[str, Any]] = {
    # Leads
    "add_lead": {"title": "Add Lead to List & Campaign", "tags": {"leads", "write"}},
    "add_lead_to_list": {"title": "Add Lead to List", "tags": {"leads", "write"}},
    "add_existing_lead_to_campaign": {"title": "Add Existing Lead to Campaign", "tags": {"leads", "write"}},
    "remove_lead_from_campaign": {"title": "Remove Lead from Campaign", "tags": {"leads", "write"}},
    "delete_lead": {"title": "Delete Lead from Workspace", "tags": {"leads", "write"}},
    "get_leads_in_campaign": {"title": "Get Leads in Campaign", "tags": {"leads", "read"}},
    "get_lead_stage": {"title": "Get Lead Stage", "tags": {"leads", "read"}},
    "check_api_key": {"title": "Check API Key", "tags": {"health", "read"}},
    # Campaigns
    "get_all_campaigns": {"title": "Get All Campaigns", "tags": {"campaigns", "read"}},
    "get_campaign_status": {"title": "Get Campaign Status", "tags": {"campaigns", "read"}},
    "start_campaign": {"title": "Start Campaign", "tags": {"campaigns", "write"}},
    "stop_campaign": {"title": "Stop Campaign", "tags": {"campaigns", "write"}},
    "get_analytics": {"title": "Get Analytics", "tags": {"campaigns", "read"}},
    # Messaging
    "send_message": {"title": "Send LinkedIn Message", "tags": {"messaging", "write"}},
    "send_voice_message": {"title": "Send Voice Message", "tags": {"messaging", "write"}},
    "get_conversation": {"title": "Get Conversation", "tags": {"messaging", "read"}},
}


def register_tools():
    """Register all tools with MCP annotations."""
    tools = get_all_tools()

    for tool_func in tools:
        tool_name = tool_func.__name__
        annotations = TOOL_ANNOTATIONS.get(tool_name, {})
        meta = TOOL_META.get(tool_name, {})
        mcp.tool(
            name=tool_name,
            title=meta.get("title"),
            tags=meta.get("tags"),
            annotations=annotations,
        )(tool_func)

    print(f"[Prosp MCP] Registered {len(tools)} tools", file=sys.stderr)


# Register tools at import time
register_tools()


@mcp.tool(
    name="get_server_info",
    title="Get Server Info",
    tags={"health", "read"},
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
