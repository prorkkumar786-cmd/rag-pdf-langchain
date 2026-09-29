def calculator(expression: str):

    try:
        # input(f'------------------------{expression}')
        result = eval(expression)

        return str(result)

    except Exception as e:

        return f"Calculator error: {e}"


print(calculator('10 *20'))