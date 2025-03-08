import argparse
import sqlite3
from datetime import datetime
from collections import Counter


db = sqlite3.connect('events.db')
cur = db.cursor()

# Создание таблицы Events, если она еще не существует
cur.execute('''
CREATE TABLE IF NOT EXISTS Events (
id INTEGER PRIMARY KEY AUTOINCREMENT,
date TEXT NOT NULL,
name TEXT NOT NULL
)
''')
db.commit()

# Создание таблицы Participants, если она еще не существует
cur.execute('''
CREATE TABLE IF NOT EXISTS Participants (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL
)
''')
db.commit()

# Таблица связи участников с событиями
cur.execute('''
CREATE TABLE IF NOT EXISTS EventParticipants (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name_id INTEGER NOT NULL,
event_id INTEGER NOT NULL,
FOREIGN KEY (name_id) REFERENCES Participants(id),
FOREIGN KEY (event_id) REFERENCES Events(id)
)
''')
db.commit()

# Интерфейс записи в таблицы
insertEvents = """INSERT INTO Events (date, name) VALUES (?,?)"""
insertParticipants = "INSERT OR IGNORE INTO Participants (name) VALUES(?)"
insertCons = "INSERT INTO EventParticipants (name_id, event_id) VALUES(?,?)"
# Обработчик добавления событий
def add_func(args):
    """
    Добавляет новое событие в базу данных.
    
    Args:
    args (list): Список аргументов [дата, название, участники...]
    """
    if len(args) < 2:
        print("Ошибка: Необходимо указать дату и название события.")
        return

    date, name, *participants = args

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Ошибка: Неверный формат даты. Используйте YYYY-MM-DD.")
        return

    try:
        cur.execute(insertEvents, (date, name))
        event_id = cur.lastrowid
        db.commit()

        for participant in participants:
            cur.execute(insertParticipants, (participant,))
            cur.execute("SELECT id FROM Participants WHERE name = ?", (participant,))
            participant_id = cur.fetchone()[0]
            cur.execute(insertCons, (participant_id, event_id))
        db.commit()

        print(f"Событие '{name}' на дату {date} успешно добавлено.")
    except sqlite3.IntegrityError as e:
        print(f"Ошибка при добавлении события: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


# Обработчик добавления событий
def add_func(args):
    """
    Добавляет новое событие в базу данных.
    
    Args:
    args (list): Список аргументов [дата, название, участники...]
    """
    if len(args) < 2:
        print("Ошибка: Необходимо указать дату и название события.")
        return

    date, name, *participants = args

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Ошибка: Неверный формат даты. Используйте YYYY-MM-DD.")
        return

    try:
        cur.execute(insertEvents, (date, name))
        event_id = cur.lastrowid
        db.commit()

        for participant in participants:
            cur.execute(insertParticipants, (participant,))
            cur.execute("SELECT id FROM Participants WHERE name = ?", (participant,))
            participant_id = cur.fetchone()[0]
            cur.execute(insertCons, (participant_id, event_id))
        db.commit()

        print(f"Событие '{name}' на дату {date} успешно добавлено.")
    except sqlite3.IntegrityError as e:
        print(f"Ошибка при добавлении события: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Система поиска
def search_func(keyword=None, date=None):
    """
    Выполняет поиск событий по ключевому слову и/или дате.
    
    Args:
    keyword (str, optional): Ключевое слово для поиска в названии события или имени участника.
    date (str, optional): Дата для поиска событий.
    """
    query = """
    SELECT e.date, e.name, GROUP_CONCAT(p.name, ', ') as participants
    FROM Events e
    LEFT JOIN EventParticipants ep ON e.id = ep.event_id
    LEFT JOIN Participants p ON ep.name_id = p.id
    """
    conditions = []
    params = []

    if keyword:
        conditions.append("(e.name LIKE ? OR p.name LIKE ?)")
        params.extend([f"%{keyword}%", f"%{keyword}%"])
    if date:
        conditions.append("e.date LIKE ?")
        params.append(f"{date}%")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " GROUP BY e.id ORDER BY e.date"

    cur.execute(query, params)
    results = cur.fetchall()

    if not results:
        print("Ничего не найдено.")
    else:
        for date, name, participants in results:
            print(f"Дата: {date}, Событие: {name}, Участники: {participants or 'нет'}")

def stats_func():
    """
    Выводит статистику по событиям и участникам.
    """
    # ... (stats_func code remains unchanged)

def help_func():
    """
    Выводит справку по использованию программы.
    """
    print("Использование программы:")
    print("  --add <дата> <название> [участники...] : Добавить новое событие")
    print("  --search [ключевое_слово] [дата] : Поиск событий")
    print("  --stats : Показать статистику")
    print("  --help : Показать эту справку")
    print("\nПримеры:")
    print("  python test.py --add 2023-05-15 'День рождения' Иван Мария")
    print("  python test.py --search 'День рождения'")
    print("  python test.py --search 2023-05")
    print("  python test.py --search 'День рождения' 2023-05")
    print("  python test.py --stats")

# Получение аргументов из терминала
parser = argparse.ArgumentParser(description="Управление событиями и участниками", add_help=False)
parser.add_argument('--add', nargs='+', help="Добавить событие: <дата> <название> [участники...]")
parser.add_argument('--search', nargs='*', help="Поиск по ключевому слову и/или дате ВНИМАНИЕ!!!"
" При вводе в порядке Дата Событие Время работает корректно."
" Просим вас пользоваться только данным порядком записи иначе вы не сможете получить результат поиска")
parser.add_argument('--stats', action='store_true', help="Показать статистику")
parser.add_argument('-h', '--help', action='store_true', help="Показать справку")
res = parser.parse_args()

if res.add:
    add_func(res.add)
elif res.search is not None:
    if len(res.search) == 0:
        search_func()
    elif len(res.search) == 1:
        # Проверяем, является ли единственный аргумент датой или ключевым словом
        if res.search[0].replace('-', '').isdigit():
            search_func(date=res.search[0])
        else:
            search_func(keyword=res.search[0])
    else:
        # Определяем, какой аргумент является датой, а какой ключевым словом
        if res.search[0].replace('-', '').isdigit():
            search_func(date=res.search[0], keyword=res.search[1])
        else:
            search_func(keyword=res.search[0], date=res.search[1])
elif res.stats:
    stats_func()
elif res.help:
    parser.print_help()
else:
    parser.print_help()