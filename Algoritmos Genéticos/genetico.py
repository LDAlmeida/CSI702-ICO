import random
import copy

class KnapsackProblem:
    def __init__(self, items, capacity):
        self.items = items
        self.capacity = capacity
        self.population = None
        
    def calculate_total_value(self, solution):
        total_value = sum(item[0] for item in solution)
        return total_value

    #Funcao de aptidao
    #porcentagem de enchimento da mochila, caso passar retornar como 0.
    def calculate_aptitude(self, guy):
        guy_value = self.calculate_total_value(guy)
        aptitude = guy_value/self.capacity
        
        return aptitude

    def generate_population(self, pop_size):
        generated_population = []
        binary_length = len(self.items)

        for _ in range(pop_size):
            guy = f'0b{random.getrandbits(binary_length):0{binary_length}b}'
            generated_population.append(guy)

        return generated_population

    def greedy_construct(self, alpha):
        items = copy.deepcopy(self.items)
        capacity = self.capacity
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


    class Population:
        def __init__(self, knapsack, size, guys):
            self.knapsack = knapsack
            self.size = size
            self.guys = guys
            self.avg_aptitude = 0
            
        def add_guy(self, guy):
            self.guys.append(guy)
            
        def calculate_pop_aptitude(self):
            sum_of_values = 0
            for guy in self.guys:
                sum_of_values += self.knapsack.calculate_aptitude(guy)
            avg_of_values = sum_of_values/len()
            print(f'Average aptitude: {avg_of_values}')            
    #chrome_size = a quantidade de items que podem ser inseridos. Quantidade de bits.
    #pop_size = tamanho da populacao a ser gerada.
    #funcao de avaliar -> deixar sempre ordenado

    #populacao
        #tamanho da populacao
        #lista de indv
        #media da aptidao (atualizar ao atualizar elementos)
        

    #individuo
        #funcao de aptidao
        #funcao objetivo


    #def genetico(knapsack, pop_size, chromo_size, crossover_perc, mutation_perc):
        # criar vetor de populacao
        # criar uma funcao de gerar uma populacao (generate_pop)
        # criar funcao de aptidao
        # avaliar toda aquela populacao depois que criada (ler individuo por individuo e calcular a funcao de aptidao daqueles individuos.)
        
        # entrar num loop que sao as geracoes daquele algoritmo genetico ate que atenda. O criterio de parada pode ser numero de geracoes
            # criar funcao de selecao de pais -> torneio, roleta, elitista ou aleatoria (selenionar dois cromosomos)
            # criar funcao operador de crossover [1111]/[2222] -> [1122]/[2211]
            # aplicar um operador de crossover com os dois selecionados
            # criar operador de mutacao (mudar um bit aleatorio)
            # calcular se o percentual de mutacao foi atingido
            # aplicar mutacao
            # inserir os individuos
            # avalia a populacao de novo
            # aplicar o metodo de selecao para remover 2 individuos
            # next

        # return populacao
        
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
    size = len(items)
    max_pop_size = size*size
    guys = knapsack.generate_population(max_pop_size)
    population = knapsack.Population(knapsack=knapsack, guys=guys, size=size)
    print(population.guys)
    # chamar genetico
      
    # imprimir a populacao (todos ou so x melhores), a media, a funcao de aptidao e objetiva de cada cromossomo que for imprimido
    