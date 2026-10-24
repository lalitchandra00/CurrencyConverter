from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
import requests 
from dotenv import load_dotenv
import os


load_dotenv()

# Create the Gemini chat model.
llm = ChatGoogleGenerativeAI(
	model="gemini-3.8-flash",
	google_api_key=os.getenv("GOOGLE_API_KEY"),
	temperature=0.8
    # max_tokens=20,
)


# Tool Creation
@tool
def get_conversion_factor(base_curr: str,   target_curr : str) -> float:
    """This function fetches the currency conversion factor between a base currency and target currency"""
    url = f"https://v6.exchangerate-api.com/v6/589f28bd305564c28b3807d6/pair/{base_curr}/{target_curr}"
    response = requests.get(url)

    return response.json()


# result_get_conversion_factor = get_conversion_factor.invoke({'base_curr' : 'USD', 'target_curr' : 'INR'})
# # Result contains dictionaries
# print(result_get_conversion_factor['conversion_rate'])


@tool
def convert(base_curr_value:float, conversion_factor:float )-> float:
    """given a currency conversion rate this function calculates the target currency value from a given base currency value"""

    return (base_curr_value * conversion_factor)

# result_convert = convert.invoke({'base_curr_value': 10, 'conversion_factor' : 95.0365})
# print("\n", result_convert)


# Tool Binding
llm_with_tools = llm.bind_tools([get_conversion_factor, convert])

# Making message and sendinf=g it to the llm.
human_message = input("Enter query : ")
message = HumanMessage(human_message)

ai_message = llm_with_tools.invoke(message)
message.append(ai_message)