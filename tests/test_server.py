"""
Tests for Prosp MCP Server.

Uses FastMCP's in-process Client for testing without an external server.
"""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, patch

import pytest

# Set a dummy API key before importing server (it registers tools at import time)
import os
os.environ.setdefault("PROSP_API_KEY", "test-key-for-testing")

from prosp_mcp.server import mcp  # noqa: E402
from prosp_mcp.client import get_client  # noqa: E402


@pytest.fixture
def client_instance():
    """Get the global Prosp client."""
    return get_client()


class TestToolDiscovery:
    """Verify all expected tools are registered."""

    async def test_tools_registered(self):
        """Server should register add_lead, check_api_key, and get_server_info."""
        from fastmcp import Client

        async with Client(transport=mcp) as c:
            tools = await c.list_tools()
            tool_names = {t.name for t in tools}

            assert "add_lead" in tool_names
            assert "check_api_key" in tool_names
            assert "get_server_info" in tool_names
            assert len(tool_names) == 3

    async def test_get_server_info(self):
        """get_server_info should return valid JSON with server metadata."""
        from fastmcp import Client

        async with Client(transport=mcp) as c:
            result = await c.call_tool("get_server_info", {})
            data = json.loads(result.content[0].text)

            assert data["server"] == "prosp-mcp"
            assert data["version"] == "0.1.0"
            assert data["api_key_configured"] is True
            assert data["total_tools"] == 3


class TestCheckApiKey:
    """Tests for the check_api_key health check tool."""

    async def test_check_api_key_no_key(self):
        """Should report error when no API key is set."""
        from fastmcp import Client

        client = get_client()
        original_key = client._api_key
        client._api_key = None

        try:
            async with Client(transport=mcp) as c:
                result = await c.call_tool("check_api_key", {})
                data = json.loads(result.content[0].text)
                assert data["success"] is False
                assert "No API key" in data["error"]
        finally:
            client._api_key = original_key

    @patch("prosp_mcp.tools.leads.get_client")
    async def test_check_api_key_valid(self, mock_get_client):
        """Should report success when API key is valid."""
        from fastmcp import Client

        mock_client = AsyncMock()
        mock_client.has_api_key = True
        mock_client.post = AsyncMock(return_value={"status": "ok"})
        mock_get_client.return_value = mock_client

        async with Client(transport=mcp) as c:
            result = await c.call_tool("check_api_key", {})
            data = json.loads(result.content[0].text)
            assert data["success"] is True


class TestAddLead:
    """Tests for the add_lead tool."""

    @patch("prosp_mcp.tools.leads.get_client")
    async def test_add_lead_success(self, mock_get_client):
        """Should successfully add a lead with valid params."""
        from fastmcp import Client

        mock_client = AsyncMock()
        mock_client.post = AsyncMock(return_value={"id": "lead-123", "status": "added"})
        mock_get_client.return_value = mock_client

        async with Client(transport=mcp) as c:
            result = await c.call_tool("add_lead", {
                "params": {
                    "linkedin_url": "https://linkedin.com/in/testuser",
                    "list_id": "abc-123",
                    "campaign_id": "def-456",
                }
            })
            data = json.loads(result.content[0].text)
            assert data["success"] is True
            assert data["data"]["id"] == "lead-123"

    @patch("prosp_mcp.tools.leads.get_client")
    async def test_add_lead_api_error(self, mock_get_client):
        """Should return error response on API failure."""
        from fastmcp import Client

        mock_client = AsyncMock()
        mock_client.post = AsyncMock(side_effect=Exception("API returned 500"))
        mock_get_client.return_value = mock_client

        async with Client(transport=mcp) as c:
            result = await c.call_tool("add_lead", {
                "params": {
                    "linkedin_url": "https://linkedin.com/in/testuser",
                    "list_id": "abc-123",
                    "campaign_id": "def-456",
                }
            })
            data = json.loads(result.content[0].text)
            assert data["success"] is False
            assert "500" in data["error"]
