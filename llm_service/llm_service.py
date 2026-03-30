import langchain
import os
from sympy import Expr
import asyncio
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from llm_service.base_prompts import BASE_PROMPT_GENERATE
from llm_service.tools.evaluation_tool import get_entire_evaluation_tool

class llm_service:
    def __init__(self):
        self.model_name = "deepseek/deepseek-chat" # Standard deepseek model name on openrouter
        self.api_key = os.getenv("OPENROUTER_API_KEY_OSCAR")
        self.model = None
        self.agent = None
        if self.api_key:
            try:
                self.model = ChatOpenAI(
                    model_name=self.model_name,
                    api_key=self.api_key,
                    base_url="https://openrouter.ai/api/v1",
                )
                
                # Create tools for the agent
                tools = [
                    get_entire_evaluation_tool()
                ]
                
                self.agent = create_agent(
                    model=self.model,
                    tools=tools,
                    middleware=[AgentTools.handle_tool_errors],
                    system_prompt=BASE_PROMPT_GENERATE,
                )

            except Exception as e:
                print(f'Failed to initialize LLM: {e}')
                self.model = None
