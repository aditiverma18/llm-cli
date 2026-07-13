import ollama

def get_response(messages):
    response = ollama.chat(
      model="llama3.1:8b",
      messages=messages
)

    assistant_response = response['message']['content']
    return assistant_response

def main():
    messages = [
    {
        "role": "system",
        "content": "You are a helpful programming tutor. Explain concepts simply and use examples."
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

if __name__ =="__main__":
    main()