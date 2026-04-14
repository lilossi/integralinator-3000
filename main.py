from sympy import *
import asyncio
from sympy.abc import x
from evaluation.evaluation import get_solution_score, print_entire_evaluation
from llm_service.llm_service import llm_service
from test_suite.integral_data import create_integral_dataframe

async def main():
   ex = x * atan(x)
   print_entire_evaluation(ex)
   
   #ai = llm_service()
   #print(await ai.generate_expression(5))
   #print(create_integral_dataframe().head())
if __name__ == "__main__":
    asyncio.run(main())
