import ollama
from tools import add , multiply , get_current_time ,get_location,get_weather,get_weather_tool,get_all_memories,save_memory

tool_map={
    "add":add,
    "multiply":multiply,
    "get_current_time":get_current_time,
    "get_weather_tool": get_weather_tool,
    "save_memory":save_memory
}
tools=[
    {"type":"function",
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
} ,
{
    "type":"function",
    "function":{
        "name":"multiply",
        "description":"mutiply two numbers",
        "parameters":{
            "type":"object",
            "properties":{
                "a":{"type":"number",
                     "description":"The first number to multiply"},
                "b":{"type":"number",
                     "description":"The second number to mutiply"}
            },
            "required":["a","b"]
        } 
   
     } 
},
{
    "type":"function",
    "function":{
        "name":"get_current_time",
        "description":"gets the current local time"
     }
},
{    "type":"function",
    "function":{
        "name":"get_weather_tool",
        "description":"get weather details of city",
        "parameters":{
            "type":"object",
            "properties":{
                "city":{"type":"string",
                     "description":"name of city"}
            },
            "required":["city"]
        } 
   
     } 
    
},
{
    "type": "function",
    "function": {
        "name": "save_memory",
         "description":"Save long-term user memories such as stable preferences, long-term facts, and information that will likely be useful in future conversations. Do not use this tool for temporary events, daily activities, or trivial information.",
         "parameters":{
            "type":"object",
            "properties":{
                "memory":{"type":"string",
                     "description":"memory to save"}
            },
            "required":["memory"]
    
        }
    }    
}
]


def get_response(messages):
    response = ollama.chat(
      model="llama3.1:8b",
      messages=messages,
      tools=tools
)
   
    tool_calls=response["message"].get("tool_calls")
    if tool_calls:

        messages.append(response["message"])
        for tool_call in tool_calls:
           function_name=tool_call["function"]["name"]
           arguments=tool_call["function"]["arguments"]




           if function_name in tool_map:
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

def build_system_prompt():
    memories=get_all_memories()
    memory_text="Known memories:\n"

    if memories:
      for memory in memories:
        memory_text += f"- {memory}\n"
    else:
        memory_text += "None\n"
    return f"""
             You are a helpful programming tutor.

Explain concepts clearly and use examples.

Use only the provided tools when necessary.
Do not invent tools.

Known memories:
{memory_text}

Use these memories when answering.

Only save long-term information that will be useful in future conversations, such as stable preferences and long-term facts.

Do not save temporary events or daily activities.

    {memory_text}
    """

def main():
    messages = [
    {
        "role": "system",
        "content":build_system_prompt()
    }
]
    while True:
        user_input = input("Enter your question: ")
        if user_input.lower() == "exit":
            break

        messages.append({"role": "user", "content": user_input})      
        
        print(messages[0]["content"])
        try:
            assistant_response = get_response(messages)
        except Exception as e:
            messages.pop()
            print(f"An error occurred: {e}")
            continue

        messages.append({"role": "assistant", "content": assistant_response})

        print(f"Assistant: {assistant_response}")

if __name__ =="__main__":
    main()
