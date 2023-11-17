import random
import copy

class KnapsackProblem:
    def __init__(self, items, capacity):
        self.items = items
        self.capacity = capacity

def calculate_total_value(solution):
    total_value = sum(item[0] for item in solution)
    total_weight = sum(item[1] for item in solution)
    total_value = total_value - 15 * max(0, total_weight - 23)
    return total_value

def generate_neighbours(current_solution, knapsack):
    default_items = knapsack.items
    neighbour_solutions = []
    
    for i, item in enumerate(default_items):
        neighbour_solution = copy.deepcopy(current_solution)
        if item in neighbour_solution:
            neighbour_solution.remove(item)
            neighbour_solutions.append(neighbour_solution)
        else:
            neighbour_solution.append(item)
            neighbour_solutions.append(neighbour_solution)
            
    return neighbour_solutions

def generate_better_neighbours(solution, knapsack):
    neighbours = generate_neighbours(solution, knapsack)
    for neighbour in neighbours:
        if calculate_total_value(neighbour) < calculate_total_value(solution):
            neighbours.remove(neighbour)
    return neighbours

def greedy_construct(knapsack, alpha):
    items = copy.deepcopy(knapsack.items)
    capacity = knapsack.capacity
    solution = []

    while capacity > 0 and items:
        sorted_items = sorted(items, key=lambda x: x[0] / x[1], reverse=True)
        num_candidates = int(len(sorted_items) * alpha)
        candidate_items = sorted_items[:num_candidates]

        if not candidate_items:
            break

        item = random.choice(candidate_items)
        if item[1] <= capacity:
            solution.append(item)
            capacity -= item[1]
        else:
            break

        items.remove(item)

    return solution

def local_search(initial_solution, knapsack):
    current_solution = initial_solution
    better_solution_found = True 

    while better_solution_found:
        better_solution_found = False

        neighbours = generate_better_neighbours(current_solution, knapsack)

        for neighbour in neighbours:
            if calculate_total_value(neighbour) > calculate_total_value(current_solution):
                current_solution = neighbour
                better_solution_found = True

    return current_solution
    
def perturbation(solution, knapsack):
    items = knapsack.items
    sorted_items = sorted(items, key=lambda x: x[0] / x[1], reverse=True)
    sorted_solution = sorted(solution, key=lambda x: x[0] / x[1], reverse=True)
    
    for item in sorted_items:
        if item not in sorted_solution:
            sorted_solution.pop(0)
            sorted_solution.append(item)
            break
        
    return sorted_solution

def acceptance_criterion(current_solution, perturbed_solution):
    if calculate_total_value(perturbed_solution) > calculate_total_value(current_solution):
        return perturbed_solution
    else:
        return current_solution
    

def ils(knapsack, max_iterations):
    current_solution = greedy_construct(knapsack, 1)
    current_solution = local_search(current_solution, knapsack)

    iteration = 0
    while iteration < max_iterations:
        perturbed_solution = perturbation(current_solution, knapsack)
        perturbed_solution = local_search(perturbed_solution, knapsack)

        current_solution = acceptance_criterion(current_solution, perturbed_solution)

        iteration += 1

    return current_solution

if __name__ == "__main__":
    items = [(2, 4), (2, 5), (3, 7), (4, 9), (4, 6)]
    capacity = 23
    knapsack = KnapsackProblem(items, capacity)

    best_solution = ils(knapsack, 10)
    print("ILS:", best_solution, calculate_total_value(best_solution))
