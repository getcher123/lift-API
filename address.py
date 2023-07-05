import os
from dadata import Dadata

def check_address(text):
    dadata = Dadata(os.environ['TOKEN_ADR'], os.environ['SECRET_ADR'])
    return dadata.clean("address", text)

