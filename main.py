from sympy import exp, pprint, Expr
import asyncio
from sympy.abc import x
from evaluation.evaluation import get_solution_score, print_entire_evaluation
from llm_service.llm_service import llm_service

async def main():
   # ex = exp(-x**2)
   # ex = 1/(x**2 + 4)
   # ex = x**3 + 2*x**2 + x + 1
   #print(get_solution_score(ex))
   ai = llm_service()
   print(await ai.generate_expression())
if __name__ == "__main__":
    asyncio.run(main())
