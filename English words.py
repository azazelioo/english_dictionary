import sqlite3
import os
import random

# Подключение к базе данных
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "English.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Создаём таблицу (если её нет)
cursor.execute('''CREATE TABLE IF NOT EXISTS Words
               (id INTEGER PRIMARY KEY,
               Word TEXT NOT NULL UNIQUE,
               Translate TEXT NOT NULL UNIQUE)''')
conn.commit()

def add_word():
    word = input("Введите слово на английском: ").strip().lower()
    translate = input("Введите перевод: ").strip().lower()

    try:
        cursor.execute('''INSERT INTO Words (Word, Translate) VALUES (?,?)''', (word,translate))
        conn.commit()
        print(f'Слово {word} успешно добавлено!')
    except sqlite3.IntegrityError:
        print(f'Такое слово или перевод уже есть в базе!')


def test_words():
    cursor.execute('''SELECT Word, Translate FROM Words''')
    words = cursor.fetchall()
    if not words:
        print(f"В словаре пока нет слов. Добавьте их сначала!")
        return
    word, correct_translate = random.choice(words)
    print(f"\nКак переводится слово: '{word}'?")
    user_translate = input("Ваш ответ: ").strip().lower()
    if user_translate == correct_translate:
        print("✅ Верно!")
    else:
        print(f"❌ Неверно! Правильный ответ: '{correct_translate}'")

def slovar():
    cursor.execute('''SELECT id, Word, Translate FROM Words ORDER BY id''')
    words = cursor.fetchall()
    if not words:
        print(f"В словаре пока нет слов. Добавьте их сначала!")
        return
    print('------------------------------------------------------')
    for i in range(len(words)):
        print(f'{words[i][0]}.', words[i][1], '-------', words[i][2])
    print('------------------------------------------------------')

def redact():
    number = int(input('Введите номер слова, которое Вы хотите изменить: '))
    new_word = input('Введите исправленное слово: ').strip().lower()
    new_translate = input('Введите исправленный перевод: ').strip().lower()
    cursor.execute('''UPDATE  Words SET Word = ?, Translate = ? WHERE id = ? ''', (new_word,new_translate, number))
    print('Слово успешно изменено!')
    conn.commit()
    
    

def main():
    while True:
        print("\n1. Добавить слово")
        print("2. Проверить знание слов")
        print("3. Выйти")
        print("4. Просмотреть словарь")
        print("5. Редактировать слово")
        choice = input("Выберите действие (1/2/3/4/5): ")
        if choice == "1":
            add_word()
        elif choice == "2":
            test_words()
        elif choice == "3":
            break
        elif choice == "4":
            slovar()
        elif choice == '5':
            redact()
        else:
            print("Некорректный ввод. Попробуйте снова.")
if __name__ == "__main__":
    main()
    conn.close()