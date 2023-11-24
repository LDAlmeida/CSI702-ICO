import random
import copy

class KnapsackProblem:
    def __init__(self, items, capacity):
        self.items = items
        self.capacity = capacity

def calculate_total_value(solution):
    total_value = sum(item[0] for item in solution)
    return total_value


#Funcao de aptidao
#porcentagem de enchimento da mochila, caso passar retornar como 0.

def generate_population(knapsack, size):
    for x in range(size):
        

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

# Function to set a specific bit to 1
def set_bit(number, position):
    return number | (1 << position)

# Function to clear a specific bit to 0
def clear_bit(number, position):
    return number & ~(1 << position)

if __name__ == "__main__":
    items = [(2, 4), (2, 5), (3, 7), (4,9), (4,6)] # Exemplo de itens (valor, peso)
    capacity = 23
    knapsack = KnapsackProblem(items, capacity)
    s = 0b10001
    s = set_bit(s,0)
    print(s)