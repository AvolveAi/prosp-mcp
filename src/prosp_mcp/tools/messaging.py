"""
Prosp MCP Server — Messaging Tools

Tools for LinkedIn messaging via Prosp.
"""

from __future__ import annotations

import json

from fastmcp.exceptions import ToolError

from ..client import get_client
from ..models.messaging import GetConversationInput, SendMessageInput, SendVoiceInput


def _require_key():
    client = get_client()
    if not client.has_api_key:
        raise ToolError(
            "API key not configured. Use check_api_key to diagnose, "
            "or set PROSP_API_KEY environment variable."
        )
    return client


async def send_message(params: SendMessageInput) -> str:
    """Send a LinkedIn message to a profile."""
    client = _require_key()

    body = {
        "linkedin_url": params.linkedin_url,
        "message": params.message,
    }
    if params.campaign_id is not None:
        body["campaign_id"] = params.campaign_id

    try:
        result = await client.post("/messages/send", json=body)
        return json.dumps({"success": True, "data": result}, indent=2)
    except Exception as e:
        raise ToolError(f"Failed to send message: {e}") from e


async def send_voice_message(params: SendVoiceInput) -> str:
    """Send a LinkedIn voice message to a profile."""
    client = _require_key()

    body = {"linkedin_url": params.linkedin_url}
    if params.campaign_id is not None:
        body["campaign_id"] = params.campaign_id

    try:
        result = await client.post("/messages/voice", json=body)
        return json.dumps({"success": True, "data": result}, indent=2)
    except Exception as e:
        raise ToolError(f"Failed to send voice message: {e}") from e


async def get_conversation(params: GetConversationInput) -> str:
    """Get the LinkedIn conversation history with a lead."""
    client = _require_key()

    body = {"linkedin_url": params.linkedin_url}

    try:
        result = await client.post("/conversations", json=body)
        return json.dumps({"success": True, "data": result}, indent=2)
    except Exception as e:
        raise ToolError(f"Failed to get conversation: {e}") from e


MESSAGING_TOOLS = [
    send_message,
    send_voice_message,
    get_conversation,
]
