

# Snowflake Architecture
<img width="1050" height="520" alt="image" src="https://github.com/user-attachments/assets/4fd16afb-fd83-4f29-9287-d72e9e09a929" />

## Tool execution:
### Cortex Analyst:
 Write and run SQL on your semantic views for structured data.
### Cortex Search:
Retrieve relevant document text for unstructured data.
### Code Execution:
Generate and run Python code in a sandboxed environment.
### Web Search: 
Query the web for real-time information.
### MCP Connectors:
Connect to external SaaS tools via the Model Context Protocol.
Custom Tools: Execute user-defined functions or stored procedures for actions.


# Snowflake Cortex AI

<img width="3608" height="1380" alt="image" src="https://github.com/user-attachments/assets/2ce4754c-ea86-4596-a4f8-d94b03c02a37" />

# Snowflake with MCP
<img width="3442" height="1928" alt="image" src="https://github.com/user-attachments/assets/1968dac4-b6ae-4f20-b5e3-8380443ffb3f" />

In Cursor, open or create mcp.json located at the root of your project and add the following. NOTE: Replace and with your values.
```
{
    "mcpServers": {
      "Snowflake MCP Server": {
        "url": "https://<YOUR-ORG-YOUR-ACCOUNT>.snowflakecomputing.com/api/v2/databases/dash_mcp_db/schemas/data/mcp-servers/dash_mcp_server",
            "headers": {
              "Authorization": "Bearer <YOUR-PAT-TOKEN>"
            }
      }
    }
}
```
Then, select **Cursor -> Settings -> Cursor Settings -> Tools & MCP** and you should see Snowflake MCP Server under Installed Servers.

# Best-practices-to-building-cortex-agents
https://www.snowflake.com/en/developers/guides/best-practices-to-building-cortex-agents/
