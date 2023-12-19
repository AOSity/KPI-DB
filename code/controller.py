from model import Model
from view import View

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def run(self):
        while True:
            choice = self.show_menu()
            if choice == '1':
                self.add()
            elif choice == '2':
                self.view_table()
            elif choice == '3':
                self.update()
            elif choice == '4':
                self.delete()
            elif choice == '5':
                self.generate()
            elif choice == '6':
                self.find()
            elif choice == '7':
                break

    def show_menu(self):
        self.view.show_message("\nMenu:")
        self.view.show_message("1. Add")
        self.view.show_message("2. View")
        self.view.show_message("3. Update")
        self.view.show_message("4. Delete")
        self.view.show_message("5. Generate")
        self.view.show_message("6. Find")
        self.view.show_message("7. Quit")
        return input("Enter your choice: ")

    def add(self):
        self.view.show_message("1. User")
        self.view.show_message("2. Resume")
        self.view.show_message("3. Vacancy")
        self.view.show_message("4. Resume / Vacancy")
        self.view.show_message("5. Cancel")
        choice = input("Enter your choice: ")
        if choice == '1':
            name, age, email = self.view.get_user_input()
            self.view.show_message(self.model.add_user(name, age, email))
        elif choice == '2':
            name, file_link, owner_id = self.view.get_resume_input()
            self.view.show_message(self.model.add_resume(name, file_link, owner_id))
        elif choice == '3':
            name, description, date, publisher_id = self.view.get_vacancy_input()
            self.view.show_message(self.model.add_vacancy(name, description, date, publisher_id))
        elif choice == '4':
            resume_id, vacancy_id = self.view.get_resvac_input()
            self.view.show_message(self.model.add_resvac(resume_id, vacancy_id))
        elif choice == '5':
            return

    def view_table(self):
        self.view.show_message("1. User")
        self.view.show_message("2. Resume")
        self.view.show_message("3. Vacancy")
        self.view.show_message("4. Resume / Vacancy")
        self.view.show_message("5. Cancel")
        choice = input("Enter your choice: ")
        if choice == '1':
            data = self.model.get_table("User")
            self.view.show_user(data)
        elif choice == '2':
            data = self.model.get_table("Resume")
            self.view.show_resume(data)
        elif choice == '3':
            data = self.model.get_table("Vacancy")
            self.view.show_vacancy(data)
        elif choice == '4':
            data = self.model.get_table("Resume / Vacancy")
            self.view.show_resvac(data)
        elif choice == '5':
            return
        return

    def update(self):
        self.view.show_message("1. User")
        self.view.show_message("2. Resume")
        self.view.show_message("3. Vacancy")
        self.view.show_message("4. Cancel")
        choice = input("Enter your choice: ")
        if choice == '1':
            id = self.view.get_id()
            name, age, email = self.view.get_user_input()
            self.model.update_user(id, name, age, email)
            self.view.show_message("User updated successfully!")
        elif choice == '2':
            id = self.view.get_id()
            name, file_link, owner_id = self.view.get_resume_input()
            self.model.update_resume(id, name, file_link, owner_id)
            self.view.show_message("Resume updated successfully!")
        elif choice == '3':
            id = self.view.get_id()
            name, description, date, publisher_id = self.view.get_vacancy_input()
            self.model.update_vacancy(id, name, description, date, publisher_id)
            self.view.show_message("Vacancy updated successfully!")
        elif choice == '4':
            return
        return

    def delete(self):
        self.view.show_message("1. User")
        self.view.show_message("2. Resume")
        self.view.show_message("3. Vacancy")
        self.view.show_message("4. Cancel")
        choice = input("Enter your choice: ")
        if choice == '1':
            id = self.view.get_id()
            self.model.delete("User",id)
            self.view.show_message("User deleted successfully!")
        elif choice == '2':
            id = self.view.get_id()
            self.model.delete("Resume",id)
            self.view.show_message("Resume deleted successfully!")
        elif choice == '3':
            id = self.view.get_id()
            self.model.delete("Vacancy",id)
            self.view.show_message("Vacancy deleted successfully!")
        elif choice == '4':
            return
        return
    
    def generate(self):
        self.view.show_message("1. User")
        self.view.show_message("2. Resume")
        self.view.show_message("3. Vacancy")
        self.view.show_message("4. Resume / Vacancy")
        self.view.show_message("5. Cancel")
        choice = input("Enter your choice: ")
        if choice == '1':
            number = input("Generated rows number: ")
            self.view.show_message(self.model.generate_user(number))
        elif choice == '2':
            number = input("Generated rows number: ")
            self.view.show_message(self.model.generate_resume(number))
        elif choice == '3':
            number = input("Generated rows number: ")
            self.view.show_message(self.model.generate_vacancy(number))
        elif choice == '4':
            number = input("Generated rows number: ")
            self.view.show_message(self.model.generate_resvac(number))
        elif choice == '5':
            return
        return

    def find(self):
        user_name = self.view.find_input("Enter user name (blank for any): ")
        min_age = self.view.find_input("Enter minimum age (blank for any): ")
        max_age = self.view.find_input("Enter maximum age (blank for any): ")
        resume_name = self.view.find_input("Enter resume name (blank for any): ")
        vacancy_name = self.view.find_input("Enter vacancy name (blank for any): ")
        min_creation_date = self.view.find_input("Enter minimum creation date (YYYY-MM-DD, blank for any): ")
        max_creation_date = self.view.find_input("Enter maximum creation date (YYYY-MM-DD, blank for any): ")
        self.view.show_found(self.model.find(user_name, min_age, max_age, resume_name, vacancy_name, min_creation_date, max_creation_date))