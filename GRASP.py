import random
import copy
import math

# Definição do problema da mochila
class KnapsackProblem:
    def __init__(self, items, capacity):
        self.items = items  # Lista de itens, cada item é uma tupla (valor, peso)
        self.capacity = capacity  # Capacidade máxima da mochila

# Função para calcular o valor total de uma solução
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
    neighbours = generate_neighbours(solution,knapsack)
    for neighbour in neighbours:
        if calculate_total_value(neighbour) < calculate_total_value(solution):
            neighbours.remove(neighbour)
    return neighbours

#método construtivo guloso para criar uma solução inicial
def greedy_construct(knapsack, alpha):
    items = copy.deepcopy(knapsack.items)
    capacity = knapsack.capacity
    solution = []

    while capacity > 0 and items:
        sorted_items = sorted(items, key=lambda x: x[0] / x[1], reverse=True)
        num_candidates = int(len(sorted_items) * alpha)
        candidate_items = sorted_items[:num_candidates]

        # Verificar se ainda há itens candidatos
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
    
def GRASP(grasp_max,knapsack):
    best_solution_value = 0
    
    for x in range(grasp_max):
        solution = greedy_construct(knapsack,1)
        print("Greedy:", solution, calculate_total_value(solution), "Iter:", x)
        current_solution = local_search(solution,knapsack)
        current_solution_value = calculate_total_value(current_solution)
        
        if current_solution_value > best_solution_value:
            best_solution = current_solution
            best_solution_value = current_solution_value
        
    return best_solution

# Exemplo de uso
if __name__ == "__main__":
    items = [(2, 4), (2, 5), (3, 7), (4,9), (4,6)]  # Exemplo de itens (valor, peso)
    capacity = 23  # Capacidade da mochila
    knapsack = KnapsackProblem(items, capacity) #cria o problema

    # GRASP
    best_solution = GRASP(10,knapsack)
    print("GRASP:", best_solution, calculate_total_value(best_solution))



