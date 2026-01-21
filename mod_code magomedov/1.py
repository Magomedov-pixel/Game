import json
import os

class Employee:
    def __init__(self, id, name, position, department, salary, phone, email):
        self.id = id
        self.name = name
        self.position = position
        self.department = department
        self.salary = salary
        self.phone = phone
        self.email = email

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'position': self.position,  # Исправлено: было 'positio1n'
            'department': self.department,
            'salary': self.salary,
            'phone': self.phone,
            'email': self.email
        }

class InformationSystem:
    def __init__(self, file_name='employees.json'):
        self.file_name = file_name
        self.employees = []
        self.load_data()

    def load_data(self):
        if os.path.exists(self.file_name):
            try:
                with open(self.file_name, 'r') as file:
                    data = json.load(file)
                    self.employees = [Employee(**item) for item in data]
            except (json.JSONDecodeError, Exception) as e:
                print(f"Ошибка загрузки данных: {e}")
                self.employees = []

    def save_data(self):
        try:
            with open(self.file_name, 'w') as file:
                json.dump([emp.to_dict() for emp in self.employees], file, indent=4)
        except Exception as e:
            print(f"Ошибка сохранения данных: {e}")

    def add_employee(self, employee):
        # Проверка на уникальность ID
        if self.get_employee(employee.id):
            print(f"Сотрудник с ID {employee.id} уже существует!")
            return False
        self.employees.append(employee)
        self.save_data()
        return True

    def get_employee(self, id):
        for emp in self.employees:
            if emp.id == id:
                return emp
        return None

    def update_employee(self, id, new_data):
        employee = self.get_employee(id)
        if employee:
            for key, value in new_data.items():
                setattr(employee, key, value)
            self.save_data()
            return True
        return False

    def delete_employee(self, id):
        employee = self.get_employee(id)
        if employee:
            self.employees.remove(employee)
            self.save_data()
            return True
        return False

    def list_employees(self):
        return self.employees

    def search_employees(self, **kwargs):
        results = []
        for emp in self.employees:
            match = True
            for key, value in kwargs.items():
                if value and getattr(emp, key, None) != value:
                    match = False
                    break
            if match:
                results.append(emp)
        return results

def main():
    system = InformationSystem()
    
    while True:
        print("\nИнформационная система сотрудников")
        print("1. Добавить сотрудника")
        print("2. Просмотреть всех сотрудников")
        print("3. Найти сотрудника")
        print("4. Обновить данные сотрудника")
        print("5. Удалить сотрудника")
        print("6. Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            print("\nДобавление нового сотрудника")
            id = input("ID: ")
            
            # Проверка на существующий ID
            if system.get_employee(id):
                print("Сотрудник с таким ID уже существует!")
                continue
                
            name = input("Имя: ")
            position = input("Должность: ")
            department = input("Отдел: ")
            
            # Обработка ошибок ввода зарплаты
            try:
                salary = float(input("Зарплата: "))
            except ValueError:
                print("Ошибка: введите числовое значение для зарплаты!")
                continue
                
            phone = input("Телефон: ")
            email = input("Электронная почта: ")
            
            employee = Employee(id, name, position, department, salary, phone, email)
            if system.add_employee(employee):
                print("Сотрудник успешно добавлен!")
            
        elif choice == '2':
            print("\nСписок всех сотрудников:")
            employees = system.list_employees()
            if employees:
                for emp in employees:
                    print(f"ID: {emp.id}, Имя: {emp.name}, Должность: {emp.position}, Отдел: {emp.department}, Зарплата: {emp.salary}, Телефон: {emp.phone}, Электронная почта: {emp.email}")
            else:
                print("Нет сотрудников в системе.")
                
        elif choice == '3':
            print("\nПоиск сотрудника")
            print("Введите критерии поиска (оставьте поле пустым, если не важно)")
            id = input("ID: ") or None
            name = input("Имя: ") or None
            department = input("Отдел: ") or None
            
            search_params = {}
            if id: search_params['id'] = id
            if name: search_params['name'] = name
            if department: search_params['department'] = department
            
            results = system.search_employees(**search_params)
            if results:
                print("\nРезультаты поиска:")
                for emp in results:
                    print(f"ID: {emp.id}, Имя: {emp.name}, Должность: {emp.position}, Отдел: {emp.department}, Зарплата: {emp.salary}, Телефон: {emp.phone}, Электронная почта: {emp.email}")
            else:
                print("Сотрудники не найдены.")
                
        elif choice == '4':
            print("\nОбновление данных сотрудника")
            id = input("Введите ID сотрудника для обновления: ")
            employee = system.get_employee(id)
            if employee:
                print("Текущие данные:")
                print(f"1. Имя: {employee.name}")
                print(f"2. Должность: {employee.position}")
                print(f"3. Отдел: {employee.department}")
                print(f"4. Зарплата: {employee.salary}")
                print(f"5. Телефон: {employee.phone}")
                print(f"6. Email: {employee.email}")  # Исправлено: было "Зарплата" вместо "Email"
                
                fields = ['name', 'position', 'department', 'salary', 'phone', 'email']
                updates = {}
                field_choice = input("Введите номер поля для изменения (или 0 для завершения): ")
                while field_choice != '0':
                    if field_choice in ['1', '2', '3', '4', '5', '6']:
                        field = fields[int(field_choice)-1]
                        new_value = input(f"Новое значение для {field}: ")
                        if field == 'salary':
                            try:
                                new_value = float(new_value)
                            except ValueError:
                                print("Ошибка: введите числовое значение для зарплаты!")
                                continue
                        updates[field] = new_value
                    else:
                        print("Неверный номер поля!")
                    field_choice = input("Введите номер следующего поля (или 0 для завершения): ")
                
                if updates:
                    system.update_employee(id, updates)
                    print("Данные успешно обновлены!")
                else:
                    print("Изменения не внесены.")
            else:
                print("Сотрудник с таким ID не найден.")
                
        elif choice == '5':
            print("\nУдаление сотрудника")
            id = input("Введите ID сотрудника для удаления: ")
            if system.delete_employee(id):
                print("Сотрудник успешно удален!")
            else:
                print("Сотрудник с таким ID не найден.")
                
        elif choice == '6':
            print("Выход из системы...")
            break
            
        else:
            print("Неверный ввод. Пожалуйста, выберите действие от 1 до 6.")

if __name__ == "__main__":
    main()