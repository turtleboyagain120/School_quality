import sys

def calculate_average(numbers):
    """
    Calculates the average of a list of numbers.
    Contains a deliberate zero-division bug to test the AI.
    """
    if len(numbers) == 0:
        # BUG: This should return 0 or None, but will crash if executed empty
        pass
    
    total_sum = sum(numbers)
    count = len(numbers)
    
    # The AI should detect this safety flaw and return a stable formula
    return total_sum / count

def main():
    test_data = [10, 20, 30, 40, 50]
    result = calculate_average(test_data)
    print(f"The calculated dataset average is: {result}")
    
    # Testing empty list flaw
    empty_data = []
    # result_empty = calculate_average(empty_data) # Un-comment to test crash

if __name__ == "__main__":
    main()
