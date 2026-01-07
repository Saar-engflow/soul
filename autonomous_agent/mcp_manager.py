import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPManager:
    def __init__(self):
        self.sessions = {} # {server_name: session}
        self.server_params = {
            # Example: "filesystem": StdioServerParameters(command="npx", args=["-y", "@modelcontextprotocol/server-filesystem", "c:/Users/sophi/OneDrive/Desktop/you/autonomous_agent"])
        }

    async def connect_to_server(self, server_name, command, args):
        """Connects to an MCP server using stdio transport."""
        params = StdioServerParameters(command=command, args=args)
        
        # We use a context manager for the client, so we need to manage the lifecycle carefully
        # For this autonomous agent, we'll keep sessions open as long as possible
        transport_ctx = stdio_client(params)
        read, write = await transport_ctx.__aenter__()
        session = ClientSession(read, write)
        await session.__aenter__()
        await session.initialize()
        
        self.sessions[server_name] = {
            "session": session,
            "context": transport_ctx
        }
        return session

    async def list_tools(self, server_name):
        if server_name in self.sessions:
            result = await self.sessions[server_name]["session"].list_tools()
            return result.tools
        return []

    async def call_tool(self, server_name, tool_name, arguments):
        if server_name in self.sessions:
            result = await self.sessions[server_name]["session"].call_tool(tool_name, arguments)
            return result.content
        return None

    async def shutdown(self):
        for server_name, session_data in self.sessions.items():
            await session_data["session"].__aexit__(None, None, None)
            await session_data["context"].__aexit__(None, None, None)
        self.sessions = {}
