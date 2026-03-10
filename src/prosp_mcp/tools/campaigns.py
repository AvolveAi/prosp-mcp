"""
Prosp MCP Server — Campaign Tools

Tools for managing campaigns in Prosp.
"""

from __future__ import annotations

import json

from fastmcp.exceptions import ToolError

from ..client import get_client
from ..models.campaigns import CampaignIdInput, GetAnalyticsInput


def _require_key():
    client = get_client()
    if not client.has_api_key:
        raise ToolError(
            "API key not configured. Use check_api_key to diagnose, "
            "or set PROSP_API_KEY environment variable."
        )
    return client


async def get_all_campaigns() -> str:
    """Get all campaigns in the workspace."""
    client = _require_key()

    try:
        result = await client.post("/campaigns", json={})
        return json.dumps({"success": True, "data": result}, indent=2)
    except Exception as e:
        raise ToolError(f"Failed to get campaigns: {e}") from e


async def get_campaign_status(params: CampaignIdInput) -> str:
    """Get the current status of a campaign."""
    client = _require_key()

    try:
        result = await client.post("/campaigns/status", json={"campaign_id": params.campaign_id})
        return json.dumps({"success": True, "data": result}, indent=2)
    except Exception as e:
        raise ToolError(f"Failed to get campaign status: {e}") from e


async def start_campaign(params: CampaignIdInput) -> str:
    """Start a campaign. Campaign must be in a startable state."""
    client = _require_key()

    try:
        result = await client.post("/campaigns/start", json={"campaign_id": params.campaign_id})
        return json.dumps({"success": True, "data": result}, indent=2)
    except Exception as e:
        raise ToolError(f"Failed to start campaign: {e}") from e


async def stop_campaign(params: CampaignIdInput) -> str:
    """Stop a running campaign."""
    client = _require_key()

    try:
        result = await client.post("/campaigns/stop", json={"campaign_id": params.campaign_id})
        return json.dumps({"success": True, "data": result}, indent=2)
    except Exception as e:
        raise ToolError(f"Failed to stop campaign: {e}") from e


async def get_analytics(params: GetAnalyticsInput) -> str:
    """Get analytics data for a campaign or the entire workspace."""
    client = _require_key()

    body = {}
    if params.campaign_id is not None:
        body["campaign_id"] = params.campaign_id

    try:
        result = await client.post("/analytics", json=body)
        return json.dumps({"success": True, "data": result}, indent=2)
    except Exception as e:
        raise ToolError(f"Failed to get analytics: {e}") from e


CAMPAIGN_TOOLS = [
    get_all_campaigns,
    get_campaign_status,
    start_campaign,
    stop_campaign,
    get_analytics,
]
