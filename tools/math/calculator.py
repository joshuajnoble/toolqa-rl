'''
input: formula strings
output: the answer of the mathematical formula
'''
import os
import re
import requests
from operator import pow, truediv, mul, add, sub
#import wolframalpha
import json
from langchain_core.tools import tool

query = '1+2*3'

@tool
def calculator(query: str) -> float:
    """Evaluate a simple math expression and return the result."""
    operators = {
        '+': add,
        '-': sub,
        '*': mul,
        '/': truediv,
    }
    query = re.sub(r'\s+', '', query)
    if query.isdigit():
        return float(query)
    for c in operators.keys():
        left, operator, right = query.partition(c)
        if operator in operators:
            return round(operators[operator](calculator(left), calculator(right)),2)

@tool
def WolframAlphaCalculator(input_query: str) -> str:
    """Query WolframAlpha for a result string."""
    wolfram_alpha_appid = "2LWY52GTWU"

    url = "https://api.wolframalpha.com/v2/query"

    params = {
        "input": input_query,
        "appid": wolfram_alpha_appid,
        "format": "plaintext",
        "output": "json"
    }

    resp = requests.get(url, params=params)
    resp.raise_for_status()

    json_obj = json.loads(resp.text)

    for p in json_obj['queryresult']['pods']:
        if(p['title'] == "Result"):
            return(p['subpods'][0]['plaintext'])
    
    return ""

if __name__ == "__main__":
    query = 'mean(247.0, 253.0, 230.0, 264.0, 254.0, 275.0, 227.0, 258.0, 245.0, 253.0, 242.0, 229.0, 259.0, 253.0)'
    print(WolframAlphaCalculator(query))