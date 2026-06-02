import os
import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from llm_service.base_prompts import BASE_PROMPT_GENERATE, build_user_prompt
from llm_service.tools.evaluation_tool import get_entire_evaluation_tool, pending_evaluations, reset_pending_evaluations
from llm_service.tools.middleware import handle_tool_errors
from llm_service.tools.submit_tool import submit_generated_integrals, submitted_integrals, reset_submitted_integrals

_SCORE_THRESHOLD = 0.8
_MAX_STALLED = 30


class LLMService:
    def __init__(self):
        load_dotenv()
        self.model_name = "deepseek/deepseek-v4-pro" #"deepseek/deepseek-v4-flash" #"openrouter/owl-alpha", "deepseek/deepseek-v4-pro"
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

        reset_submitted_integrals()

        try:
            loop = asyncio.get_running_loop()
            stalled = 0

            while len(submitted_integrals) < target_num:
                before = len(submitted_integrals)
                print(f"Submissions so far: {before}/{target_num}")

                reset_pending_evaluations()
                user_msg = build_user_prompt(list(submitted_integrals), target_num) 
                await loop.run_in_executor(
                    None,
                    lambda msg=user_msg: self.agent.invoke(
                        {"messages": [{"role": "user", "content": msg}]}
                    ),
                )

                # Fallback:
                if len(submitted_integrals) == before and pending_evaluations:
                    good = [
                        expr for expr, score in pending_evaluations.items()
                        if score >= _SCORE_THRESHOLD and expr not in submitted_integrals
                    ]
                    if good:
                        print(f"Fallback: submitting {len(good)} expression(s) the model evaluated but didn't submit.")
                        submitted_integrals.update(good)

                if len(submitted_integrals) == before:
                    stalled += 1
                    print(f"No new submissions this round ({stalled}/{_MAX_STALLED} stalled).")
                    if stalled >= _MAX_STALLED:
                        print("Stall limit reached. Returning collected integrals.")
                        break
                else:
                    stalled = 0

            return list(submitted_integrals)

        except Exception as e:
            return [f"Failed to generate: {e}"]
