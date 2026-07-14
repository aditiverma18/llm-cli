import ollama
from tools import add
tool_map={
    "add":add
}
tools=[{
    "type":"function",
    "function":{
        "name":"add",
        "description":"Add two numbers",
        "parameters":{
            "type":"object",
            "properties":{
                "a":{"type":"number",
                     "description":"The first number to add"},
                "b":{"type":"number",
                     "description":"The second number to add"}
            },
            "required":["a","b"]
        }
    }
}]
def get_response(messages):
    response = ollama.chat(
      model="llama3.1:8b",
      messages=messages,
      tools=tools
)
   
    tool_calls=response["message"].get("tool_calls")
    if tool_calls:

        messages.append(response["message"])
        print(tool_calls)
        tool_call=tool_calls[0]
        function_name=tool_call["function"]["name"]
        arguments=tool_call["function"]["arguments"]
        print(function_name)
        print(arguments)

        if(function_name in tool_map):
            tool_function=tool_map[function_name]
            tool_result=tool_function(**arguments)
        else:
            tool_result=f"Error: Unknown tool'{function_name}'"
        messages.append({
                "role":"tool",
                "content":str(tool_result),
                "tool_name":function_name})
        final_response=ollama.chat(
                model="llama3.1:8b",
                messages=messages,
                tools=tools
            )
        assistant_response=final_response["message"]["content"]
        return assistant_response

    assistant_response=response["message"]["content"]
    return assistant_response


def main():
    messages = [
    {
        "role": "system",
        "content":(
            "You are a helpful programming tutor. "
            "Explain concepts simply and use examples. "
            "Use tools only when they are necessary. "
            "You only have access to the tools explicitly provided to you. "
            "Never invent or mention nonexistent tools. "
            "For normal programming questions, answer directly in natural language."
        )
    }
]
    while True:
        user_input = input("Enter your question: ")
        if user_input.lower() == "exit":
            break

        messages.append({"role": "user", "content": user_input}
)
        try:
            assistant_response = get_response(messages)
        except Exception as e:
            messages.pop()
            print(f"An error occurred: {e}")
            continue

        messages.append({"role": "assistant", "content": assistant_response})

        print(f"Assistant: {assistant_response}")
    #print(add(10,20))

if __name__ =="__main__":
    main()