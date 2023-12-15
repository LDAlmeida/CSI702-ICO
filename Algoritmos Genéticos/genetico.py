import random

class KnapsackProblem:
    def __init__(self, items, capacity):
        self.items = items
        self.capacity = capacity
        self.population = None
        
    def calculate_total_value(self, guy):
        selected_items = [item for item, bit in zip(self.items, guy.chromo[2:]) if bit == '1']
        total_value = sum(item[0] for item in selected_items)
        return total_value

    def calculate_aptitude(self, guy):
        guy_value = self.calculate_total_value(guy)
        aptitude = guy_value/self.capacity
        
        if aptitude > 1:
            return 0
        else:
            return aptitude

    def generate_population(self, pop_size):
        generated_population = []
        binary_length = len(self.items)

        for _ in range(pop_size):
            chromo = f'0b{random.getrandbits(binary_length):0{binary_length}b}'
            guy = self.Guy(self, chromo)
            generated_population.append(guy)

        self.population = self.Population(self,pop_size,generated_population)
        
        return generated_population
    
    def crossover(self, guys):
        if len(guys) != 2:
            raise ValueError("The crossover function expects a list of two Guy instances.")

        binary_str1 = guys[0].chromo
        binary_str2 = guys[1].chromo

        if binary_str1.startswith('0b'):
            binary_str1 = binary_str1[2:]
        if binary_str2.startswith('0b'):
            binary_str2 = binary_str2[2:]

        if len(binary_str1) != len(binary_str2):
            raise ValueError("Binary strings must have the same length")

        length = len(binary_str1)
        crossover_point = length // 2

        new_binary_str1 = '0b' + binary_str1[:crossover_point] + binary_str2[crossover_point:]
        new_binary_str2 = '0b' + binary_str2[:crossover_point] + binary_str1[crossover_point:]

        return [self.Guy(guys[0].knapsack, new_binary_str1), self.Guy(guys[1].knapsack, new_binary_str2)]
    
    
    class Guy:
        def __init__(self, knapsack, chromo):
            self.knapsack = knapsack
            self.chromo = chromo
            self.aptitude = knapsack.calculate_aptitude(self)
            
        def mutate(self):
            binary_str = self.chromo

            if binary_str.startswith('0b'):
                binary_str = binary_str[2:]

            mutation_point = random.randint(0, len(binary_str) - 1)
            mutated_bit = '1' if binary_str[mutation_point] == '0' else '0'

            new_binary_str = '0b' + binary_str[:mutation_point] + mutated_bit + binary_str[mutation_point + 1:]

            return self.knapsack.Guy(self.knapsack, new_binary_str)
            
        def __str__(self):
            return str(f'{self.chromo} - {self.aptitude}')
        
    class Population:
        def __init__(self, knapsack, size, guys):
            self.knapsack = knapsack
            self.size = size
            self.guys = guys
            self.avg_aptitude = self.calculate_pop_aptitude()
            
        def add_guy(self, guy):
            self.guys.append(guy)
            self.calculate_pop_aptitude()
            
        def calculate_pop_aptitude(self):
            sum_of_values = 0
            for guy in self.guys:
                sum_of_values += self.knapsack.calculate_aptitude(guy)
            avg_of_values = sum_of_values/len(self.guys)
            self.avg_aptitude = avg_of_values
            print(f'Average aptitude: {avg_of_values}')
            
            return avg_of_values
            
