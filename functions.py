import csv
import random
from data_structures import *


def write_group_data_to_csv(groups, csv_filename):

    headers = ['name', 'category', 'subject', 'group_1_hours', 'group_2_hours']
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:

        writer = csv.writer(file)
        writer.writerow(headers)
        for group in groups:
            name = group['name']
            for subject, hours in group['lectures'].items():
                writer.writerow([name, 'lectures', subject, hours, ''])
            for subject, hours in group['seminars'].items():
                if isinstance(hours, dict):
                    writer.writerow([name, 'seminars', subject, hours['підгрупа 1'], hours['підгрупа 2']])
                else:
                    writer.writerow([name, 'seminars', subject, hours, ''])


def write_lecturers_data_to_csv(lecturers, csv_filename):

    headers = ['name', 'category', 'subject']
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for lecturer in lecturers:
            name = lecturer['name']
            for subject in lecturer['subjects']:
                if 'lectures' in lecturer['can_teach']:
                    writer.writerow([name, 'lectures', subject])
                if 'seminars' in lecturer['can_teach']:
                    writer.writerow([name, 'seminars', subject])


def read_csv_to_groups(file_path):

    groups_data = {}
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            group_name = row['name']
            category = row['category']
            subject = row['subject']
            group_1_hours = int(row['group_1_hours']) if row['group_1_hours'] else None
            group_2_hours = int(row['group_2_hours']) if row['group_2_hours'] else None

            if group_name not in groups_data:
                groups_data[group_name] = {'lectures': {}, 'seminars': {}}

            groups_data[group_name][category][subject] = {'group_1': group_1_hours, 'group_2': group_2_hours}

    return groups_data


def read_csv_to_lecturers(file_path):

    lecturers_data = {}
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            lecturer_name = row['name']
            category = row['category']
            subject = row['subject']

            if lecturer_name not in lecturers_data:
                lecturers_data[lecturer_name] = {
                    'subjects': [],
                    'can_teach': []
                }
            if subject not in lecturers_data[lecturer_name]['subjects']:
                lecturers_data[lecturer_name]['subjects'].append(subject)
            if category not in lecturers_data[lecturer_name]['can_teach']:
                lecturers_data[lecturer_name]['can_teach'].append(category)
    lecturers = [
        {
            'name': name,
            'subjects': data['subjects'],
            'can_teach': data['can_teach']
        }
        for name, data in lecturers_data.items()
    ]

    return lecturers


def generate_groups(groups, students_num_range):

    groups_ = []
    for group_name, schedule in groups.items():

        student_num = random.randint(*students_num_range)
        group_1 = student_num // 2 + random.randint(0, 3)
        group_2 = student_num - group_1
        group_obj = Group(group_name, schedule, student_num, group_1, group_2)
        groups_.append(group_obj)

    return groups_


def generate_auditoriums(num_auditoriums, seat_range, max_students):

    auditoriums = []
    for i in range(1, num_auditoriums + 1):
        seats = random.randint(seat_range[0], seat_range[1])
        auditorium_obj = Auditorium(f"Аудиторія {i}", seats)
        auditoriums.append(auditorium_obj)

    if any(auditorium.seats >= max_students for auditorium in auditoriums):
        return auditoriums
    else:
        auditoriums[0].seats = max_students
        return auditoriums


def generate_lecturers(lecturers_data):

    lecturers = []
    for lecturer in lecturers_data:
        lecturer_obj = Lecturer(lecturer['name'], lecturer['subjects'], lecturer['can_teach'])
        lecturers.append(lecturer_obj)
    return lecturers


def print_data(groups_list, lecturers_list, auditoriums_list, groups_schedule):

    for group in groups_list:
        print(f"Group: {group.name}, Students: {group.student_number}, Group 1: {group.group_1}, Group 2: {group.group_2}")
    print("-" * 50)
    print()

    for group_name, schedule in groups_schedule.items():
        print(f"Group: {group_name}")
        print("Lectures:")
        for subject, hours in schedule['lectures'].items():
            print(f"  {subject}: {hours} hours")
        print("Seminars:")
        for subject, subgroups in schedule['seminars'].items():
            print(f"  {subject}: {subgroups} hours")
    print("-" * 50)
    print()

    for auditorium in auditoriums_list:
        print(f"Auditorium: {auditorium.name}, Seats: {auditorium.seats}")
    print("-" * 50)
    print()

    for lecturer in lecturers_list:
        print(f"Lecturer: {lecturer.name}, Subjects: {', '.join(lecturer.subjects)}, Can Teach: {', '.join(lecturer.can_teach)}")
    print("-" * 50)
    print()