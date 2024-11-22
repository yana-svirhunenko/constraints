from functions import *
from evolution_functions import *
from evolution_functions import LambdaConstraint
from database import *


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
groups_schedule = read_csv_to_groups(groups_file_path)
lecturers = read_csv_to_lecturers(lecturers_file_path)

groups_list = generate_groups(groups_schedule, (20, 40))
auditoriums_list = generate_auditoriums(GROUPS_NUM + 1, (20, 50), 40)
lecturers_list = generate_lecturers(lecturers)

constraints = [
    Constraint(group=["МІ-41"], day=[1, 2], lesson_period=1),
    Constraint(group=["МІ-42"], lecturer=['Dr. Іваненко'], auditorium='Аудиторія 1'),
    Constraint(group=["МІ-31", "ТТП-31"], subject_name=["Аналіз даних", "Комп'ютерні мережі"], lesson_period=[1, 2, 3])
]

lambda_constraints = [

    LambdaConstraint(
        lambda schedule: any(
            lesson.group.name == 'МІ-41' and lesson.lecturer.name == 'Dr. Іваненко' and lesson.day == 1
            for day, lessons in schedule.items()
            for sim_lessons in lessons
            for lesson in sim_lessons
        )
    ),

    LambdaConstraint(
        lambda schedule: all(
        len(sim_lessons) >= 2
        for day, lessons in schedule.items()
        for sim_lessons in lessons
        )
    ),

    LambdaConstraint(
        lambda schedule: sum(
        1 for day, lessons in schedule.items()
        for sim_lessons in lessons
        for lesson in sim_lessons
        if lesson.lecturer.name == 'Dr. Іваненко'
        ) > 3
    ),

    LambdaConstraint(
        lambda schedule: any(
            lesson.auditorium.name == 'Аудиторія 1' or 'Аудиторія 6' and lesson.lesson_period == 1 and lesson.day == 1
            for day, lessons in schedule.items()
            for sim_lessons in lessons
            for lesson in sim_lessons
        )
    ),

]


schedule, way = get_schedule(groups_list, lecturers_list, auditoriums_list, constraints, lambda_constraints)
print(f'Вартість шляху: {way}')
create_database()
save_schedule_to_db(schedule)
fetch_lessons()
