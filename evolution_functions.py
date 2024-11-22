import copy
import random
from collections import defaultdict
from constants import *
from data_structures import *


class Constraint:

    def __init__(self, group=None, und_group=None, subject_name=None, subject_type=None,
                 lecturer=None, auditorium=None, day=None, lesson_period=None):

        self.group = group if isinstance(group, list) else [group] if group else None
        self.und_group = und_group if isinstance(und_group, list) else [und_group] if und_group else None
        self.subject_name = subject_name if isinstance(subject_name, list) else [subject_name] if subject_name else None
        self.subject_type = subject_type if isinstance(subject_type, list) else [subject_type] if subject_type else None
        self.lecturer = lecturer if isinstance(lecturer, list) else [lecturer] if lecturer else None
        self.auditorium = auditorium if isinstance(auditorium, list) else [auditorium] if auditorium else None
        self.day = day if isinstance(day, list) else [day] if day else None
        self.lesson_period = lesson_period if isinstance(lesson_period, list) else [lesson_period] if lesson_period else None

    def check_constraint(self, schedule, i, j):

        if self.day is not None:
            if any(self.day) < i:
                return True

        if self.day is not None and self.lesson_period is not None:
            if any(self.day) < i or (any(self.day) == i and any(self.lesson_period) < j):
                return True

        for day, lessons in schedule.items():
            for sim_lessons in lessons:
                for lesson in sim_lessons:

                    if self.group and lesson.group.name not in self.group:
                        continue
                    if self.und_group and lesson.und_group not in self.und_group:
                        continue
                    if self.subject_name and lesson.subject_name not in self.subject_name:
                        continue
                    if self.subject_type and lesson.subject_type not in self.subject_type:
                        continue
                    if self.lecturer and lesson.lecturer.name not in self.lecturer:
                        continue
                    if self.auditorium and lesson.auditorium.name not in self.auditorium:
                        continue
                    if self.day and lesson.day not in self.day:
                        continue
                    if self.lesson_period and lesson.lesson_period not in self.lesson_period:
                        continue
                    return True
        return False


class LambdaConstraint:

    def __init__(self, predicate):
        if not callable(predicate):
            raise ValueError("Predicate must be callable.")
        self.predicate = predicate

    def check_constraint(self, schedule):
        return self.predicate(schedule)


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


def check(sc, constr, i, j):
    for c in constr:
        if not c.check_constraint(sc, i, j):
            return False
    return True


def check_lambda(sc, constr):
    for c in constr:
        if not c.check_constraint(sc):
            return False
    return True


def get_schedule(groups, lecturers, auditoriums, constraints=None, lambda_constraints=None):

    attempts = 1
    while True:
        individual = {
            'day_1': [],
            'day_2': [],
            'day_3': [],
            'day_4': [],
            'day_5': []
        }

        for i in range(1, DAYS + 1):
            j = 1
            while j <= MAXIMUM_LESSONS_PER_DAY:
                g = copy.deepcopy(groups)
                l = copy.deepcopy(lecturers)
                a = copy.deepcopy(auditoriums)
                simultaneous_lessons = generate_simultaneous_lessons(g, l, a, i, j)
                new_individual = copy.deepcopy(individual)
                new_individual[f'day_{i}'].append(simultaneous_lessons)

                if check(new_individual, constraints, i, j):
                    individual = new_individual
                    j += 1
                attempts += 1

        if check_lambda(individual, lambda_constraints):
            return individual, attempts
