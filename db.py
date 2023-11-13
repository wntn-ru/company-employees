import sqlite3

# запрос для создания таблицы сотрудников
CREATE_TABLE_QUERY = '''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        full_name TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        email TEXT NOT NULL,
        salary REAL
    )
'''

class DB:
    def __init__(self, file_name: str = 'db.sqlite'):
        # подключение к базе данных
        self.connection = sqlite3.connect(database=file_name)
        self.cursor = self.connection.cursor()
        # создание таблицы, если ее нет
        self.cursor.execute(CREATE_TABLE_QUERY)
        self.connection.commit()

    def add(self, full_name: str, phone_number: str, email: str, salary: str):
        # функция добавления сотрудника в базу данных
        data = (full_name, phone_number, email, salary)
        self.cursor.execute('INSERT INTO employees (full_name, phone_number, email, salary) VALUES (?, ?, ?, ?)', data)
        self.connection.commit()

    def delete(self, id: int):
        # функция удаления сотрудника из базы данных
        self.cursor.execute('DELETE FROM employees WHERE id = ?', (id, ))
        self.connection.commit()

    def get(self) -> list:
        # функция получения всех сотрудников из базы данных
        self.cursor.execute('SELECT * FROM employees WHERE 1')
        result = self.cursor.fetchall()
        return result
    
    def update(self, id: int, full_name: str, phone_number: str, email: str, salary: str):
        # функция обновления сотрудника в базе данных
        self.cursor.execute(
            'UPDATE employees SET full_name = ?, phone_number = ?, email = ?, salary = ? WHERE id = ?', 
            (full_name, phone_number, email, salary, id)
        )
        self.connection.commit()
    
    def search(self, full_name: str) -> list | None:
        # функция поиска сотрудников
        self.cursor.execute('SELECT * FROM employees WHERE full_name = ?', (full_name, ))
        result = self.cursor.fetchall()
        return result