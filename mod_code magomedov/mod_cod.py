import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTableWidget, QTableWidgetItem, QPushButton, QDialog, QLabel,
                             QLineEdit, QMessageBox, QFormLayout, QDialogButtonBox)
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
            'position': self.position, 
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

class EmployeeDialog(QDialog):
    def __init__(self, parent=None, employee=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить сотрудника" if employee is None else "Обновить сотрудника")
        self.employee = employee
        self.init_ui()
    def init_ui(self):
        layout = QFormLayout(self)
        self.id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.position_input = QLineEdit()
        self.department_input = QLineEdit()
        self.salary_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        layout.addRow("ID:", self.id_input)
        layout.addRow("Имя:", self.name_input)
        layout.addRow("Должность:", self.position_input)
        layout.addRow("Отдел:", self.department_input)
        layout.addRow("Зарплата:", self.salary_input)
        layout.addRow("Телефон:", self.phone_input)
        layout.addRow("Email:", self.email_input)
        if self.employee:
            self.id_input.setText(self.employee.id)
            self.id_input.setEnabled(False) 
            self.name_input.setText(self.employee.name)
            self.position_input.setText(self.employee.position)
            self.department_input.setText(self.employee.department)
            self.salary_input.setText(str(self.employee.salary))
            self.phone_input.setText(self.employee.phone)
            self.email_input.setText(self.employee.email)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    def get_data(self):
        data = {
            'id': self.id_input.text(),
            'name': self.name_input.text(),
            'position': self.position_input.text(),
            'department': self.department_input.text(),
            'phone': self.phone_input.text(),
            'email': self.email_input.text()
        }
        try:
            data['salary'] = float(self.salary_input.text())
        except ValueError:
            data['salary'] = 0.0
        return data
class SearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Поиск сотрудника")
        self.init_ui()
    def init_ui(self):
        layout = QFormLayout(self)
        self.id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.department_input = QLineEdit()
        layout.addRow("ID:", self.id_input)
        layout.addRow("Имя:", self.name_input)
        layout.addRow("Отдел:", self.department_input)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    def get_search_params(self):
        params = {}
        if self.id_input.text().strip():
            params['id'] = self.id_input.text().strip()
        if self.name_input.text().strip():
            params['name'] = self.name_input.text().strip()
        if self.department_input.text().strip():
            params['department'] = self.department_input.text().strip()
        return params
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.system = InformationSystem()
        self.setWindowTitle("Информационная система сотрудников")
        self.resize(800, 600)
        self.init_ui()
        self.load_employees()
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels(["ID", "Имя", "Должность", "Отдел", "Зарплата", "Телефон", "Email"])
        layout.addWidget(self.table)
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Добавить")
        self.edit_btn = QPushButton("Редактировать")
        self.delete_btn = QPushButton("Удалить")
        self.search_btn = QPushButton("Поиск")
        self.refresh_btn = QPushButton("Обновить")
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.search_btn)
        btn_layout.addWidget(self.refresh_btn)
        layout.addLayout(btn_layout)
        self.add_btn.clicked.connect(self.add_employee)
        self.edit_btn.clicked.connect(self.edit_employee)
        self.delete_btn.clicked.connect(self.delete_employee)
        self.search_btn.clicked.connect(self.search_employee)
        self.refresh_btn.clicked.connect(self.load_employees)
    def load_employees(self):
        employees = self.system.list_employees()
        self.table.setRowCount(0)
        for emp in employees:
            row_pos = self.table.rowCount()
            self.table.insertRow(row_pos)
            self.table.setItem(row_pos, 0, QTableWidgetItem(emp.id))
            self.table.setItem(row_pos, 1, QTableWidgetItem(emp.name))
            self.table.setItem(row_pos, 2, QTableWidgetItem(emp.position))
            self.table.setItem(row_pos, 3, QTableWidgetItem(emp.department))
            self.table.setItem(row_pos, 4, QTableWidgetItem(str(emp.salary)))
            self.table.setItem(row_pos, 5, QTableWidgetItem(emp.phone))
            self.table.setItem(row_pos, 6, QTableWidgetItem(emp.email))
    def add_employee(self):
        dialog = EmployeeDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            if self.system.get_employee(data['id']):
                QMessageBox.warning(self, "Ошибка", "Сотрудник с таким ID уже существует!")
                return
            employee = Employee(**data)
            if self.system.add_employee(employee):
                QMessageBox.information(self, "Успех", "Сотрудник успешно добавлен!")
                self.load_employees()
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось добавить сотрудника!")
    def edit_employee(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите сотрудника для редактирования!")
            return
        emp_id = self.table.item(selected, 0).text()
        employee = self.system.get_employee(emp_id)
        if not employee:
            QMessageBox.warning(self, "Ошибка", "Сотрудник не найден!")
            return
        dialog = EmployeeDialog(self, employee)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            if self.system.update_employee(emp_id, data):
                QMessageBox.information(self, "Успех", "Данные успешно обновлены!")
                self.load_employees()
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось обновить данные сотрудника!")
    def delete_employee(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите сотрудника для удаления!")
            return
        emp_id = self.table.item(selected, 0).text()
        reply = QMessageBox.question(self, "Подтверждение", f"Вы действительно хотите удалить сотрудника с ID {emp_id}?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.system.delete_employee(emp_id):
                QMessageBox.information(self, "Успех", "Сотрудник успешно удален!")
                self.load_employees()
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось удалить сотрудника!")
    def search_employee(self):
        dialog = SearchDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            params = dialog.get_search_params()
            results = self.system.search_employees(**params)
            if results:
                self.table.setRowCount(0)
                for emp in results:
                    row_pos = self.table.rowCount()
                    self.table.insertRow(row_pos)
                    self.table.setItem(row_pos, 0, QTableWidgetItem(emp.id))
                    self.table.setItem(row_pos, 1, QTableWidgetItem(emp.name))
                    self.table.setItem(row_pos, 2, QTableWidgetItem(emp.position))
                    self.table.setItem(row_pos, 3, QTableWidgetItem(emp.department))
                    self.table.setItem(row_pos, 4, QTableWidgetItem(str(emp.salary)))
                    self.table.setItem(row_pos, 5, QTableWidgetItem(emp.phone))
                    self.table.setItem(row_pos, 6, QTableWidgetItem(emp.email))
            else:
                QMessageBox.information(self, "Результаты", "Сотрудники не найдены.")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())