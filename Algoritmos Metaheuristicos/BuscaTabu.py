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

def taboo_search(initial_solution, taboo_size, bt_max, knapsack):
    best_solution_value =  calculate_total_value(initial_solution)
    current_solution_value = calculate_total_value(initial_solution)
    current_solution = initial_solution
    best_solution_taboo = initial_solution
    minimal_solution_value = 1
    x = 0
    best_iteration = 0
    taboo_list = [-1]
    
    while current_solution_value > minimal_solution_value and x - best_iteration <= bt_max:
        x += 1
        current_neighbours = generate_neighbours(current_solution, knapsack)
        for neighbour in current_neighbours:
            neighbour_solution_value = calculate_total_value(neighbour)
            neighbour_solution_index = current_neighbours.index(neighbour)
            if neighbour_solution_value > current_solution_value and neighbour_solution_index != taboo_list[taboo_size-1] or neighbour_solution_value > best_solution_value:
                taboo_list.pop(0)
                taboo_list.append(neighbour_solution_index)
                
                current_solution_value = neighbour_solution_value
                current_solution = neighbour
        if current_solution_value > best_solution_value:
            best_solution_taboo = current_solution
            best_solution_value = current_solution_value
            best_iteration = x
    
    return best_solution_taboo

# Exemplo de uso
if __name__ == "__main__":
    items = [(2, 4), (2, 5), (3, 7), (4,9), (4,6), (10,4), (20,20), (4,1), (20,10),(10,7), (8,50), (9,20), (12,17)] # Exemplo de itens (valor, peso)
    capacity = 23  # Capacidade da mochila
    knapsack = KnapsackProblem(items, capacity) #cria o problema

    #constroi solucao inicial
    initial_solution = greedy_construct(knapsack, 0.2)
    print("Greedy:", initial_solution, calculate_total_value(initial_solution))


    # Taboo search
    best_solution = taboo_search(initial_solution,1,1,knapsack)
    print("Taboo search:", best_solution, calculate_total_value(best_solution))



