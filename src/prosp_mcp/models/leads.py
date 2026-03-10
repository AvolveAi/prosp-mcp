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


class AddLeadToListInput(BaseModel):
    """Input for adding a lead to a contact list only."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="ignore")

    linkedin_url: str = Field(
        ..., description="Lead's full LinkedIn profile URL"
    )
    list_id: str = Field(
        ..., description="Prosp list UUID"
    )
    data: Optional[list[dict[str, Any]]] = Field(
        default=None, description="Optional custom field mapping"
    )


class AddExistingLeadToCampaignInput(BaseModel):
    """Input for adding an existing lead to a campaign."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="ignore")

    linkedin_url: str = Field(
        ..., description="Lead's full LinkedIn profile URL"
    )
    campaign_id: str = Field(
        ..., description="Prosp campaign UUID"
    )


class RemoveLeadFromCampaignInput(BaseModel):
    """Input for removing a lead from a campaign."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="ignore")

    linkedin_url: str = Field(
        ..., description="Lead's full LinkedIn profile URL"
    )
    campaign_id: str = Field(
        ..., description="Prosp campaign UUID"
    )


class DeleteLeadInput(BaseModel):
    """Input for deleting a lead from the workspace."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="ignore")

    linkedin_url: str = Field(
        ..., description="Lead's full LinkedIn profile URL"
    )


class GetLeadStageInput(BaseModel):
    """Input for getting current stage of a lead in a campaign."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="ignore")

    linkedin_url: str = Field(
        ..., description="Lead's full LinkedIn profile URL"
    )
    campaign_id: str = Field(
        ..., description="Prosp campaign UUID"
    )


class GetLeadsInCampaignInput(BaseModel):
    """Input for getting all leads in a campaign."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="ignore")

    campaign_id: str = Field(
        ..., description="Prosp campaign UUID"
    )
    page: Optional[int] = Field(
        default=None, description="Page number for pagination"
    )
    limit: Optional[int] = Field(
        default=None, description="Number of leads per page"
    )
