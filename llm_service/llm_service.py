import os
import re
import json
from dotenv import load_dotenv
from langchain.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
from sympy import Expr
import asyncio
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from llm_service.base_prompts import BASE_PROMPT_GENERATE, USER_PROMPT_TEMPLATE
from llm_service.tools.evaluation_tool import get_entire_evaluation_tool
from llm_service.tools.middleware import AgentTools

class IntegralList(BaseModel):
    expressions: list[str] = Field(description="A list of mathematical expressions for the integrals.")

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

    async def generate_expression(self, num_expressions: int) -> list[str]:
        if self.model is None or self.agent is None:
            return ['LLM not configured. Check the API key.']

        try:
            loop = asyncio.get_event_loop()
            parser = PydanticOutputParser(pydantic_object=IntegralList)
            prompt = USER_PROMPT_TEMPLATE.format(
                num_expressions=num_expressions,
                format_instructions=parser.get_format_instructions()
            )
            agent_response = await loop.run_in_executor(
                None,
                lambda: self.agent.invoke(
                    {"input": prompt}
                ),
            )

            # Look for JSON output directly in the final output
            final_output = agent_response.get("output", "")
            
            if not final_output.strip():
                # If output is empty, try to get it from the last AI message
                messages = agent_response.get("messages", [])
                ai_replies = [msg.content for msg in messages if msg.type == "ai" and msg.content.strip()]
                if ai_replies:
                    final_output = ai_replies[-1]

            print(f"Raw agent output:\n{final_output}\n")  # Debugging line to see the raw output
            
            # Parse the JSON
            try:
                parsed_result = parser.parse(final_output)
                expressions = parsed_result.expressions
            except OutputParserException as e:
                # Find a JSON object if wrapped in markdown or extraneous text
                import json
                expressions = None
                
                # First try looking for the dict with "expressions"
                dict_match = re.search(r'\{[\s\S]*"expressions"[\s\S]*\}', final_output)
                if dict_match:
                    try:
                        parsed_json = json.loads(dict_match.group(0))
                        if "expressions" in parsed_json and isinstance(parsed_json["expressions"], list):
                            expressions = parsed_json["expressions"]
                    except Exception:
                        pass
                
                # Then try looking for a plain array if first failed
                if expressions is None:
                    array_match = re.search(r'\[\s*(?:"[^"]*"(?:\s*,\s*"[^"]*")*\s*)?\]', final_output)
                    if array_match:
                        try:
                            parsed_array = json.loads(array_match.group(0))
                            if isinstance(parsed_array, list) and all(isinstance(i, str) for i in parsed_array):
                                expressions = parsed_array
                        except Exception:
                            pass

                if expressions is None:
                    return [f"Failed to extract JSON from response.\nParser Exception: {e}"]

            # Strictly enforce the number of expressions requested
            if len(expressions) > num_expressions:
                print(f"Warning: Model generated {len(expressions)} expressions but {num_expressions} were requested. Truncating.")
                expressions = expressions[:num_expressions]
            elif len(expressions) < num_expressions:
                print(f"Warning: Model generated only {len(expressions)} expressions but {num_expressions} were requested.")
                
            return expressions

        except Exception as e:
            return [f'Failed to process prompt with agent: {e}']
               
        