import random
import numpy as np
import matplotlib.pyplot as plt

# Define city names and distance matrix for 8 cities
city_names = [
    "Karachi", "Lahore", "Islamabad", "Peshawar", "Quetta",
    "Multan", "Sialkot", "Faisalabad"
]

distance_matrix = [
    [0, 1210, 1410, 1520, 690, 900, 1225, 1150],
    [1210, 0, 375, 510, 960, 340, 125, 140],
    [1410, 375, 0, 185, 820, 550, 300, 250],
    [1520, 510, 185, 0, 950, 680, 460, 400],
    [690, 960, 820, 950, 0, 600, 990, 870],
    [900, 340, 550, 680, 600, 0, 410, 280],
    [1225, 125, 300, 460, 990, 410, 0, 200],
    [1150, 140, 250, 400, 870, 280, 200, 0]
]

# Define the TSP functions
def calculate_total_distance(route):
    total = 0
    for i in range(len(route)):
        total += distance_matrix[route[i]][route[(i + 1) % len(route)]]
    return total

def initialize_population(size, num_cities):
    return [random.sample(range(num_cities), num_cities) for _ in range(size)]

def mate(parent1, parent2):
    start, end = sorted(random.sample(range(len(parent1)), 2))
    child = [-1] * len(parent1)
    child[start:end+1] = parent1[start:end+1]
    p2_index = 0
    for i in range(len(parent1)):
        if child[i] == -1:
            while parent2[p2_index] in child:
                p2_index += 1
            child[i] = parent2[p2_index]
    return child

def mutate(route):
    i, j = random.sample(range(len(route)), 2)
    route[i], route[j] = route[j], route[i]
    return route

def bmo_tsp(pop_size=50, generations=200, mutation_rate=0.2):
    num_cities = len(distance_matrix)
    population = initialize_population(pop_size, num_cities)
    best_solution = None
    best_distance = float('inf')
    fitness_history = []

    for gen in range(generations):
        population = sorted(population, key=calculate_total_distance)
        if calculate_total_distance(population[0]) < best_distance:
            best_solution = population[0]
            best_distance = calculate_total_distance(population[0])

        new_population = population[:5]  # Elitism
        while len(new_population) < pop_size:
            parent1, parent2 = random.sample(population[:25], 2)
            child = mate(parent1, parent2)
            if random.random() < mutation_rate:
                child = mutate(child)
            new_population.append(child)

        population = new_population
        fitness_history.append(best_distance)

    return best_solution, best_distance, fitness_history

# Run optimizer
best_route, best_dist, fitness = bmo_tsp()

# Display results
print(" Best route:")
for city in best_route:
    print(city_names[city], end=" → ")
print(city_names[best_route[0]])
print(f" Total Distance: {best_dist} km")
