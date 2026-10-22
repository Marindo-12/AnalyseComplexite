
from source_analyzer import analyze_python_source

code = """
def example(n):
    total = 0
    for i in range(n):
        total += i
    return total
"""

result = analyze_python_source(code)

print("Expression estimée :", result["expression"])
print("Complexité estimée :", result["complexity"])