def parent_selection(style, population):
    parents = []
    print('Selecting parents, may the odds be in your favor!')
    match style:
        case "Championship":
            print('Championship begins.')
            while len(parents) < 2:
                parent_contestant1 = random.choice(population.guys)
                parent_contestant2 = random.choice(population.guys)
                if parent_contestant1.aptitude > parent_contestant2.aptitude:
                    parents.append(parent_contestant2)
                else:
                    parents.append(parent_contestant1)
                print(f'{parents[len(parents)-1]} wins the round!')
                
        case "Roulette":
            parents = random.choices(population.guys,k=2)
            print(f'Roulette style winners are:')
            for parent in parents:
                print(parent)
            
        case "Elitist":
            sorted_population = sorted(population.guys, key=lambda x: x.aptitude, reverse=True)
            parents = sorted_population[:2]
            print(f'Elitist winners are:')
            for parent in parents:
                print(parent)
            
        case "Random":
            parents.append(random.choice(population.guys))
            parents.append(random.choice(population.guys))
            print(f'The lucky random style winners are:')
            for parent in parents:
                print(parent)
            
    return parents
       
def genetico(knapsack, pop_size, chromo_size, crossover_perc, mutation_perc):
    # criar vetor de populacao
    # criar uma funcao de gerar uma populacao (generate_pop)
    # criar funcao de aptidao
    # criar funcao de selecao de pais -> torneio, roleta, elitista ou aleatoria (selenionar dois cromosomos)
    # criar funcao operador de crossover [1111]/[2222] -> [1122]/[2211]
    guys = knapsack.generate_population(pop_size)
    population = knapsack.Population(knapsack=knapsack, guys=guys, size=chromo_size)
    
    # avaliar toda aquela populacao depois que criada (ler individuo por individuo e calcular a funcao de aptidao daqueles individuos.)
    population.calculate_pop_aptitude()
    
    # entrar num loop que sao as geracoes daquele algoritmo genetico ate que atenda. O criterio de parada pode ser numero de geracoes
    max_generations = 100
    for i in range(max_generations):
        parents = parent_selection("Championship",population)
        # aplicar um operador de crossover com os dois selecionados
        if random.random() <= crossover_perc:
            cross_parents = knapsack.crossover(parents)
            parents = cross_parents
            
        # criar operador de mutacao (mudar um bit aleatorio)
        # calcular se o percentual de mutacao foi atingido
        # aplicar mutacao
        if random.random() <= mutation_perc:
            for parent in parents:
                parents.remove(parent)
                parents.append(parent.mutate())
                

        # inserir os individuos
        for parent in parents:
            # avalia a populacao de novo
            population.add_guy(parent)
            print(f'Adding {parent} ...')
            
        # aplicar o metodo de selecao para remover 2 individuos
        parents_to_remove = parent_selection("Roulette",population)
        for parent in parents_to_remove:
            print(f'Removing {parent} ...')
            try:
                population.guys.remove(parent)
            except Exception as e:
                print("Removing failed")
        # next

    # return populacao
    return population
    
# Function to set a specific bit to 1
def set_bit(number, position):
    return number | (1 << position)

# Function to clear a specific bit to 0
def clear_bit(number, position):
    return number & ~(1 << position)


         
if __name__ == "__main__":
    items = [
    (2, 4), (2, 5), (3, 7), (4, 9), (4, 6), (10, 4), (20, 20), (4, 1), (20, 10),
    (10, 7), (8, 50), (9, 20), (12, 17),
    #itens adicionais
    (15, 8), (6, 12), (18, 15), (7, 3), (5, 10),
    (14, 2), (3, 18), (9, 6), (12, 8), (11, 5)
]
    capacity = 100
    knapsack = KnapsackProblem(items, capacity)
    chromossome_size = len(items)
    max_pop_size = chromossome_size*chromossome_size
    # chamar genetico
    resulting_population = genetico(knapsack,max_pop_size,chromossome_size,1,0.1) 
    # imprimir a populacao (todos ou so x melhores), a media, a funcao de aptidao e objetiva de cada cromossomo que for imprimido
    print("And here come the results...")
    print(f"Average aptitude: {resulting_population.avg_aptitude}")
    sorted_population = sorted(resulting_population.guys, key=lambda x: x.aptitude, reverse=True)
    for guy in sorted_population:
        if guy.aptitude != 0:
            print(guy)
            print(f'Value: {knapsack.calculate_total_value(guy)}')