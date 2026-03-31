"""Agent tools and middleware for LangChain agents."""

from collections.abc import Callable
from typing import Any

from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage


class AgentTools:
    """Utility class for agent tool handling."""

    @wrap_tool_call
    def handle_tool_errors(request: Any, handler: Callable[..., Any]) -> ToolMessage:
        """Handle tool execution errors with custom messages."""
        try:
            return handler(request)
        except Exception as e:
            return ToolMessage(
                content=f"Tool error: Please check your input and try again. ({e!s})",
                tool_call_id=request.tool_call["id"]
            )