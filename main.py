import tkinter as tk
from tkinter import ttk

from db import DB


class MainWindow:
    def __init__(self, root, db: DB):
        self.db = db
        self.root = root
        self.root.title('Управление сотрудниками')

        button_frame = tk.Frame(self.root)
        button_frame.pack()

        # элементы главного окна приложения

        self.add_button = tk.Button(button_frame, text='Добавить сотрудника', command=self.open_add_window)
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.edit_button = tk.Button(button_frame, text='Изменить сотрудника', command=self.open_edit_window)
        self.edit_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_button = tk.Button(button_frame, text='Удалить сотрудника', command=self.delete_employee)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.search_button = tk.Button(button_frame, text='Поиск сотрудника', command=self.open_search_window)
        self.search_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.update_button = tk.Button(button_frame, text='Обновить', command=self.update_treeview)
        self.update_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.tree = ttk.Treeview(self.root, columns=('full_name', 'phone_number', 'email', 'salary'))
        self.tree.heading('#0', text='ID')
        self.tree.heading('full_name', text='ФИО')
        self.tree.heading('phone_number', text='Номер телефона')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('salary', text='Зарплата')

        self.update_treeview()

    def update_treeview(self, employees: list | None = None):
        # обновление списка сотрудников
        for record in self.tree.get_children():
            self.tree.delete(record)
        
        if employees is None:
            employees = self.db.get()

        for employee in employees:
            self.tree.insert('', 'end', text=employee[0], values=employee[1:])
        
        self.tree.pack()

    def open_add_window(self):
        # открытие окна добавления сотрудника
        AddEmployeeWindow(self)

    def open_edit_window(self):
        # открытие окна редактирования сотрудника
        if self.tree.selection():
            EditEmployeeWindow(self)

    def delete_employee(self):
        # логика удаления сотрудника
        if selected_item := self.tree.selection():
            employee_id = self.tree.item(selected_item)['text']
            self.db.delete(employee_id)
            self.update_treeview()

    def open_search_window(self):
        SearchEmployeeWindow(self)

class AddEmployeeWindow:
    def __init__(self, app: MainWindow):
        self.app = app
        self.db = app.db
        self.root = tk.Toplevel(app.root)
        self.root.title('Добавить сотрудника')

        # элементы окна добавления сотрудника
        self.full_name_label = tk.Label(self.root, text='ФИО')
        self.full_name_label.pack()

        self.full_name_entry = tk.Entry(self.root)
        self.full_name_entry.pack()

        self.phone_number_label = tk.Label(self.root, text='Номер телефона')
        self.phone_number_label.pack()

        self.phone_number_entry = tk.Entry(self.root)
        self.phone_number_entry.pack()

        self.email_label = tk.Label(self.root, text='E-mail')
        self.email_label.pack()

        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack()

        self.salary_label = tk.Label(self.root, text='Зарплата')
        self.salary_label.pack()

        self.salary_entry = tk.Entry(self.root)
        self.salary_entry.pack()

        self.submit_button = tk.Button(self.root, text='Добавить', command=self.add_employee)
        self.submit_button.pack()

    def add_employee(self):
        # Логика добавления сотрудника
        full_name = self.full_name_entry.get()
        phone_number = self.phone_number_entry.get()
        email = self.email_entry.get()
        salary = self.salary_entry.get()
        self.db.add(full_name, phone_number, email, salary)
        app.update_treeview()

class EditEmployeeWindow:
    def __init__(self, app: MainWindow):
        self.app = app
        self.db = app.db
        self.root = tk.Toplevel(app.root)
        self.root.title('Изменить сотрудника')
        # элементы окна редактирования сотрудника
        selected_element = self.app.tree.item(self.app.tree.selection())

        self.employee_id = selected_element['text']

        selected_employee = selected_element['values']

        self.name_label = tk.Label(self.root, text='ФИО')
        self.name_label.pack()

        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()
        self.name_entry.insert(0, selected_employee[0])

        self.phone_number_label = tk.Label(self.root, text='Номер телефона')
        self.phone_number_label.pack()

        self.phone_number_entry = tk.Entry(self.root)
        self.phone_number_entry.pack()
        self.phone_number_entry.insert(0, selected_employee[1])

        self.email_label = tk.Label(self.root, text='E-mail')
        self.email_label.pack()

        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack()
        self.email_entry.insert(0, selected_employee[2])

        self.salary_label = tk.Label(self.root, text='Зарплата')
        self.salary_label.pack()

        self.salary_entry = tk.Entry(self.root)
        self.salary_entry.pack()
        self.salary_entry.insert(0, selected_employee[3])

        self.submit_button = tk.Button(self.root, text='Сохранить', command=self.save_employee)
        self.submit_button.pack()

    def save_employee(self):
        # Логика сохранения изменений сотрудника
        id = self.employee_id
        name = self.name_entry.get()
        phone_number = self.phone_number_entry.get()
        email = self.email_entry.get()
        salary = self.salary_entry.get()
        self.db.update(id, name, phone_number, email, salary)
        self.app.update_treeview()

class SearchEmployeeWindow:
    def __init__(self, app: MainWindow):
        self.app = app
        self.db = app.db
        self.root = tk.Toplevel(app.root)
        self.root.title('Поиск сотрудника')

        # Элементы интерфейса для поиска сотрудника
        self.search_label = tk.Label(self.root, text='Поиск по имени:')
        self.search_label.pack()

        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack()

        self.search_button = tk.Button(self.root, text='Найти', command=self.search_employee)
        self.search_button.pack()

    def search_employee(self):
        # Логика поиска сотрудника
        search_query = self.search_entry.get()
        result = self.db.search(search_query)
        self.app.update_treeview(result)



if __name__ == '__main__':
    # инициализация класса бд
    db = DB()
    # инициализация класса tkinter
    root = tk.Tk()
    # инициализация класса главного окна
    app = MainWindow(root, db)
    # запуск работы tkinter
    root.mainloop()
