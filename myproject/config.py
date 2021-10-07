import os

class Config:
    # move to the env var in the future
    SECRET_KEY = "asdasd46a5sd6a4fa4d6f4fas64fas6fsa"
    # move to the env var in the future
    DATABASE = os.path.join(os.path.dirname(__file__), "deso.sqlite")
