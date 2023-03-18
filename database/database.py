# Создаем шаблон заполнения # "игрушечной" базы данных из питоновского словаря
user_dict_template: dict = {'correct_answers': int, 'questions': int, 'SCORE': float}

# Инициализируем "базу данных"
users_db: dict = {}
# SCORE=correct_answers/total_questions
