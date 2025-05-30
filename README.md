# MCP Agent  with Mem0 Integration

A Proof of Concept for an MCP Agent that integrates with a Model Context Protocol (MCP) server to provide AI agents with long-term memory capabilities using Mem0.

## Overview

This  demonstrates an MCP Agent that connects to a simulated MCP server to store, retrieve, and search memories. It uses LangChain for agent orchestration and Mem0 with Chroma for memory management, following best practices from Anthropic's MCP framework.

## Features

- **Save Memory**: Store information in long-term memory with semantic indexing.
- **Get All Memories**: Retrieve all stored memories for context.
- **Search Memories**: Find relevant memories using semantic search.
- **LangChain Agent**: Processes user queries and decides which MCP tool to call.

## Prerequisites

- Python 3.12+
- OpenAI API key (or other LLM provider like Ollama/OpenRouter)
