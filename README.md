# Prosp MCP Server

MCP server for [Prosp.ai](https://prosp.ai) LinkedIn outreach automation. Manage leads, campaigns, messaging, and analytics programmatically via the Model Context Protocol.

## Tools (17)

### Leads (8 tools)
| Tool | Description | Type |
|------|-------------|------|
| `add_lead` | Add a lead to a contact list and campaign | write |
| `add_lead_to_list` | Add a lead to a contact list only | write |
| `add_existing_lead_to_campaign` | Add an existing lead to a campaign | write |
| `remove_lead_from_campaign` | Remove a lead from a campaign | destructive |
| `delete_lead` | Permanently delete a lead from workspace | destructive |
| `get_leads_in_campaign` | Get all leads in a campaign | read-only |
| `get_lead_stage` | Get current stage of a lead in a campaign | read-only |
| `check_api_key` | Verify API key and connectivity | read-only |

### Campaigns (5 tools)
| Tool | Description | Type |
|------|-------------|------|
| `get_all_campaigns` | List all campaigns in workspace | read-only |
| `get_campaign_status` | Get status of a campaign | read-only |
| `start_campaign` | Start a campaign | write |
| `stop_campaign` | Stop a running campaign | destructive |
| `get_analytics` | Get analytics for campaign or workspace | read-only |

### Messaging (3 tools)
| Tool | Description | Type |
|------|-------------|------|
| `send_message` | Send a LinkedIn message to a profile | write |
| `send_voice_message` | Send a LinkedIn voice message | write |
| `get_conversation` | Get conversation history with a lead | read-only |

### System (1 tool)
| Tool | Description | Type |
|------|-------------|------|
| `get_server_info` | Server version, config, loaded tools | read-only |

## Setup

### Environment Variable

```bash
export PROSP_API_KEY="your-api-key-here"
```

Get your API key from [Prosp Settings](https://prosp.ai/settings).

### Claude Desktop / Claude Code

Add to your MCP config:

```json
{
  "mcpServers": {
    "prosp": {
      "command": "prosp-mcp",
      "env": {
        "PROSP_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Lazy Loading

Load only specific tool categories via `TOOL_CATEGORIES`:

```json
{
  "mcpServers": {
    "prosp": {
      "command": "prosp-mcp",
      "env": {
        "PROSP_API_KEY": "your-api-key-here",
        "TOOL_CATEGORIES": "leads,campaigns"
      }
    }
  }
}
```

Available categories: `leads`, `campaigns`, `messaging`

## Install

```bash
pip install prosp-mcp
```

Or from source:

```bash
git clone https://github.com/AvolveAi/prosp-mcp.git
cd prosp-mcp
pip install -e .
```

## Development

```bash
pip install -e ".[dev]"
pytest tests/
```

## API Coverage

Wraps the Prosp API v1 endpoints:

| Endpoint | Tool |
|----------|------|
| `POST /api/v1/leads` | `add_lead` |
| `POST /api/v1/leads/list` | `add_lead_to_list` |
| `POST /api/v1/leads/campaign` | `add_existing_lead_to_campaign` |
| `POST /api/v1/leads/campaign/remove` | `remove_lead_from_campaign` |
| `POST /api/v1/leads/delete` | `delete_lead` |
| `POST /api/v1/leads/campaign/list` | `get_leads_in_campaign` |
| `POST /api/v1/leads/stage` | `get_lead_stage` |
| `POST /api/v1/campaigns` | `get_all_campaigns` |
| `POST /api/v1/campaigns/status` | `get_campaign_status` |
| `POST /api/v1/campaigns/start` | `start_campaign` |
| `POST /api/v1/campaigns/stop` | `stop_campaign` |
| `POST /api/v1/analytics` | `get_analytics` |
| `POST /api/v1/messages/send` | `send_message` |
| `POST /api/v1/messages/voice` | `send_voice_message` |
| `POST /api/v1/conversations` | `get_conversation` |

> **Note:** Endpoint paths are inferred from Prosp's API documentation and Zapier/Make.com integration. Some paths may need adjustment once the full OpenAPI spec is available.

## License

MIT
