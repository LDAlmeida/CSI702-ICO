import random
import matplotlib.pyplot as plt
import numpy as np

class TravelingSalesmanProblem:
    def __init__(self, num_cities, capacity):
        self.num_cities = num_cities
        self.routes = []
        self.capacity = capacity
        self.cities_matrix = [[]]
        self.generate_cities_matrix()
        
    def generate_cities_matrix(self):
        cities_matrix = [[0 for _ in range(self.num_cities)] for _ in range(self.num_cities)]
        for i in range(self.num_cities):
            for j in range(self.num_cities):
                if i != j:
                    distance = random.randint(1, 10)
                    cities_matrix[i][j] = distance
                    cities_matrix[j][i] = distance
        self.cities_matrix = cities_matrix
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
            route_size = random.randint(2, self.num_cities - 1)
            start_city = random.randint(0, self.num_cities - 1)
            route = [start_city] + random.sample([city for city in range(self.num_cities) if city != start_city], route_size - 1)
            route.append(start_city)
            new_route = self.Route(route, self)
            population.append(new_route)
        self.routes = population
        return population

    class Route:
        def __init__(self, route, TSProblem):
            self.route = route
            self.total_distance = 0
            self.TSProblem = TSProblem
            self.aptitude = 0
            self.calculate_total_value()
            
        def calculate_total_value(self):
            total_value = 0
            num_cities = len(self.route)
            for i in range(num_cities):
                current_city_index = i % num_cities
                next_city_index = (i + 1) % num_cities
                distance = self.TSProblem.cities_matrix[self.route[current_city_index]][self.route[next_city_index]]
                total_value += distance
            self.total_distance = total_value
            return total_value
        
        def __str__(self):
            return f'Rota : {self.route} \n Distancia total: {self.total_distance} \n Aptitude: {self.aptitude}'
    
    @staticmethod
    def visualize_top_routes(routes, cities_coordinates):
        # Plot all cities
        for city, coord in enumerate(cities_coordinates):
            plt.scatter(*coord, c='black')
            plt.text(coord[0], coord[1], str(city))

        # Colors for the routes
        colors = ['blue', 'green', 'red', 'cyan', 'magenta']
        
        for idx, route in enumerate(routes):
            x = [cities_coordinates[city][0] for city in route]
            y = [cities_coordinates[city][1] for city in route]
            plt.plot(x, y, c=colors[idx % len(colors)], label=f'Route {idx + 1}')

        plt.title('Top 5 TSP Routes')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.legend()
        plt.show()

class GeneticAlgorythm:
    
    def __init__(self, pop_size, chromo_size, crossover_perc, mutation_perc):
        self.pop_size = pop_size
        self.chromo_size = chromo_size
        self.crossover_perc = crossover_perc
        self.mutation_perc = mutation_perc
        
    @staticmethod
    def crossover_OX(parent1, parent2):
        num_cities = len(parent1.route)
        if num_cities > 4:
            start, end = sorted(random.sample(range(1, num_cities - 1), 2))
            child_route = parent1.route[:-1]
            fill_positions = list(range(start, end)) + list(range(end, num_cities - 1)) + list(range(1, start))
            for position in fill_positions:
                if child_route[position] not in parent2.route[start:end] and position not in range(start, end):
                    for city in parent2.route:
                        if city not in child_route:
                            child_route[position] = city
                            break
            child_route.append(child_route[0])
            child = TravelingSalesmanProblem.Route(child_route, parent1.TSProblem)
        else:
            child = random.choice([parent1,parent2])
        return [child]

    @staticmethod
    def mutation_generic(route):
        idx1, idx2 = random.sample(range(1, len(route.route) - 1), 2)
        route.route[idx1], route.route[idx2] = route.route[idx2], route.route[idx1]
        return route
        
    @staticmethod    
    def parent_selection(style, population):
        parents = []
        if style == "Championship":
            while len(parents) < 2:
                parent_contestant1 = random.choice(population)
                parent_contestant2 = random.choice(population)
                if parent_contestant1.aptitude > parent_contestant2.aptitude:
                    parents.append(parent_contestant2)
                else:
                    parents.append(parent_contestant1)
        elif style == "Roulette":
            total_aptitude = sum(route.aptitude for route in population)
            weights = [route.aptitude / total_aptitude if total_aptitude > 0 else 1 / len(population) for route in population]
            first_parent = random.choices(population, weights, k=1)[0]
            if total_aptitude > 0:
                adjusted_weights = [w if route != first_parent else 0 for route, w in zip(population, weights)]
                total_adjusted_weights = sum(adjusted_weights)
                adjusted_weights = [w / total_adjusted_weights for w in adjusted_weights]
            else:
                adjusted_weights = [1 / (len(population) - 1) if route != first_parent else 0 for route in population]
            second_parent = random.choices(population, adjusted_weights, k=1)[0]
            parents = [first_parent, second_parent]
        elif style == "Elitist":
            sorted_population = sorted(population, key=lambda x: x.aptitude, reverse=True)
            parents = sorted_population[:2]
        elif style == "Random":
            parents.append(random.choice(population))
            parents.append(random.choice(population))
        return parents
       
    def calculate_avg_aptitude(self, population):
        total_aptitude = sum(route.TSProblem.calculate_aptitude(route) for route in population)
        avg_aptitude = total_aptitude / len(population) if len(population) > 0 else 0
        return avg_aptitude   
        
    def apply(self, problem, max_iterations):       
        for i in range(max_iterations):
            parents = self.parent_selection("Championship",problem.routes)
            if random.random() <= self.crossover_perc:
                cross_parents = self.crossover_OX(parents[0], parents[1])
                parents = cross_parents
            if random.random() <= self.mutation_perc:
                for parent in parents:
                    if len(parent.route) > 4:
                        parents.remove(parent)
                        parents.append(self.mutation_generic(parent))
            for parent in parents:
                problem.routes.append(parent)
            parents_to_remove = self.parent_selection("Roulette",problem.routes)
            for parent in parents_to_remove:
                try:
                    problem.routes.remove(parent)
                except Exception as e:
                    print(f"Removing failed: {e}")
        avg_aptitude = self.calculate_avg_aptitude(problem.routes)
        print(f"Average aptitude in generation {i}: {avg_aptitude}")
        return problem

if __name__ == "__main__":
    TSproblem = TravelingSalesmanProblem(num_cities=13, capacity=50)
    TSproblem.generate_population(pop_size=100)
    genetic_algorythm = GeneticAlgorythm(pop_size=len(TSproblem.routes), chromo_size=0, crossover_perc=0.8, mutation_perc=0.1)
    resulting_population = genetic_algorythm.apply(TSproblem,100)
    sorted_routes = sorted(resulting_population.routes, key=lambda x: TSproblem.calculate_aptitude(x), reverse=True)
    
    # Select top 5 routes
    top_routes = [route.route for route in sorted_routes[:5]]

    # Assuming city coordinates are known or generated here
    np.random.seed(42)  # For reproducible results
    cities_coordinates = [tuple(coord) for coord in np.random.rand(TSproblem.num_cities, 2) * 100]

    # Visualize the top 5 routes
    TSproblem.visualize_top_routes(top_routes, cities_coordinates)
