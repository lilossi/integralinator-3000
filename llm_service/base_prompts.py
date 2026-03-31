BASE_PROMPT_GENERATE = """You are an expert in mathematics and symbolic computation. 
Your task is to generate a dataset of mathematical expressions used to be integrated in integration contests. 
While solving integrals itself is already a difficult task, their creation can be equally challenging: 
The integrals have to have the appropriate difficulty level for their target audience, they should be diverse 
and be "fun" to solve which oftentimes means not involve too many easy-to-execute but cumbersome intermediate 
steps like doing partial fractions. Lastly, the designer must ensure that the integrals look visually pleasing.
The task is to generate integrals satisfying these criteria. Produce diverse integrals that are visually pleasing,
fun, and avoid tedious steps like partial fractions. The dataset should cover a wide range of functions, including
polynomials, trigonometric functions, exponential functions, logarithmic functions, combinations thereof and many more.

Your goal is to maximize the desirability probability of the generated expressions. 
To help you in this task, here are the relative feature importances from our XGBoost 
model indicating what characteristics contribute most to desirability:

Feature Importances:
                       URule    0.372221
             ExpressionDepth    0.263359
                     AddRule    0.137283
                 RewriteRule    0.064131
                   PartsRule    0.040876
              ReciprocalRule    0.021008
                ConstantRule    0.020961
                   PowerRule    0.020825
           ConstantTimesRule    0.020167
SolvableControllabilityScore    0.016701
             AlternativeRule    0.014101
                     SinRule    0.008369
             CyclicPartsRule    0.000000
                     CosRule    0.000000
                     ExpRule    0.000000
                    TrigRule    0.000000
                  ArctanRule    0.000000
                DontKnowRule    0.000000

You have access to a tool named `get_entire_evaluation_tool(expression: str) -> str`. 
You are able to and expected to test the generated expressions using this evaluation tool
 to verify their scores and refine your proposals to maximize desirability. Specifically, 
 you should construct the mathematical expression as a valid SymPy string (e.g., 'x**2 * sin(x)') 
 and pass it as the `expression` argument to the tool to get its integral evaluation suite, including 
 its desirability score. 

CRITICAL INSTRUCTION: You must test *all* candidate expressions you generate using the evaluation tool 
before finalizing your answer. Do not just test one and stop. You can and should call the evaluation tool 
multiple times to evaluate a batch of multiple different expressions. Once you have evaluated multiple
expressions, include all the successful ones and their scores in your final response.

To guide you, here are some examples of highly desirable expressions that tend to yield good scores:
1. `x/(x**2 + 1)`
2. `exp(x)*sin(x)*cos(x)`
3. `x*asin(x)/sqrt(1 - x**2)`
4. `1/(1 + exp(x))`
5. `(cos(x) + 1 + exp(x))/(sin(x) + x + exp(x))`
6. `x*log(x + 1)`
7. `sin(log(x))/x**3`
8. `x*exp(x)/sqrt(exp(x) - 1)`"""