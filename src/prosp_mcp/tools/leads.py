"""
Prosp MCP Server — Lead Tools

Tools for managing leads in Prosp campaigns and lists.
"""

from __future__ import annotations

import json
from typing import Any, Optional

from ..client import get_client
from ..models.leads import AddLeadInput


async def add_lead(params: AddLeadInput) -> str:
    """Add a lead to a Prosp list and campaign by LinkedIn URL."""
    client = get_client()

    body: dict[str, Any] = {
        "linkedin_url": params.linkedin_url,
        "list_id": params.list_id,
        "campaign_id": params.campaign_id,
    }

    if params.data is not None:
        body["data"] = params.data

    try:
        result = await client.post("/leads", json=body)
        return json.dumps(
            {"success": True, "data": result, "message": "Lead added successfully"},
            indent=2,
        )
    except ValueError as e:
        return json.dumps(
            {
                "success": False,
                "error": str(e),
                "message": "API key not configured. Use check_api_key to diagnose.",
            },
            indent=2,
        )
    except Exception as e:
        return json.dumps(
            {"success": False, "error": str(e), "message": "Failed to add lead"},
            indent=2,
        )


async def check_api_key() -> str:
    """Verify the Prosp API key is valid and the API is reachable."""
    client = get_client()

    if not client.has_api_key:
        return json.dumps(
            {
                "success": False,
                "error": "No API key configured",
                "message": "Set PROSP_API_KEY environment variable or pass --api-key on startup.",
            },
            indent=2,
        )

    try:
        # Use a minimal POST to /leads with invalid data to test auth
        # A 400 (bad request) means auth worked; 401/403 means bad key
        await client.post("/leads", json={"linkedin_url": "", "list_id": "", "campaign_id": ""})
        return json.dumps(
            {"success": True, "message": "API key is valid. Prosp API is reachable."},
            indent=2,
        )
    except Exception as e:
        error_str = str(e)
        # Auth errors
        if "401" in error_str or "403" in error_str or "Unauthorized" in error_str.lower():
            return json.dumps(
                {
                    "success": False,
                    "error": "Invalid API key",
                    "message": "The API key was rejected. Check your key at https://prosp.ai/settings",
                },
                indent=2,
            )
        # Connection errors mean API is down or unreachable
        if isinstance(e, (ConnectionError, TimeoutError)):
            return json.dumps(
                {
                    "success": False,
                    "error": str(e),
                    "message": "Cannot reach Prosp API. Check your network connection.",
                },
                indent=2,
            )
        # Any other error (including 400/422) means auth worked but request was invalid
        # which is expected since we sent empty data — that's a pass
        return json.dumps(
            {"success": True, "message": "API key is valid. Prosp API is reachable."},
            indent=2,
        )


# Export list for category loader
LEAD_TOOLS = [add_lead, check_api_key]
