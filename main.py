from sympy import *
import asyncio
from sympy.abc import x
from evaluation.evaluation import get_solution_score, print_entire_evaluation
from llm_service.llm_service import llm_service
from test_suite.integral_data import create_integral_dataframe

async def main():
   #ex = exp(-x**2)
   # ex = 1/ln(x)
   # ex = 1/(x**2 + 4)
   #ex = exp(x)*sin(x)
   #ex = x**3 + 2*x**2 + x + 1
   #ex = log(x + sqrt(1 + x**2)) #(Score: 0.9839)
   #ex = (1 + log(x))/x
   #ex = x**4 + 3*x**2 + 17*x + 5 + exp(x)
   ex = x * atan(x)
   #print(get_solution_score(ex))
   print_entire_evaluation(ex)
   
   #ai = llm_service()
   #print(await ai.generate_expression(5))
   #print(create_integral_dataframe().head())
if __name__ == "__main__":
    asyncio.run(main())
