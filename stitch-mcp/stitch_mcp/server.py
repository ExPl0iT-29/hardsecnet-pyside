import os
import sys
import asyncio
import httpx
from typing import Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Initialize the MCP server
app = Server("stitch-mcp")

# Default endpoint - to be overridden by the user if needed
STITCH_API_ENDPOINT = os.environ.get("STITCH_API_ENDPOINT", "https://stitch.withgoogle.com/api/v1/generate")

async def generate_stitch_code(prompt: str, context: Optional[str] = None) -> str:
    """
    Calls the Google Stitch API to generate UI code based on the prompt.
    """
    api_key = os.environ.get("STITCH_API_KEY")
    if not api_key:
        return "Error: STITCH_API_KEY environment variable is not set. Please set it to use this tool."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    # Construct the payload
    # Note: This is a placeholder payload structure. 
    # The exact payload depends on Google Stitch's actual API documentation.
    payload = {
        "prompt": prompt,
    }
    if context:
        payload["context"] = context

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                STITCH_API_ENDPOINT,
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            
            data = response.json()
            # Extract the code from the response. 
            # Again, this path ('code') is a placeholder and should be updated 
            # once the exact API response structure is known.
            if "code" in data:
                return f"Successfully generated code:\n\n{data['code']}"
            else:
                return f"Received successful response but could not parse the code block. Raw response: {data}"
                
    except httpx.HTTPStatusError as e:
        return f"HTTP error occurred while calling Stitch API: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="generate_stitch_ui",
            description="Generate a UI component (HTML/CSS/React) using Google Stitch AI by providing a natural language prompt.",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The description of the UI you want to build (e.g. 'A modern login form with a dark theme')."
                    },
                    "context": {
                        "type": "string",
                        "description": "Optional additional context or design constraints."
                    }
                },
                "required": ["prompt"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    if name == "generate_stitch_ui":
        prompt = arguments.get("prompt")
        context = arguments.get("context")
        
        if not prompt:
            raise ValueError("The 'prompt' argument is required.")
            
        result = await generate_stitch_code(prompt, context)
        return [TextContent(type="text", text=result)]
    
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
