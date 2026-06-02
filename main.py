from sympy import *
import asyncio
from sympy.abc import x
from evaluation.evaluation import get_entire_evaluation

async def main():
   #ex = x * atan(x)
   #ex = x/(1 + x**2)
   #ex = exp(x) * sin(x) * cos(x)


   # backward
   #ex = -3*sinh(3)*sinh(x)*cosh(x)**2/8
   #ex = -exp(x)*log(27)*cos(exp(x))/27**sin(exp(x))
   # forward
   #ex = x + atan(cosh(sinh(cos(x)) - 2))
   #ex =  2**(2*x)/1024 + x - 15/(4*x)

   #ex = -exp(x)*log(27)*cos(exp(x))/27**sin(exp(x))
   #ex = x**2+2*x+1
   #ex = 4*(x*sinh(x) + cosh(x))*sin(sinh(x*cosh(x)) + 1)*cosh(x*cosh(x))
   ex: Expr = x**2 * exp(x) + sin(x/3)
   print(ex)
   for node in preorder_traversal(ex):
      print(node)
      print(type(node))
      print(node.args)
   print(get_entire_evaluation(ex))
   
   #ai = llm_service()
   #print(await ai.generate_expression(5))
   #print(create_integral_dataframe().head())
if __name__ == "__main__":
    asyncio.run(main())
