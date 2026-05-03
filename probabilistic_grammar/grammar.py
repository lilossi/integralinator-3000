from pcfg import PCFG
grammar = PCFG.fromstring("""
S -> Subject Action [1.0]
Subject -> "a cow" [0.7] | "some guy" [0.1] | "the woman" [0.2]
Action -> "eats lunch" [0.5] | "was here" [0.5]
""")

def main():
    for sentence in grammar.generate(100):
        print(sentence)

if __name__ == "__main__":
    main()