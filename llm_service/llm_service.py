import os
import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from llm_service.base_prompts import BASE_PROMPT_GENERATE, build_user_prompt
from llm_service.tools.evaluation_tool import get_entire_evaluation_tool
from llm_service.tools.middleware import handle_tool_errors
from llm_service.tools.submit_tool import submit_generated_integrals, submitted_integrals


class LLMService:
    def __init__(self):
        load_dotenv()
        self.model_name = "deepseek/deepseek-v4-flash" #"deepseek/deepseek-v4-flash" #"openrouter/owl-alpha", "deepseek/deepseek-v4-pro"
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.agent = None

        if self.api_key:
            try:
                model = ChatOpenAI(
                    model_name=self.model_name,
                    api_key=self.api_key,
                    base_url="https://openrouter.ai/api/v1",
                    #reasoning={"effort": "xhigh", "summary": "auto"},
                )

                self.agent = create_agent(
                    model=model,
                    tools=[get_entire_evaluation_tool, submit_generated_integrals],
                    middleware=[handle_tool_errors],
                    system_prompt=BASE_PROMPT_GENERATE,
                )

            except Exception as e:
                print(f"Failed to initialize LLM: {e}")

    async def generate_expression(self, target_num: int) -> list[str]:
        if self.agent is None:
            return ["LLM not configured. Check the API key."]

        try:
            loop = asyncio.get_running_loop()
            history = []

            while len(submitted_integrals) < target_num:
                print(f"Submissions so far: {len(submitted_integrals)}/{target_num}")
                user_msg = build_user_prompt(list(submitted_integrals), target_num)
                result = await loop.run_in_executor(
                    None,
                    lambda: self.agent.invoke(
                        {"messages": history + [{"role": "user", "content": user_msg}]}
                    ),
                )
                history = result["messages"]

            return list(submitted_integrals)

        except Exception as e:
            return [f"Failed to process prompt with agent: {e}"]
