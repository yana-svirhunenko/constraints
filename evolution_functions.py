import copy
import random
from collections import defaultdict
from constants import *
from data_structures import *


def get_random_subject(simultaneous_lessons, group):

    subjects_with_hours = []
    for subject, hours in group.schedule['seminars'].items():
        subjects_with_hours.append((subject, 'seminars', hours))
    for subject, hours in group.schedule['lectures'].items():
        subjects_with_hours.append((subject, 'lectures', hours))

    subject = random.choice(subjects_with_hours)
    if subject[1] == 'lectures':
        if any(l.group.name == group.name for l in simultaneous_lessons):
            return None, None, None
        return subject, None, True
    for l in simultaneous_lessons:
        if l.group.name == group.name and subject[2]['group_2'] is not None:
            return subject, abs((l.und_group - 3)), True
        elif l.group.name == group.name and subject[2]['group_2'] is None:
            return None, None, None
    return subject, random.choice([1, 2]), False


def get_lecturer_and_auditorium(simultaneous_lessons, subject, lecturers, auditoriums):

    if subject[1] == 'lectures':
        for l in simultaneous_lessons:
            if l.subject_name == subject[0] and l.subject_type == 'lectures':
                return l.lecturer, l.auditorium

    try:
        available_lecturers = [l for l in lecturers if subject[0] in l.subjects and subject[1] in l.can_teach]
        lecturer = random.choice(available_lecturers)
        auditorium = random.choice(auditoriums)
    except:
        return None, None

    return lecturer, auditorium


def generate_simultaneous_lessons(g, l, a, i, j):

    simultaneous_lessons = []
    for _ in range(GROUPS_NUM):
        if random.choices([True, False], weights=[0.1, 0.9])[0]:
            continue
        group = random.choice(g)
        subject, und_gr, remove_group = get_random_subject(simultaneous_lessons, group)
        if subject is None:
            continue
        lecturer, auditorium = get_lecturer_and_auditorium(simultaneous_lessons, subject, l, a)
        time = subject[2]['group_1']
        if lecturer is None or auditorium is None:
            continue
        simultaneous_lessons.append(Lesson(group, und_gr, subject[0], subject[1], lecturer, auditorium, i, j, time))
        if auditorium in a:
            a.remove(auditorium)
        if lecturer in l:
            l.remove(lecturer)
        if remove_group:
            g.remove(group)

        if len(g) <= 0 or len(l) <= 0 or len(a) <= 0:
            break
    return simultaneous_lessons


def initialize_population(groups, lecturers, auditoriums):

    population = []
    for _ in range(POPULATION_SIZE):

        individual = {
            'day_1': [],
            'day_2': [],
            'day_3': [],
            'day_4': [],
            'day_5': []
        }

        for i in range(1, DAYS + 1):
          for j in range(1, MAXIMUM_LESSONS_PER_DAY + 1):
            g = copy.deepcopy(groups)
            l = copy.deepcopy(lecturers)
            a = copy.deepcopy(auditoriums)
            simultaneous_lessons = generate_simultaneous_lessons(g, l, a, i, j)
            individual[f'day_{i}'].append(simultaneous_lessons)
        population.append(individual)

    return population


def find_windows(schedule):

    windows_number = 0
    for i in range(MAXIMUM_LESSONS_PER_DAY):
      for j in range(GROUPS_NUM):
        if j == 1:
          k = i
          window = False
          while k < MAXIMUM_LESSONS_PER_DAY:
            if schedule[k][j] == 0:
              window = True
            if schedule[k][j] == 1 and window:
              windows_number += 1
            k += 1

    return windows_number


def count_lesson_hours(individual):

    lesson_hours = defaultdict(int)
    for day, lessons in individual.items():
        for sim_lessons in lessons:
            for l in sim_lessons:
                lesson_key = (l.group.name, l.und_group, l.subject_name, l.subject_type, l.total_hours)
                lesson_hours[lesson_key] += LESSON_LENGTH * WEEKS

    return dict(lesson_hours)


def fitness(individual, groups, lecturers):

    score = 0
    for day, lessons in individual.items():
      windows_number = 0
      prev_lesson_groups = [[0 for _ in range(len(groups))] for _ in range(MAXIMUM_LESSONS_PER_DAY)]
      prev_lesson_lecturers = [[0 for _ in range(len(lecturers))] for _ in range(MAXIMUM_LESSONS_PER_DAY)]
      for i, sim_lessons in enumerate(lessons):
        for l in sim_lessons:

          current_students = (
          l.group.student_number
          if l.und_group is None
          else l.group.group_1
          if l.und_group == 1
          else l.group.group_2
          )
          if current_students > l.auditorium.seats:
            score -= 1000

          index_1 = next((i for i, group in enumerate(groups) if l.group.name == group.name), None)
          index_2 = next((i for i, lecturer in enumerate(lecturers) if l.lecturer.name == lecturer.name), None)

          if index_1 is not None and index_2 is not None:
              prev_lesson_groups[i][index_1] = 1
              prev_lesson_lecturers[i][index_2] = 1
          else:
              print(f"Warning: Lecturer or Group not found for lesson {l}.")

      windows_number += find_windows(prev_lesson_groups)
      windows_number += find_windows(prev_lesson_lecturers)
      score -= windows_number * 500

    hours_offset = 0
    lesson_hours = count_lesson_hours(individual)

    for lesson, total_hours in lesson_hours.items():
        required_hours = lesson[-1]
        hours_offset += abs(required_hours - total_hours)

    score -= 100 * hours_offset

    return score


def selection(population, fitness_scores):

    selected = random.sample(list(enumerate(fitness_scores)), TOURNAMENT_SIZE)
    selected = sorted(selected, key=lambda x: x[1], reverse=True)
    best_idx = selected[0][0]
    return population[best_idx]


def crossover(parent1, parent2):

    if not isinstance(parent1, dict) or not isinstance(parent2, dict):
        raise TypeError("Both parents must be dictionaries.")
    days = list(parent1.keys())
    child1 = {}
    child2 = {}
    for i, day in enumerate(days):
      if random.choice([True, False]):
        child1[day] = parent1[day]
        child2[day] = parent2[day]
      else:
        child1[day] = parent2[day]
        child2[day] = parent1[day]

    return child1, child2


def mutate(individual, groups, lecturers, auditoriums):

    if random.random() < MUTATION_RATE:

        days = list(individual.keys())
        idx_1 = random.randint(0, DAYS - 1)
        day_key = days[idx_1]
        idx_2 = random.randint(0, MAXIMUM_LESSONS_PER_DAY - 1)
        g = copy.deepcopy(groups)
        l = copy.deepcopy(lecturers)
        a = copy.deepcopy(auditoriums)
        simultaneous_lessons = generate_simultaneous_lessons(g, l, a, idx_1 + 1, idx_2 + 1)
        individual[day_key][idx_2] = simultaneous_lessons

    return individual
