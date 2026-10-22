
from cost_model import add_costs, multiply_by_n
from complexity import analyze_cost


# Part 1: a linear sequence of operations.
part_one = {0: 3, 1: 2}  # 3 + 2n

# Part 2: a constant operation repeated n times.
part_two = multiply_by_n({0: 4})  # 4n

# Sequential parts: add their costs.
total_cost = add_costs(part_one, part_two)

# Analyze the result.
result = analyze_cost(total_cost)

print("Total cost:", result["expression"])
print("Complexity:", result["complexity"])
