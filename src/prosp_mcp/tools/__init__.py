"""
Prosp MCP Server — Tool Implementations

Tool implementations organized by category.
Supports lazy loading via TOOL_CATEGORIES environment variable.
"""

from __future__ import annotations

import os
from typing import Callable


def get_available_categories() -> list[str]:
    """Get list of available tool categories."""
    return ["leads"]


def is_lazy_loading_enabled() -> bool:
    """Check if lazy loading is active."""
    return bool(os.environ.get("TOOL_CATEGORIES"))


def get_requested_categories() -> list[str]:
    """Get list of categories requested via TOOL_CATEGORIES env var."""
    categories_env = os.environ.get("TOOL_CATEGORIES", "")
    if not categories_env:
        return get_available_categories()

    requested = [c.strip().lower() for c in categories_env.split(",") if c.strip()]
    valid = [c for c in requested if c in get_available_categories()]

    if not valid:
        return get_available_categories()

    return valid


def load_tools_for_category(category: str) -> list[Callable]:
    """Load tools for a specific category."""
    if category == "leads":
        from .leads import LEAD_TOOLS
        return LEAD_TOOLS
    return []


def get_all_tools() -> list[Callable]:
    """Get all tools based on TOOL_CATEGORIES configuration."""
    categories = get_requested_categories()
    tools: list[Callable] = []

    for category in categories:
        tools.extend(load_tools_for_category(category))

    return tools


__all__ = [
    "get_available_categories",
    "is_lazy_loading_enabled",
    "get_requested_categories",
    "get_all_tools",
]
