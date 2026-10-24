# What this code is about
# This is the 'tool execution loop' - when LLM says 'use these tools', we must actually run them ourselves

# Line by line explanation

# 3. for tool in ai_message.tool_calls:
#    - ai_message.tool_calls contains list of tools LLM wants to call (e.g. get_conversion_factor, then convert)
#    - We loop through each one and run them one by one

for tool in ai_message.tool_calls:

# 4. if tool['name'] == 'get_conversion_factor':
#    - Check: Is this the first tool? We need exchange rate first before converting
    if tool['name'] == 'get_conversion_factor':

# 5. tool1_message = get_conversion_factor.invoke(tool)
#    - Actually call the function with args LLM decided (base_curr, target_curr)
#    - invoke() runs it for real and returns a ToolMessage object
        tool1_message = get_conversion_factor.invoke(tool)

# 6. print(tool1_message)
#    - Just to see what tool returned (debug)
        print(tool1_message)

# 7. messages.append(tool1_message)
#    - Add tool result to chat history. Without this, LLM won't know the tool ran
        messages.append(tool1_message)

# 8. conversion_factor = json.loads(tool1_message.content)['conversion_factor']
#    - tool1_message.content has JSON string. Parse it.
#    - Extract conversion_factor value (e.g. 83.5) and save in variable
#    - We need this value for the convert() tool next
        conversion_factor = json.loads(tool1_message.content)['conversion_factor']


# 10. if tool['name'] == 'convert':
#     - Now check if LLM also wants to convert
    if tool['name'] == 'convert':

# 11. tool['args']['conversion_rate'] = conversion_factor
#     - The convert() function needs conversion rate. 
#     - We manually put the rate we got from step 2 into the args
#     - This is called 'injecting' - we're feeding it ourselves instead of asking LLM
        tool['args']['conversion_rate'] = conversion_factor

# 12. tool2_message = convert.invoke(tool)
#     - Run convert() now with base value + conversion rate we injected
        tool2_message = convert.invoke(tool)

# 13. messages.append(tool2_message)
#     - Add convert result to chat history too
        messages.append(tool2_message)


# 15. final_result = llm_with_tools.invoke(messages).content
#     - Now send full history: original question + AI tool calls + tool1 result + tool2 result
#     - LLM looks at all of this and gives a proper answer like '10 USD = 835 INR'
        final_result = llm_with_tools.invoke(messages).content

# 16. print(final_result)
#     - Display the final answer to user
        print(final_result)
