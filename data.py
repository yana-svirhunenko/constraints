Mi41 = {
    'name': 'МІ-41',
    'lectures': {
        'Теорія прийняття рішень': 28,
        'Статистичне моделювання в задачах штучного інтелекту': 28,
        'Інтелектуальні системи': 28,
        'Інформаційні технології': 14,
        'Складність алгоритмів': 14,
        'Основи комп’ютерної лінгвістики': 14
    },
    'seminars': {
        'Основи комп’ютерної лінгвістики': {
            'підгрупа 1': 14,
            'підгрупа 2': 14
        },
        'Інформаційні технології': 14,
        'Теорія прийняття рішень': 14
    }
}

Mi42 = {
    'name': 'МІ-42',
    'lectures': {
        'Теорія прийняття рішень': 28,
        'Статистичне моделювання в задачах штучного інтелекту': 28,
        'Інтелектуальні системи': 28,
        'Інформаційні технології': 14,
        'Складність алгоритмів': 14,
        'Основи комп’ютерної лінгвістики': 14
    },
    'seminars': {
        'Основи комп’ютерної лінгвістики': {
            'підгрупа 1': 14,
            'підгрупа 2': 14
        },
        'Інформаційні технології': 14,
        'Теорія прийняття рішень': 14
    }
}

TTP41 = {
    'name': 'ТТП-41',
    'lectures': {
        'Теорія прийняття рішень': 28,
        'Інтелектуальні системи': 28,
        'Інформаційні технології': 14,
        'Основи управління ІТ проектами': 28,
    },
    'seminars': {
        'Інформаційні технології': 14,
        'Теорія прийняття рішень': 14,
        'Основи управління ІТ проектами': {
            'підгрупа 1': 14,
            'підгрупа 2': 14
        }
    }
}

TTP42 = {
    'name': 'ТТП-42',
    'lectures': {
        'Теорія прийняття рішень': 28,
        'Інформаційні технології': 14,
        'Основи управління ІТ проектами': 28
    },
    'seminars': {
        'Інформаційні технології': 14,
        'Теорія прийняття рішень': 14,
        'Основи управління ІТ проектами': {
            'підгрупа 1': 14,
            'підгрупа 2': 14
        }
    }
}

lecturers = [
    {'name': 'Dr. Іваненко', 'subjects': ['Теорія прийняття рішень', 'Інтелектуальні системи'], 'can_teach': ['lectures', 'seminars']},
    {'name': 'Dr. Петренко', 'subjects': ['Статистичне моделювання в задачах штучного інтелекту'], 'can_teach': ['lectures']},
    {'name': 'Dr. Сидоренко', 'subjects': ['Основи комп’ютерної лінгвістики', 'Нейронні мережі'], 'can_teach': ['lectures', 'seminars']},
    {'name': 'Dr. Бойко', 'subjects': ['Інформаційні технології'], 'can_teach': ['lectures', 'seminars']},
    {'name': 'Dr. Гнатюк', 'subjects': ['Складність алгоритмів'], 'can_teach': ['lectures']},
    {'name': 'Dr. Ковальчук', 'subjects': ['Основи управління ІТ проектами', 'Розробка ПЗ під мобільні платформи', 'Методи паралельних обчислень'], 'can_teach': ['lectures', 'seminars']},
]

groups = [Mi41, Mi42, TTP41, TTP42]