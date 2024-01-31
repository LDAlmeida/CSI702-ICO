import random

class TravelingSalesmanProblem:
    def __init__(self, num_cities, capacity):
        self.num_cities = num_cities
        self.routes = []
        self.capacity = capacity
        self.cities_matrix = [[]]
        self.generate_cities_matrix()
        
    def generate_cities_matrix(self):
        # Initialize an empty matrix
        cities_matrix = [[0 for _ in range(self.num_cities)] for _ in range(self.num_cities)]

        # Populate the matrix with random distances (symmetric)
        for i in range(self.num_cities):
            for j in range(self.num_cities):  # Fix: iterate over the range of self.num_cities
                if i != j:
                    distance = random.randint(1, 100)  # Adjust the range as needed
                    cities_matrix[i][j] = distance
                    cities_matrix[j][i] = distance

        return cities_matrix

    def calculate_aptitude(self, route):
        aptitude = route.total_distance/self.capacity
        
        if aptitude > 1:
            return 0
        else:
            return aptitude

    def generate_population(self, pop_size):
        population = []

        for _ in range(pop_size):
            # Generate a random route (vector of cities)
            route = self.Route(list(range(self.num_cities)), self)
            random.shuffle(route.route)  # Shuffle to avoid duplicates
            # Add the route to the population
            population.append(route)

        self.routes = population
        
        return population

    class Route:
        def __init__(self, route, TSProblem):
            self.route = route
            self.total_distance = 0
            self.TSProblem = TSProblem
            self.calculate_total_value()
            
        def calculate_total_value(self):
            total_value = 0
            num_cities = len(self.route)

            for i in range(num_cities):
                # Use modulo to wrap around the indices
                current_city_index = i % num_cities
                next_city_index = (i + 1) % num_cities

                distance = self.TSProblem.cities_matrix[self.route[current_city_index]][self.route[next_city_index]]
                total_value += distance

            self.total_distance = total_value
            return total_value
        
class GeneticAlgorythm:
    
    def __init__(self, pop_size, chromo_size, crossover_perc, mutation_perc):
        self.pop_size = pop_size
        self.chromo_size = chromo_size
        self.crossover_perc = crossover_perc
        self.mutation_perc = mutation_perc
        
    @staticmethod
    def crossover_OX(parent1, parent2):
        num_cities = len(parent1.route)
        start, end = sorted(random.sample(range(num_cities), 2))

        # Create a copy of the parents
        child_route = parent1.route[:]

        # Fill the gap with cities from the second parent
        for city in parent2.route:
            if city not in child_route[start:end]:
                child_route[start] = city
                start = (start + 1) % num_cities

        # Create a new route using the child_route
        child = TravelingSalesmanProblem.Route(child_route, parent1.TSProblem)

        return child
    
    @staticmethod
    def mutation_generic(route):
        # Swap two elements in the route vector in place
        idx1, idx2 = random.sample(range(len(route)), 2)
        route[idx1], route[idx2] = route[idx2], route[idx1]
        
    @staticmethod    
    def parent_selection(style, population):
        parents = []
        print('Selecting parents, may the odds be in your favor!')

        if style == "Championship":
            print('Championship begins.')
            while len(parents) < 2:
                parent_contestant1 = random.choice(population)
                parent_contestant2 = random.choice(population)
                if parent_contestant1.aptitude > parent_contestant2.aptitude:
                    parents.append(parent_contestant2)
                else:
                    parents.append(parent_contestant1)
                print(f'{parents[len(parents)-1]} wins the round!')

        elif style == "Roulette":
            parents = random.choices(population, k=2)
            print(f'Roulette style winners are:')
            for parent in parents:
                print(parent)

        elif style == "Elitist":
            sorted_population = sorted(population, key=lambda x: x.aptitude, reverse=True)
            parents = sorted_population[:2]
            print(f'Elitist winners are:')
            for parent in parents:
                print(parent)

        elif style == "Random":
            parents.append(random.choice(population))
            parents.append(random.choice(population))
            print(f'The lucky random style winners are:')
            for parent in parents:
                print(parent)

        return parents
       
    def calculate_avg_aptitude(self, population):
        total_aptitude = sum(route.TSProblem.calculate_aptitude(route) for route in population)
        avg_aptitude = total_aptitude / len(population) if len(population) > 0 else 0
        return avg_aptitude   
        
    def apply(self, problem, max_iterations):       
        # entrar num loop que sao as geracoes daquele algoritmo genetico ate que atenda. O criterio de parada pode ser numero de geracoes
        for i in range(max_iterations):
            parents = self.parent_selection("Championship",problem.routes)
            # aplicar um operador de crossover com os dois selecionados
            if random.random() <= self.crossover_perc:
                cross_parents = self.crossover_OX(parents[0], parents[1])
                parents = cross_parents

            if random.random() <= self.mutation_perc:
                for parent in parents:
                    parents.remove(parent)
                    parents.append(parent.mutate())

            for parent in parents:
                problem.routes.append(parent)
                
            parents_to_remove = self.parent_selection("Roulette",problem.routes)
            for parent in parents_to_remove:
                try:
                    problem.routes.remove(parent)
                except Exception as e:
                    print(f"Removing failed: {e}" )
                    
        avg_aptitude = self.calculate_avg_aptitude(problem.routes)
        print(f"Average aptitude in generation {i}: {avg_aptitude}")
        return problem
   
    
if __name__ == "__main__":
    TSproblem = TravelingSalesmanProblem(num_cities=100, capacity=50)
    TSproblem.generate_population(pop_size=1000)

    resulting_population = GeneticAlgorythm(pop_size=len(TSproblem.routes), chromo_size=0, crossover_perc=0.8, mutation_perc=0.1)

    sorted_population = sorted(resulting_population.routes, key=lambda x: TSproblem.calculate_aptitude(x), reverse=True)
    for route in sorted_population:
        if route.aptitude != 0:
            print(route)
            print(f'Value: {TSproblem.calculate_aptitude(route)}')