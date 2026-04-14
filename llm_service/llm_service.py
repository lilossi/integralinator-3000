import os
import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from llm_service.base_prompts import BASE_PROMPT_GENERATE, USER_PROMPT_TEMPLATE
from llm_service.tools.evaluation_tool import get_entire_evaluation_tool
from llm_service.tools.middleware import AgentTools
from llm_service.tools.submit_tool import submit_generated_integrals, get_previously_submitted_integrals, submitted_integrals

class llm_service:
    def __init__(self):
        load_dotenv()
        self.model_name = "deepseek/deepseek-chat"
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

                tools = [
                    get_entire_evaluation_tool,
                    get_previously_submitted_integrals,
                    submit_generated_integrals
                ]
                
                self.agent = create_agent(
                    model=self.model,
                    tools=tools,
                    middleware=[AgentTools.handle_tool_errors],
                    system_prompt=BASE_PROMPT_GENERATE
                )

            except Exception as e:
                print(f'Failed to initialize LLM: {e}')
                self.model = None

    async def generate_expression(self, target_num: int) -> list[str]:
        if self.model is None or self.agent is None:
            return ['LLM not configured. Check the API key.']

        try:
            loop = asyncio.get_event_loop()
            prompt = USER_PROMPT_TEMPLATE
            
            while len(submitted_integrals) < target_num:
                print(f"Submissions so far: {len(submitted_integrals)}/{target_num}")
                agent_response = await loop.run_in_executor(
                    None,
                    lambda: self.agent.invoke(
                        {"input": prompt}
                    ),
                )
                print(agent_response.get("messages", []))

            return list(submitted_integrals)

        except Exception as e:
            return [f'Failed to process prompt with agent: {e}']
               
        