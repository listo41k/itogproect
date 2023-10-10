import tkinter as tk
from tkinter import ttk 
import sqlite3

class Main(tk.Frame):
    def __init__(self, window):
        super().__init__(window)
        self.init_main()

    def init_main(self):
        global refresh
        toolbar = tk.Frame(bd=2, bg='gray') #Приборная строка
        toolbar.pack(side='top', fill='x')

        ##################################################################################################################
        # Таблица с записями из базы данных
        self.treeview = ttk.Treeview(self, columns=('id', 'full_name', 'email', 'phone_number', 'salary'), height=45, show='headings') 
        
        self.treeview.column('id', width=100, anchor='center')
        self.treeview.column('full_name', width=250, anchor='center')
        self.treeview.column('email', width=250, anchor='center')
        self.treeview.column('phone_number', width=150, anchor='center')
        self.treeview.column('salary', width=150, anchor='center')
        
        self.treeview.heading('id', text='id')
        self.treeview.heading('full_name', text='ФИО')
        self.treeview.heading('email', text='Email')
        self.treeview.heading('phone_number', text='Номер телефона')
        self.treeview.heading('salary', text='Зарплата')

        # Сначала добавляем в таблицу все записи из бд
        for staff in Staff().order(): 
            self.treeview.insert('', tk.END, values=staff)

        def refresh():
            self.treeview.delete(*self.treeview.get_children()) # Для начала удаляем все записи
            for staff in Staff().order(): # Берем все записи из бд
                self.treeview.insert('', tk.END, values=staff) # Потом вставляем, таким образом
                                                               # Удаленные, добавленные, измененные сотрудники будут видны 
        
        # Таблица с записями из базы данных
        ##################################################################################################################
        # Кнопки

        self.add_image = tk.PhotoImage(file='./img/add.png') # Картинка для кнопки
        # Кнопка для вызова окна добавления
        btn_call_add = tk.Button(toolbar, bd=0, bg='green', image=self.add_image,
                                    command=self.open_add, cursor='hand2')
        btn_call_add.pack(side='left')

        self.update_img = tk.PhotoImage(file='./img/update.png')
        btn_call_update = tk.Button(toolbar, bd=0, bg='green', image=self.update_img,
                                    command=self.open_update, cursor='hand2')
        btn_call_update.pack(side='left')

        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_call_search = tk.Button(toolbar, bd=0, bg='blue', image=self.search_img,
                                    command=self.open_search, cursor='hand2')
        btn_call_search.pack(side='right')

        self.refresh_img = tk.PhotoImage(file='./img/refresh.png')
        btn_call_refresh = tk.Button(toolbar, bd=0, bg='blue', image=self.refresh_img,
                                    command=refresh, cursor='hand2')
        btn_call_refresh.pack(side='right')

        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        btn_call_delete = tk.Button(toolbar, bd=0, bg='red', image=self.delete_img,
                                    command=self.open_delete, cursor='hand2')
        btn_call_delete.pack(side='top')

        # Кнопки
        ##################################################################################################################

        self.treeview.pack(side='left')

    ######################################################################################################################
    # Методы для открытия окон    
    def open_add(self):
        Add()

    def open_update(self):
        Update()

    def open_delete(self):
        Delete()

    def open_search(self):
        Search()
    
    ######################################################################################################################

# Класс диалогового окна для наследования другими классами 
class Child(tk.Toplevel):	
    def __init__(self):
        super().__init__()
        self.geometry('300x200')        
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        
    def init_child(self):
        self.geometry('300x200')        
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        


