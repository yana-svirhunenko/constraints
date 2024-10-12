
class Group:
    def __init__(self, name, schedule, student_number, group_1=None, group_2=None):
        self.name = name
        self.schedule = schedule
        self.student_number = student_number
        self.group_1 = group_1
        self.group_2 = group_2

    def __str__(self):
        return (f"Group: {self.name}, "
                f"Student Number: {self.student_number}, "
                f"Group 1: {self.group_1}, "
                f"Group 2: {self.group_2}")


class Lecturer:
    def __init__(self, name, subjects, can_teach):
        self.name = name
        self.subjects = subjects
        self.can_teach = can_teach

    def __str__(self):
        return (f"Lecturer: {self.name}, "
                f"Subjects: {', '.join(self.subjects)}, "
                f"Can Teach: {', '.join(self.can_teach)}")


class Auditorium:
    def __init__(self, name, seats):
        self.name = name
        self.seats = seats

    def __str__(self):
        return f"Auditorium: {self.name}, Seats: {self.seats}"


class Lesson:
    def __init__(self, group, und_group, subject_name, subject_type, lecturer, auditorium, day, lesson_period, total_hours=None):
        self.group = group
        self.und_group = und_group
        self.subject_name = subject_name
        self.subject_type = subject_type
        self.lecturer = lecturer
        self.auditorium = auditorium
        self.day = day
        self.lesson_period = lesson_period
        self.total_hours = total_hours

    def __str__(self):
        return (f"Day: {self.day}, Lesson Period: {self.lesson_period}\n"
                f"Group: {self.group.name} - Undergroup: {self.und_group}\n"
                f"Lesson: {self.subject_name} ({self.subject_type})\n"
                f"Lecturer: {self.lecturer.name}\n"
                f"Auditorium: {self.auditorium.name}, Seats: {self.auditorium.seats}\n"
                )

    def to_dict(self):
        return {
            'group': self.group,
            'und_group': self.und_group,
            'subject_name': self.subject_name,
            'subject_type': self.subject_type,
            'lecturer': self.lecturer,
            'auditorium': self.auditorium,
            'day': self.day,
            'lesson_period': self.lesson_period,
            'total_hours': self.total_hours
        }
