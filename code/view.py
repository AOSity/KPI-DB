from tabulate import tabulate

#class View:
#    def getView(self, data, headers):
#        return tabulate(data, headers, tablefmt="pretty", maxcolwidths=[50,50,50,50,50])
    
class View:
    def show_user(self, data):
        try:
            print(tabulate(data, ["ID", "Name", "Age", "Email"], tablefmt="pretty", maxcolwidths=[50,50,50,50]))
        except IndexError:
            print('Table "User" is empty')

    def show_resume(self, data):
        try:
            print(tabulate(data, ["ID", "Name", "Link", "OwnerID"], tablefmt="pretty", maxcolwidths=[50,50,50,50]))
        except IndexError:
            print('Table "Resume" is empty')
    def show_vacancy(self, data):
        try:
            print(tabulate(data, ["ID", "Name", "Description", "Date", "PublisherID"], tablefmt="pretty", maxcolwidths=[50,50,50,50,50]))
        except IndexError:
            print('Table "Vacancy" is empty')

    def show_resvac(self, data):
        try:
            print(tabulate(data, ["ResumeID", "VacancyID"], tablefmt="pretty", maxcolwidths=[50,50]))
        except IndexError:
            print('Table "Resume / Vacancy" is empty')

    def get_user_input(self):
        name = input("Enter user name: ")
        age = input("Enter user age: ")
        email = input("Enter user email: ")
        return name, age, email
    
    def get_resume_input(self):
        name = input("Enter resume name: ")
        file_link = input("Enter resume link: ")
        owner_id = input("Enter owner ID: ")
        return name, file_link, owner_id
    
    def get_vacancy_input(self):
        name = input("Enter vacancy name: ")
        description = input("Enter vacancy description: ")
        date = input("Enter vacancy date: ")
        publisher_id = input("Enter publisher ID: ")
        return name, description, date, publisher_id
    
    def get_resvac_input(self):
        resume_id = input("Enter resume ID: ")
        vacancy_id = input("Enter vacancy ID: ")
        return resume_id, vacancy_id

    def get_id(self):
        return int(input("Enter ID: "))

    def show_message(self, message):
        print(message)