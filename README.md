# Prosp MCP Server

MCP server for [Prosp.ai](https://prosp.ai) LinkedIn outreach automation. Add leads to campaigns, verify API connectivity, and manage LinkedIn outreach programmatically.

## Tools

| Tool | Description | Annotations |
|------|-------------|-------------|
| `add_lead` | Add a lead to a Prosp list and campaign | write |
| `check_api_key` | Verify API key is valid and Prosp is reachable | read-only |
| `get_server_info` | Get server version, config status, and loaded tools | read-only |

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

Currently wraps the confirmed Prosp API endpoints:

- `POST /api/v1/leads` — Add lead to list/campaign

Additional endpoints (send message, send voice, remove lead) are referenced in Prosp's Zapier integration and will be added as documentation becomes available.

## License

MIT
