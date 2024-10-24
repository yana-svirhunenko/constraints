from functions import *
from evolution_functions import *
from database import *


def genetic_algorithm(groups, lecturers, auditoriums):

    population = initialize_population(groups, lecturers, auditoriums)

    for generation in range(GENERATIONS):
        fitness_scores = [fitness(individual, groups, lecturers) for individual in population]
        new_population = []
        while len(new_population) < POPULATION_SIZE:

            parent1 = selection(population, fitness_scores)
            parent2 = selection(population, fitness_scores)
            child1, child2 = crossover(parent1, parent2)
            c1_m = mutate(copy.deepcopy(child1), groups, lecturers, auditoriums)
            c2_m = mutate(copy.deepcopy(child2), groups, lecturers, auditoriums)
            new_population.extend([child1, child2, c1_m, c2_m])

        population = new_population

        best_fitness = max(fitness_scores)
        print(f"Generation {generation}, Best Fitness: {best_fitness}")
        if best_fitness >= 0:
            print()
            break

    final_fitness_scores = [fitness(individual, groups, lecturers) for individual in population]
    best_individual_idx = final_fitness_scores.index(max(final_fitness_scores))
    print()
    return population[best_individual_idx]


def print_individual(individual):

    sorted_days = sorted(individual.keys(), key=lambda x: int(x.split('_')[1]))
    for day in sorted_days:
        lessons = individual[day]
        if not lessons:
            print("  No lessons scheduled.")
        else:
            for lesson_list in lessons:
                for lesson in lesson_list:
                    print(lesson)
        print()



groups_file_path = 'groups_data.csv'
lecturers_file_path = 'lecturers_data.csv'
#write_group_data_to_csv(groups, groups_file_path)
#write_lecturers_data_to_csv(lecturers, lecturers_file_path)
groups_schedule = read_csv_to_groups(groups_file_path)
lecturers = read_csv_to_lecturers(lecturers_file_path)

groups_list = generate_groups(groups_schedule, (20, 40))
auditoriums_list = generate_auditoriums(GROUPS_NUM + 1, (20, 50), 40)
lecturers_list = generate_lecturers(lecturers)

#print_data(groups_list, lecturers_list, auditoriums_list, groups_schedule)
schedule = genetic_algorithm(groups_list, lecturers_list, auditoriums_list)

create_database()
save_schedule_to_db(schedule)
fetch_lessons()
