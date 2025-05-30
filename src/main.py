import os
import asyncio
import json
from typing import Dict, Any
from contextlib import asynccontextmanager
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from utils import get_mem0_client

class SimulatedMCPClient:
    def __init__(self):
        self.mem0_client = get_mem0_client()

    async def list_tools(self):
        return [
            {"name": "save_memory", "description": "Save a memory to the vector store"},
            {"name": "search_memories", "description": "Search for memories in the vector store"},
            {"name": "get_all_memories", "description": "Retrieve all stored memories"}
        ]

    async def call_tool(self, tool_name: str, parameters: Dict[str, Any]):
        if tool_name == "save_memory":
            memory_content = parameters.get("content")
            self.mem0_client.add([{"role": "user", "content": memory_content}], user_id="user")
            return f"Successfully saved memory: {memory_content}"
        elif tool_name == "search_memories":
            query = parameters.get("query")
            results = self.mem0_client.search(query, user_id="user")
            return [result["content"] for result in results]
        elif tool_name == "get_all_memories":
            results = self.mem0_client.get_all(user_id="user")
            return [result["content"] for result in results]
        else:
            return f"Unknown tool: {tool_name}"

class MCPAgent:
    def __init__(self, llm):
        self.llm = llm
        self.mcp_client = None
        self.tools = []
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an AI assistant with access to a memory store via MCP tools. Use the tools to manage and retrieve memories based on user queries. If a query involves saving, searching, or retrieving memories, call the appropriate tool. For other queries, respond directly. Always respond clearly."),
            ("human", "{input}")
        ])

    @asynccontextmanager
    async def initialize(self):
        # self.mcp_client = SimulatedMCPClient()
        # self.tools = await self.mcp_client.list_tools()
        # yield
        pass # Temporarily disable mcp_client initialization
        yield # Still need to yield for asynccontextmanager

    async def run(self, query: str):
        try:
            async with self.initialize():
                if any(keyword in query.lower() for keyword in ["save memory", "search memories", "retrieve memories"]):
                    tool_name = None
                    parameters = {}
                    if "save memory" in query.lower():
                        tool_name = "save_memory"
                        parameters = {"content": query.replace("Save a memory:", "").strip()}
                    elif "search memories" in query.lower():
                        tool_name = "search_memories"
                        parameters = {"query": query.replace("Search for memories about", "").strip()}
                    elif "retrieve memories" in query.lower():
                        tool_name = "get_all_memories"
                        parameters = {}

                    if tool_name:
                        result = await self.mcp_client.call_tool(tool_name, parameters)
                        return json.dumps(result) if isinstance(result, list) else result
                else:
                    chain = self.prompt | self.llm
                    response = await chain.ainvoke({"input": query})
                    return response.content
        except Exception as e:
            return f"Error processing query: {str(e)}"

async def main():
    # Initialize LLM
    # llm = ChatOllama(model="llama3", base_url="http://localhost:11434") # Hardcoded for testing
    llm = ChatOllama(model=os.getenv("LLM_CHOICE", "llama3")) # base_url removed, relying on default

    # Create and initialize agent
    agent = MCPAgent(llm)

    # Example queries
    queries = [
        "Hello", # Query that should go to the LLM directly
        "Save a memory: I attended a Python conference on May 30, 2025.",
        "Search for memories about Python conferences.",
        "Retrieve all my stored memories."
    ]

    for query in queries:
        print(f"\nQuery: {query}")
        result = await agent.run(query)
        print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())