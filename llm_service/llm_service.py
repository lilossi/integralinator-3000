import os
from dotenv import load_dotenv
from langchain.messages import HumanMessage, SystemMessage
from sympy import Expr
import asyncio
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from llm_service.base_prompts import BASE_PROMPT_GENERATE
from llm_service.tools.evaluation_tool import get_entire_evaluation_tool
from llm_service.tools.middleware import AgentTools

class llm_service:
    def __init__(self):
        load_dotenv()
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
                    get_entire_evaluation_tool
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

    async def generate_expression(self) -> str:
        if self.model is None or self.agent is None:
            return 'LLM not configured. Check the API key.'

        try:
            loop = asyncio.get_event_loop()
            agent_response = await loop.run_in_executor(
                None,
                lambda: self.agent.invoke(
                    {"input": "Generate a mathematical expression."}
                ),
            )

            #return agent_response.get("output", str(agent_response))

            messages = agent_response.get("messages", [])
            ai_replies = [msg.content for msg in messages if msg.type == "ai" and msg.content.strip()]
            
            if not ai_replies:
                return agent_response.get("output", str(agent_response))
            
            return "\n\n".join(ai_replies)

        except Exception as e:
            return f'Failed to process prompt with agent: {e}'
               
        