"""Pydantic models for messaging operations."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SendMessageInput(BaseModel):
    """Input for sending a LinkedIn message."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="ignore")

    linkedin_url: str = Field(
        ..., description="Lead's full LinkedIn profile URL"
    )
    message: str = Field(
        ..., description="Message text to send"
    )
    campaign_id: Optional[str] = Field(
        default=None, description="Prosp campaign UUID (optional context)"
    )


class SendVoiceInput(BaseModel):
    """Input for sending a LinkedIn voice message."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="ignore")

    linkedin_url: str = Field(
        ..., description="Lead's full LinkedIn profile URL"
    )
    campaign_id: Optional[str] = Field(
        default=None, description="Prosp campaign UUID (optional context)"
    )


class GetConversationInput(BaseModel):
    """Input for getting a conversation from LinkedIn."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="ignore")

    linkedin_url: str = Field(
        ..., description="Lead's full LinkedIn profile URL"
    )
