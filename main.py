from agent import app


while True:

    question = input("\nAsk your question: ")

    if question.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    try:

        result = app.invoke({

            "question": question,

            "answer": "",

            "tool": "",

            "tool_input": "",

            "tool_result": ""
        })

        print("\nFinal Answer:")
        print(result["answer"])

    except Exception as e:

        print("\nERROR:")
        print(type(e).__name__)
        print(e)

        import traceback
        traceback.print_exc()