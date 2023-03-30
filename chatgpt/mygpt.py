import openai

openai.api_key = "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"

question = input("What is your question for ChatGPT? ")

response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=question,
    max_tokens=2000,
    n=1,
    stop=None,
    temperature=0.9
)
context = "Human: " + question + "AI: " + str(response)
print("AI: " + response["choices"][0]["text"])

while " ":

    human = input("Human: ")
    if human == "diagnostic":
        selection = input("what would you like to see?\ncontext\nquit\n")
        if selection == "context":
            print(context)
        if selection == "quit":
            quit

    context += human

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=context,
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=0.9
    )
    context += str(response)

    print("AI: ")

    print(response["choices"][0]["text"])
