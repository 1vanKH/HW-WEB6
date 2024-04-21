import logging
from faker import Faker
import random
import sqlite3
from sqlite3 import Error
import os
from faker.providers import DynamicProvider

subject_provider = DynamicProvider(
     provider_name="subject",
     elements=["Biology","History","Economics","Philosophy","Engineering","Mathematics","Chemistry","Physics"],
)

fake = Faker()

fake.add_provider(subject_provider)


def create_db():
    # читаємо файл зі скриптом для створення БД
    with open('create_table.sql', 'r') as f:
        sql = f.read()

    # створюємо з'єднання з БД (якщо файлу з БД немає, він буде створений)
    with sqlite3.connect('University.db') as con:
        cur = con.cursor()
        # виконуємо скрипт із файлу, який створить таблиці в БД
        cur.executescript(sql)

    # Додавання груп
    for _ in range(3):
        cur.execute("INSERT INTO groups (name) VALUES (?)", (fake.word(),))

    # Додавання викладачів
    for _ in range(4):
        cur.execute("INSERT INTO teachers (name) VALUES (?)", (fake.name(),))

    # Додавання предметів із вказівкою викладача
    for teacher_id in range(1, 4):
        for _ in range(2):
            cur.execute("INSERT INTO subjects (name, teacher_id) VALUES (?, ?)", (fake.unique.subject(), teacher_id))

    # Додавання студентів і оцінок
    for group_id in range(1, 4):
        for _ in range(10):
            cur.execute("INSERT INTO students (name, group_id) VALUES (?, ?) RETURNING id",
                        (fake.name(), group_id))
            student_id = cur.fetchone()[0]
            for subject_id in range(1, 7):
                for _ in range(3):
                    cur.execute("INSERT INTO grades (student_id, subject_id, grade, date_received) VALUES (?, ?, ?, ?)",
                                (student_id, subject_id, random.randint(0, 100), fake.date_this_decade()))

    try:
        # Збереження змін
        con.commit()
    except Error as e:
        logging.error(e)
        con.rollback()
    finally:
        # Закриття підключення
        cur.close()
        con.close()


if __name__ == "__main__":
    if os.path.exists("University.db"):
        numb_query=input("Enter number of query: ")
        query=f"query_{numb_query}.sql"
        with open(query, "r") as f:
            sql = f.read()
        with sqlite3.connect('University.db') as con:
            cur = con.cursor()
            cur.execute(sql)
            print(cur.fetchall())
            
    else:
        create_db()
