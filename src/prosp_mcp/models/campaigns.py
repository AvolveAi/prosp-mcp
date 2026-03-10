"""Pydantic models for campaign operations."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CampaignIdInput(BaseModel):
    """Input requiring just a campaign ID."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="ignore")

    campaign_id: str = Field(
        ..., description="Prosp campaign UUID"
    )


class GetAnalyticsInput(BaseModel):
    """Input for getting analytics data."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="ignore")

    campaign_id: Optional[str] = Field(
        default=None, description="Prosp campaign UUID (omit for workspace-level analytics)"
    )
