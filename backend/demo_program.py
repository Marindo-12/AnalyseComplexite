
from program_analyzer import analyze_program


source = """
def example(n):
    numbers = list(range(n))

    for i in range(n):
        print(numbers[i])

    return numbers
"""

result = analyze_program(source)

for key, value in result.items():
    print(f"{key}: {value}")
