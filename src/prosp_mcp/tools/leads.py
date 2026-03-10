"""
Prosp MCP Server — Lead Tools

Tools for managing leads in Prosp campaigns and lists.
"""

from __future__ import annotations

import json

from fastmcp.exceptions import ToolError

from ..client import get_client
from ..models.leads import (
    AddExistingLeadToCampaignInput,
    AddLeadInput,
    AddLeadToListInput,
    DeleteLeadInput,
    GetLeadsInCampaignInput,
    GetLeadStageInput,
    RemoveLeadFromCampaignInput,
)


def _require_key():
    client = get_client()
    if not client.has_api_key:
        raise ToolError(
            "API key not configured. Use check_api_key to diagnose, "
            "or set PROSP_API_KEY environment variable."
        )
    return client


async def add_lead(params: AddLeadInput) -> str:
    """Add a lead to a Prosp contact list and campaign by LinkedIn URL."""
    client = _require_key()

    body = {
        "linkedin_url": params.linkedin_url,
        "list_id": params.list_id,
        "campaign_id": params.campaign_id,
    }
    if params.data is not None:
        body["data"] = params.data

    try:
        result = await client.post("/leads", json=body)
        return json.dumps({"success": True, "data": result}, indent=2)
    except Exception as e:
        raise ToolError(f"Failed to add lead: {e}") from e


async def add_lead_to_list(params: AddLeadToListInput) -> str:
    """Add a lead to a contact list only (no campaign assignment)."""
    client = _require_key()

    body = {"linkedin_url": params.linkedin_url, "list_id": params.list_id}
    if params.data is not None:
        body["data"] = params.data

    try:
        result = await client.post("/leads/list", json=body)
        return json.dumps({"success": True, "data": result}, indent=2)
    except Exception as e:
        raise ToolError(f"Failed to add lead to list: {e}") from e


async def add_existing_lead_to_campaign(params: AddExistingLeadToCampaignInput) -> str:
    """Add an existing lead (already in workspace) to a campaign."""
    client = _require_key()

    body = {
        "linkedin_url": params.linkedin_url,
        "campaign_id": params.campaign_id,
    }

    try:
        result = await client.post("/leads/campaign", json=body)
        return json.dumps({"success": True, "data": result}, indent=2)
    except Exception as e:
        raise ToolError(f"Failed to add lead to campaign: {e}") from e


async def remove_lead_from_campaign(params: RemoveLeadFromCampaignInput) -> str:
    """Remove a lead from a campaign (lead stays in workspace)."""
    client = _require_key()

    body = {
        "linkedin_url": params.linkedin_url,
        "campaign_id": params.campaign_id,
    }

    try:
        result = await client.post("/leads/campaign/remove", json=body)
        return json.dumps({"success": True, "data": result}, indent=2)
    except Exception as e:
        raise ToolError(f"Failed to remove lead from campaign: {e}") from e


async def delete_lead(params: DeleteLeadInput) -> str:
    """Permanently delete a lead from the workspace."""
    client = _require_key()

    body = {"linkedin_url": params.linkedin_url}

    try:
        result = await client.post("/leads/delete", json=body)
        return json.dumps({"success": True, "data": result}, indent=2)
    except Exception as e:
        raise ToolError(f"Failed to delete lead: {e}") from e


async def get_leads_in_campaign(params: GetLeadsInCampaignInput) -> str:
    """Get all leads in a campaign with optional pagination."""
    client = _require_key()

    body = {"campaign_id": params.campaign_id}
    if params.page is not None:
        body["page"] = params.page
    if params.limit is not None:
        body["limit"] = params.limit

    try:
        result = await client.post("/leads/campaign/list", json=body)
        return json.dumps({"success": True, "data": result}, indent=2)
    except Exception as e:
        raise ToolError(f"Failed to get leads: {e}") from e


async def get_lead_stage(params: GetLeadStageInput) -> str:
    """Get the current stage of a lead in a campaign."""
    client = _require_key()

    body = {
        "linkedin_url": params.linkedin_url,
        "campaign_id": params.campaign_id,
    }

    try:
        result = await client.post("/leads/stage", json=body)
        return json.dumps({"success": True, "data": result}, indent=2)
    except Exception as e:
        raise ToolError(f"Failed to get lead stage: {e}") from e


async def check_api_key() -> str:
    """Verify the Prosp API key is valid and the API is reachable."""
    client = get_client()

    if not client.has_api_key:
        raise ToolError(
            "No API key configured. Set PROSP_API_KEY environment variable "
            "or pass --api-key on startup."
        )

    try:
        await client.post("/leads", json={"linkedin_url": "", "list_id": "", "campaign_id": ""})
        return json.dumps({"success": True, "message": "API key is valid."}, indent=2)
    except Exception as e:
        error_str = str(e)
        if "401" in error_str or "403" in error_str or "unauthorized" in error_str.lower():
            raise ToolError(
                "Invalid API key. Check your key at https://prosp.ai/settings"
            ) from e
        if isinstance(e, (ConnectionError, TimeoutError)):
            raise ToolError(f"Cannot reach Prosp API: {e}") from e
        # 400/422 means auth worked but request invalid — that's a pass
        return json.dumps({"success": True, "message": "API key is valid."}, indent=2)


LEAD_TOOLS = [
    add_lead,
    add_lead_to_list,
    add_existing_lead_to_campaign,
    remove_lead_from_campaign,
    delete_lead,
    get_leads_in_campaign,
    get_lead_stage,
    check_api_key,
]
