"""
Prosp MCP Server — API Client

HTTP client for the Prosp.ai API v1.
Key difference from most APIs: auth key goes in the JSON request body, not headers.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Optional

import httpx

# API Configuration
PROSP_API_URL = "https://prosp.ai/api/v1"
DEFAULT_TIMEOUT = 30.0


@dataclass
class ProspClient:
    """
    HTTP client for Prosp.ai API v1.

    Auth: API key is injected into the JSON request body (Prosp's pattern).
    """

    _api_key: Optional[str] = field(default=None, repr=False)

    def __post_init__(self):
        if not self._api_key:
            self._api_key = os.environ.get("PROSP_API_KEY")

    @property
    def has_api_key(self) -> bool:
        """Check if an API key is configured."""
        return bool(self._api_key)

    def set_api_key(self, api_key: str) -> None:
        """Set API key programmatically."""
        self._api_key = api_key

    async def request(
        self,
        method: str,
        endpoint: str,
        *,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
        api_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        """
        Make an authenticated request to the Prosp API.

        The API key is injected into the JSON body for POST requests
        (Prosp's auth pattern — not header-based).
        """
        use_api_key = api_key or self._api_key
        if not use_api_key:
            raise ValueError(
                "Prosp API key is required. Set PROSP_API_KEY environment variable "
                "or pass --api-key on startup."
            )

        url = f"{PROSP_API_URL}{endpoint}"
        request_timeout = timeout or DEFAULT_TIMEOUT

        # Inject api_key into JSON body for POST requests
        if method.upper() == "POST":
            if json is None:
                json = {}
            json["api_key"] = use_api_key

        # For GET requests, add api_key as query param
        if method.upper() == "GET":
            if params is None:
                params = {}
            params["api_key"] = use_api_key

        async with httpx.AsyncClient(timeout=request_timeout) as http:
            try:
                response = await http.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json,
                )

                if response.status_code >= 400:
                    error_detail = self._parse_error(response)
                    raise httpx.HTTPStatusError(
                        message=error_detail,
                        request=response.request,
                        response=response,
                    )

                if response.status_code == 204:
                    return {"success": True}

                return response.json()

            except httpx.TimeoutException as e:
                raise TimeoutError(
                    f"Request to Prosp API timed out after {request_timeout}s."
                ) from e
            except httpx.RequestError as e:
                raise ConnectionError(
                    f"Failed to connect to Prosp API: {e}"
                ) from e

    def _parse_error(self, response: httpx.Response) -> str:
        """Parse error response and return descriptive message."""
        try:
            data = response.json()
            if isinstance(data, dict):
                if "error" in data:
                    error = data["error"]
                    if isinstance(error, dict):
                        return error.get("message", str(error))
                    return str(error)
                if "message" in data:
                    return data["message"]
                if "detail" in data:
                    return data["detail"]
            return f"HTTP {response.status_code}: {response.text[:200]}"
        except Exception:
            return f"HTTP {response.status_code}: {response.text[:200]}"

    async def post(self, endpoint: str, **kwargs: Any) -> Any:
        """POST request."""
        return await self.request("POST", endpoint, **kwargs)

    async def get(self, endpoint: str, **kwargs: Any) -> Any:
        """GET request."""
        return await self.request("GET", endpoint, **kwargs)


# Global client instance
client = ProspClient()


def get_client() -> ProspClient:
    """Get the global API client instance."""
    return client


def set_api_key(api_key: str) -> None:
    """Set the API key for the global client."""
    client.set_api_key(api_key)
