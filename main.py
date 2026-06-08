import pandas as pd
from test_suite.integral_data import create_integral_dataframe

if __name__ == "__main__":
    df = create_integral_dataframe()
    desirable = df[df["Desirable"] == 1]
    print(desirable)
