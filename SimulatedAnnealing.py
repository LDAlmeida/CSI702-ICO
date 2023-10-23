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
    return total_value

def generate_neighbour(current_solution, knapsack):
    neighbour_solution = copy.deepcopy(current_solution)

    # Escolher aleatoriamente um item para remover, se houver algum item
    if neighbour_solution:
        item_to_remove = random.choice(neighbour_solution)
        neighbour_solution.remove(item_to_remove)

    # Escolher aleatoriamente um item para adicionar, garantindo a viabilidade
    remaining_items = [item for item in knapsack.items if item not in neighbour_solution]
    valid_items = [item for item in remaining_items if sum(item[1] for item in neighbour_solution) + item[1] <= knapsack.capacity]

    if valid_items:
        item_to_add = random.choice(valid_items)
        neighbour_solution.append(item_to_add)

    return neighbour_solution

#método construtivo guloso para criar uma solução inicial
def greedy_construct(knapsack, alpha):
    items = knapsack.items
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
    
    
def simulated_annealing(knapsack, initial_solution, initial_temperature, cooling_rate, num_iterations):
    best_solution = initial_solution
    current_solution = initial_solution
    current_temperature = initial_temperature
    iterT = 0
    
    while(current_temperature > 1
          ):
        while(iterT < num_iterations):
            #print(current_temperature)
            iterT+= 1
            neighbour_solution = generate_neighbour(current_solution, knapsack)
            neighbour_value = calculate_total_value(neighbour_solution)
            current_value = calculate_total_value(current_solution)
            best_value = calculate_total_value(best_solution)
            delta = neighbour_value - current_value
            
            if delta > 0:
                if neighbour_value > current_value:
                    best_solution = neighbour_solution
                    current_solution = neighbour_solution
                else:
                    x = random.random()
                    if(x > math.exp(delta/current_temperature)):
                        current_solution = neighbour_solution
                        
        current_temperature*= cooling_rate
        iterT = 0
    return best_solution
                    





# Exemplo de uso
if __name__ == "__main__":
    items = [(2, 4), (2, 5), (3, 7), (4,9), (4,6)]  # Exemplo de itens (valor, peso)
    capacity = 23  # Capacidade da mochila
    knapsack = KnapsackProblem(items, capacity) #cria o problema

    #constroi solucao inicial
    initial_solution = greedy_construct(knapsack, 0.5)
    print("Greedy:", initial_solution, calculate_total_value(initial_solution))


    # Simulated Annealing
    best_solution = simulated_annealing(knapsack, initial_solution, initial_temperature=1000, cooling_rate=0.95, num_iterations=1000)
    print("Simulated Annealing:", best_solution, calculate_total_value(best_solution))