class Staff:
    def __init__(self):
        self.connection = sqlite3.connect(database='database.db')
        self.cursor = self.connection.cursor()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS staff (
                            id INTEGER PRIMARY KEY,
                            full_name TEXT,
                            email TEXT,
                            phone_number TEXT,
                            salary INTEGER
        )""")

    def insert(self, full_name, email, phone_number, salary):
        insert_query = "INSERT INTO staff (full_name, email, phone_number, salary) VALUES (?, ?, ?, ?)"
        self.cursor.execute(insert_query, (full_name, email, phone_number, salary))

        self.connection.commit()

    def delete(self, id):
        delete_query = "DELETE FROM staff WHERE id = (?)"
        self.cursor.execute(delete_query, (id,))

        self.connection.commit()

    def update(self, id, full_name='', email='', phone_number='', salary=''):
        update_query = "UPDATE staff SET "
        update_query += "full_name = ?, " if full_name != '' else ''
        update_query += "email = ?, " if email != '' else ''
        update_query += "phone_number = ?, " if phone_number != '' else ''
        update_query += "salary = ?, " if salary != '' else ''
        update_query += "WHERE id = ?"
        update_query = update_query.replace(', WHERE', ' WHERE')

        update_data = [full_name, email, phone_number, salary]
        if full_name == '':
            update_data.remove(full_name)
        if email == '':
            update_data.remove(email)
        if phone_number == '':
            update_data.remove(phone_number)
        if salary == '':
            update_data.remove(salary)

        update_data.append(int(id))

        self.cursor.execute(update_query, tuple(update_data))
        self.connection.commit()

    def search(self, full_name='', id=None):
        search_query = "SELECT * FROM staff WHERE"
        search_data = []

        if full_name != '':
            search_query += ' full_name=?'
            search_data.append(full_name)

        if id != '' and full_name != '':
            search_query += ', AND id=?'
            search_data.append(id)
        elif id!='':
            search_query += ' id=?'
            search_data.append(id)

        self.cursor.execute(search_query, tuple(search_data))
        self.connection.commit()

        staff_data = self.cursor.fetchall()

        return staff_data[0]
    
    def order(self):
        order_query = "SELECT * FROM staff ORDER BY id"
        self.cursor.execute(order_query)
        self.connection.commit()

        return self.cursor.fetchall()


# Добавление сотрудника
class Add(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_add()

    def init_add(self):
        global add_info, email_entry, salary_entry, phone_number_entry, full_name_entry
        self.configure(bg='#C0C0C0')
        self.title('Добавить')
        self.geometry('400x400')
        add_info = tk.Label(self, bg='#C0C0C0', text='Здесь вы можете добавить сотрудника') # Информация о запросе
        add_info.pack(pady=10, side='top')

        toolbar = tk.Frame(self, bd=10, bg='#C0C0C0')
        toolbar.pack(side='top', fill='x')

        # Виджеты и поля для ввода
        full_name_label = tk.Label(toolbar, text='ФИО:')
        full_name_label.pack(anchor='center')
        full_name_entry = tk.Entry(toolbar, cursor='hand2', width=40)
        full_name_entry.pack(anchor='center', pady=10)

        email_label = tk.Label(toolbar, text='Email:')
        email_label.pack(anchor='center')
        email_entry = tk.Entry(toolbar, cursor='hand2', width=40)
        email_entry.pack(anchor='center', pady=10)

        phone_number_label = tk.Label(toolbar, text='Номер телефона:')
        phone_number_label.pack(anchor='center')
        phone_number_entry = tk.Entry(toolbar, cursor='hand2', width=25)
        phone_number_entry.pack(anchor='center', pady=10)

        salary_label = tk.Label(toolbar, text='Зарплата:')
        salary_label.pack(anchor='center')
        salary_entry = tk.Entry(toolbar, cursor='hand2')
        salary_entry.pack(anchor='center', pady=10)
        # Виджеты и поля для ввода

        # Кнопка для добавления
        add_button = tk.Button(toolbar, command=self.add_staff, text='Добавить', cursor='hand2', bg='green')
        add_button.pack(anchor='center')
    
    # Метод для добавления
    def add_staff(self):
        # Берем значения из полей для воода
        full_name = full_name_entry.get()
        email = email_entry.get()
        phone_number = phone_number_entry.get()
        salary = int(salary_entry.get())

        # Обработка ошибок при выполнении запроса
        try:
            Staff().insert(full_name, email, phone_number, salary)
            add_info.configure(text='Сотрудник успешно добавлен!')
        except Exception as exception:
            add_info.configure(text='Произошла ошибка. Проверьте правильность заполнения полей')
# Добавление сотрудника

# Удаление сотрудника
class Delete(Child):
    def __init__(self):
        super().__init__()
        self.init_delete()

    def init_delete(self):
        global id_for_delete_entry, delete_info
        self.configure(bg='#C0C0C0')
        self.title('Удалить')
        self.geometry('400x400')
        delete_info = tk.Label(self, bg='#C0C0C0', text='Здесь вы можете удалить сотрудника')  # Информация о запросе
        delete_info.pack(pady=10, side='top')

        toolbar = tk.Frame(self, bd=10, bg='#C0C0C0')
        toolbar.pack(side='top', fill='x')
        
        # Виджеты и поля для ввода
        id_for_delete = tk.Label(toolbar, text='Введите id сотрудника для удаления:')
        id_for_delete.pack(anchor='center')
        id_for_delete_entry = tk.Entry(toolbar, cursor='hand2')
        id_for_delete_entry.pack(anchor='center', pady=10)
        # Виджеты и поля для ввода

        # Кнопка для удаления
        delete_button = tk.Button(toolbar, text='Удалить', bg='red', command=self.delete_staff, cursor='hand2')
        delete_button.pack(anchor='center')

    # Метод для удаления
    def delete_staff(self):
        # Берем значения из полей для ввода
        id = id_for_delete_entry.get()

        # Обработка ошибок при выполнении запроса
        try:
            Staff().delete(id=id)
            delete_info.configure(text='Сотрудник успешно удален')
        except Exception as exception:
            delete_info.configure(text='Произошла ошибка, проверьте правильность заполнения полей')
# Удаление сотрудника

# Изменения данных о сотруднике
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_update()

    def init_update(self):
        global new_email_entry, new_full_name_entry, new_phone_number_entry, new_salary_entry, id_for_update_entry, update_info
        self.configure(bg='#C0C0C0')
        self.title('Обновить')
        self.geometry('400x400')
        update_info = tk.Label(self, bg='#C0C0C0', text='Здесь вы можете обновить данные сотрудника') # Информация о запросе
        update_info.pack(pady=10, side='top')

        toolbar = tk.Frame(self, bd=10, bg='#C0C0C0')
        toolbar.pack(side='top', fill='x')

        # Виджеты и поля для ввода
        id_for_update_label = tk.Label(toolbar, text='Введите id сотрудника для изменения данных:')
        id_for_update_label.pack(anchor='center')
        id_for_update_entry = tk.Entry(toolbar, cursor='hand2')
        id_for_update_entry.pack(anchor='center', pady=10)

        new_full_name_label = tk.Label(toolbar, text='Новые ФИО:')
        new_full_name_label.pack(anchor='center')
        new_full_name_entry = tk.Entry(toolbar, cursor='hand2', width=40)
        new_full_name_entry.pack(anchor='center', pady=10)

        new_email_label = tk.Label(toolbar, text='Новый Email:')
        new_email_label.pack(anchor='center')
        new_email_entry = tk.Entry(toolbar, cursor='hand2', width=40)
        new_email_entry.pack(anchor='center', pady=10)

        new_phone_number_label = tk.Label(toolbar, text='Новый номер телефона:')
        new_phone_number_label.pack(anchor='center')
        new_phone_number_entry = tk.Entry(toolbar, cursor='hand2', width=25)
        new_phone_number_entry.pack(anchor='center', pady=10)

        new_salary_label = tk.Label(toolbar, text='Новая зарплата:')
        new_salary_label.pack(anchor='center')
        new_salary_entry = tk.Entry(toolbar, cursor='hand2')
        new_salary_entry.pack(anchor='center', pady=10)
        # Виджеты и поля для ввода

        # Кнопка для изменения
        update_button = tk.Button(toolbar, command=self.update_staff, text='Изменить', cursor='hand2', bg='green')
        update_button.pack(anchor='center')

    def update_staff(self):
        # Берем значения из полей для ввода
        id = id_for_update_entry.get()
        full_name = new_full_name_entry.get()
        email = new_email_entry.get()
        phone_number = new_phone_number_entry.get()
        salary = int(new_salary_entry.get())

        # Обработка ошибок при выполнении запроса
        try:
            Staff().update(id, full_name, email, phone_number, salary)
            update_info.configure(text='Данные успешно изменены!')
        except Exception as exception:
            update_info.configure(text='Произошла ошибка, проверьте правильность заполнения полей')
            print(exception)
# Изменения данных о сотруднике

class Search(Child):
    def __init__(self):
        super().__init__()
        self.init_search()

    def init_search(self):
        global id_search_entry, full_name_search_entry, toolbar, search_info
        self.configure(bg='#C0C0C0')
        self.title('Поиск')
        self.geometry('900x300')
        search_info = tk.Label(self, bg='#C0C0C0', text='Здесь вы можете найти данные о сотруднике')   # Информация о запросе
        search_info.pack(pady=10, side='top')

        toolbar = tk.Frame(self, bd=10, bg='#C0C0C0')
        toolbar.pack(side='top', fill='x')
        
        # Виджеты и поля для ввода
        id_search_label = tk.Label(toolbar, text='Введите id сотрудника для поиска:')
        id_search_label.pack(anchor='center')
        id_search_entry = tk.Entry(toolbar, cursor='hand2')
        id_search_entry.pack(anchor='center', pady=10)

        full_name_search_label = tk.Label(toolbar, text='Введите ФИО сотрудника для поиска:')
        full_name_search_label.pack(anchor='center')
        full_name_search_entry = tk.Entry(toolbar, cursor='hand2', width=40)
        full_name_search_entry.pack(anchor='center', pady=10)
        # Виджеты и поля для ввода

        # Кнопка для поиска
        search_button = tk.Button(toolbar, command=self.search_staff, text='Найти', cursor='hand2', bg='blue')
        search_button.pack(anchor='center')
    
    # Метод для поиска
    def search_staff(self):
        # Берем значения из полей для ввода
        id = id_search_entry.get()
        full_name = full_name_search_entry.get()
        
        # Данные о сотруднике
        staff_info = Staff().search(full_name, id)
        search_info.configure(text='Сотрудник успешно найден!')
        
        # Таблица с данными о сотруднике
        staff_table = ttk.Treeview(self, columns=('id', 'full_name', 'email', 'phone_number', 'salary'), height=45, show='headings') 

        # Добавляем столбцы
        staff_table.column('id', width=100, anchor='center')
        staff_table.column('full_name', width=250, anchor='center')
        staff_table.column('email', width=250, anchor='center')
        staff_table.column('phone_number', width=150, anchor='center')
        staff_table.column('salary', width=150, anchor='center')

        # Добавляем заголовки
        staff_table.heading('id', text='id')
        staff_table.heading('full_name', text='ФИО')
        staff_table.heading('email', text='Email')
        staff_table.heading('phone_number', text='Номер телефона')
        staff_table.heading('salary', text='Зарплата')

        # Добавляем данные о найденном сотруднике в таблицу для вывода
        staff_table.insert('', tk.END, values=staff_info)

        staff_table.pack(side='left')

if __name__ == '__main__':
    window = tk.Tk()
    window.geometry('900x450')
    app = Main(window)
    app.pack()
    window.title('Телефонная книга')
    tk.mainloop()