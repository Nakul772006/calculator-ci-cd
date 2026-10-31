"""A simple menu-driven command-line calculator."""


def add(first: float, second: float) -> float:
    """Return the sum of two numbers."""
    return first + second


def subtract(first: float, second: float) -> float:
    """Return the difference between two numbers."""
    return first - second


def multiply(first: float, second: float) -> float:
    """Return the product of two numbers."""
    return first * second


def divide(first: float, second: float) -> float:
    """Return the quotient, or raise an error if the divisor is zero."""
    if second == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return first / second


def read_number(prompt: str) -> float:
    """Read a number from the user, repeating until the input is valid."""
    while True:
        try:
            # float() accepts both integer strings (such as "4") and decimals.
            return float(input(prompt))
        except ValueError:
            print("Invalid number. Please enter an integer or decimal value.")


def main() -> None:
    """Display the calculator menu and handle user selections."""
    operations = {
        "1": ("Addition", add),
        "2": ("Subtraction", subtract),
        "3": ("Multiplication", multiply),
        "4": ("Division", divide),
    }

    while True:
        print("\nCalculator")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Exit")

        choice = input("Choose an option (1-5): ").strip()
        if choice == "5":
            print("Goodbye!")
            break
        if choice not in operations:
            print("Invalid choice. Please select an option from 1 to 5.")
            continue

        first = read_number("Enter the first number: ")
        second = read_number("Enter the second number: ")
        operation_name, operation = operations[choice]

        try:
            result = operation(first, second)
        except ZeroDivisionError as error:
            print(error)
        else:
            print(f"{operation_name} result: {result}")


if __name__ == "__main__":
    main()
