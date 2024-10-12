import sqlite3
from prettytable import PrettyTable
from constants import *


def create_database():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS schedules (
                id INTEGER PRIMARY KEY AUTOINCREMENT
            )
        ''')
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS lessons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                schedule_id INTEGER,  -- Foreign key to reference the schedules table
                group_name TEXT,
                und_group TEXT,
                subject_name TEXT,
                subject_type TEXT,
                lecturer TEXT,
                auditorium TEXT,
                day TEXT,
                lesson_period TEXT,
                total_hours INTEGER,
                FOREIGN KEY (schedule_id) REFERENCES schedules(id) ON DELETE CASCADE
            )
        ''')
    conn.commit()
    conn.close()


def insert_schedule():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO schedules DEFAULT VALUES
    ''')
    schedule_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return schedule_id


def insert_lesson(lesson, schedule_id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO lessons (schedule_id, group_name, und_group, subject_name, subject_type, 
                             lecturer, auditorium, day, lesson_period, total_hours)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (schedule_id, lesson.group.name, lesson.und_group, lesson.subject_name, lesson.subject_type,
          lesson.lecturer.name, lesson.auditorium.name, lesson.day, lesson.lesson_period, lesson.total_hours))

    conn.commit()
    conn.close()


def save_schedule_to_db(individual):

    schedule_id = insert_schedule()
    for day, lessons in individual.items():
        for lesson_group in lessons:
            for lesson in lesson_group:
                insert_lesson(lesson, schedule_id)


def fetch_lessons():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM schedules ORDER BY id DESC LIMIT 1')
    last_schedule = cursor.fetchone()
    if last_schedule is None:
        print("No schedules found.")
        return

    last_schedule_id = last_schedule[0]
    cursor.execute('SELECT * FROM lessons WHERE schedule_id = ?', (last_schedule_id,))
    lessons = cursor.fetchall()
    conn.close()
    table = PrettyTable()
    table.field_names = ["День", "Пара", "Група", "Підгрупа", "Предмет", "Тип предмету", "Викладач", "Аулиторія"]
    grouped_lessons = {}

    for lesson in lessons:
        group_name = lesson[2]
        und_group_name = lesson[3]
        subject_name = lesson[4]
        subject_type = lesson[5]
        lecturer_name = lesson[6]
        auditorium = lesson[7]
        day = lesson[8]
        lesson_period = lesson[9]

        key = (day, lesson_period)
        if key not in grouped_lessons:
            grouped_lessons[key] = []
        grouped_lessons[key].append([group_name, und_group_name, subject_name, subject_type, lecturer_name, auditorium])

    for (day, lesson_period), lessons in grouped_lessons.items():
        for lesson in lessons:
            table.add_row([day, lesson_period, *lesson[:6]])
        table.add_row(["", "_______", "_______", "_______", "________________________", "_______", "_______", "_______"])

    print(table)
