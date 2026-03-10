"""Pydantic models for lead operations."""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class AddLeadInput(BaseModel):
    """Input for adding a lead to a Prosp list and campaign."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="ignore")

    linkedin_url: str = Field(
        ..., description="Lead's full LinkedIn profile URL"
    )
    list_id: str = Field(
        ..., description="Prosp list UUID (from the list URL in Prosp UI)"
    )
    campaign_id: str = Field(
        ..., description="Prosp campaign UUID (from the campaign URL in Prosp UI)"
    )
    data: Optional[list[dict[str, Any]]] = Field(
        default=None, description="Optional custom field mapping"
    )
