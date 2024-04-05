def addition_calculator(num1, num2):
    try:
        num1 = float(num1)
        num2 = float(num2)
        
        result = num1 + num2
        print("The sum is:", result)
    except ValueError:
        print("Please enter valid numbers.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python calc.py <num1> <num2>")
        sys.exit(1)
    num1 = sys.argv[1]
    num2 = sys.argv[2]
    addition_calculator(num1, num2)
