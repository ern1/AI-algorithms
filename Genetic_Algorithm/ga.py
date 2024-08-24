import math
import random

class Individual:
    def __init__(self, path = [], distance = 0.0, fitness = 0.0, age = 0):
        self.path = path
        self.distance = distance
        self.fitness = fitness
        self.age = age
        
    def calculateFitness(self):
        self.distance = 0.0
        for i, city in enumerate(self.path[1:], start = 0):
            test1 = city
            test2 = self.path[i]
            self.distance += city.distanceTo(self.path[i])

        self.distance += self.path[-1].distanceTo(self.path[0])
        self.fitness = 1.0 / self.distance

    # Ordered crossover
    def crossover(self, ind2):
        size = len(self.path)
        child1 = []
        child2 = []
        
        cp1, cp2 = random.randint(1, size), random.randint(1, size)
        start, end = min(cp1, cp2), max(cp1, cp2)

        for loc in ind2.path:
            if loc not in self.path[start:end]:
                child1.append(loc)
        for loc in self.path:
            if loc not in ind2.path[start:end]:
                child2.append(loc)
        for i, loc in enumerate(self.path[start:end], start = start):
            child1.insert(i, loc)
        for i, loc in enumerate(ind2.path[start:end], start = start):
            child2.insert(i, loc)

        return Individual(child1), Individual(child2)

    # Reverse a random section of the path
    def mutate(self, p):
        if p > random.uniform(0, 1):
            size = len(self.path)
            cp1, cp2 = random.randint(1, size), random.randint(1, size)
            start, end = min(cp1, cp2), max(cp1, cp2)
            self.path[start:end] = self.path[start:end][::-1]

class Location:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    def distanceTo(self, location_to):
        return math.sqrt(math.pow(location_to.x - self.x, 2) + math.pow(location_to.y - self.y, 2))

def initializePopulation(population, size, locations):
    for _ in range(size):
        c = list(locations[1:])
        random.shuffle(c)
        c.insert(0, locations[0])
        population.append(Individual(c))

# Tournament selection
def ts(population, k):
    parents = []
    for i in range(2):
        candidates = list(population)
        random.shuffle(candidates)
        candidates = candidates[0:k]
        candidates.sort(key = lambda x: x.fitness, reverse = True)
        parents.append(candidates[0])
    return parents[0], parents[1]

def tsp_ga(locations):
    POPULATION_SIZE = 100
    MUTATION_PROBABILITY = 0.3
    ELITIST_SIZE = 20
    
    # Create population
    population = []
    initializePopulation(population, POPULATION_SIZE, locations)
    for individual in population:
        individual.calculateFitness()

    best_ind = population[0]
    generations = 0
    gen_since_improvement = 0

    while best_ind.distance > 9000.0 or gen_since_improvement < 5000:
        childs = []
        p1, p2 = ts(population, 2)
        c1, c2 = p1.crossover(p2)
        childs.append(c1)
        childs.append(c2)

        for child in childs:
            # Mutate
            child.mutate(MUTATION_PROBABILITY)
 
            # Calculate fitness
            child.calculateFitness()

            population.sort(key = lambda x: x.fitness, reverse = True)
            best_inds = population[:ELITIST_SIZE]

            # Replace oldest individual not in best_inds in population with child
            population.sort(key = lambda x: x.age, reverse = True)
            for j in range(0, POPULATION_SIZE):
                if population[j] not in best_inds:
                    population[j] = child
                    break

            if child.fitness > best_ind.fitness:
                best_ind = Individual(list(child.path), child.distance, child.fitness)
                print('Generation: {}\nFitness: {} - Distance: {}\n'
                      .format(generations, str(best_ind.fitness), str(best_ind.distance)))
                gen_since_improvement = 0

        if not generations % 500:
            print('Generation: {}\nFitness: {} - Distance: {}\n'
                  .format(generations, str(best_ind.fitness), str(best_ind.distance)))

        # Increase age of population
        for ind in population:
            ind.age += 1

        generations += 1
        gen_since_improvement += 1
        
    return best_ind

def read_file(file_path, locations):
    file = open(file_path, 'r')
    lines = file.readlines()

    for line in lines[6:]:
        if 'EOF' in line:
            break
        id, x, y = map(float, line.split(' '))
        locations.append(Location(id, x, y))

def main():
    locations = []
    read_file('berlin52', locations)
    solution = tsp_ga(locations)
    print('Best distance: {}\n'.format(str(solution.distance)))

if __name__ == '__main__':
   main()
