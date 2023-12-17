import psycopg2
from db_setup import db_setup_script

class Model:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='postgres',
            host='localhost',
            port=5432
        )
        self.create_tables()

    def create_tables(self):
        try:
            c = self.conn.cursor()
            c.execute(db_setup_script)
            self.conn.commit()
        except Exception:
            self.conn.rollback()

    def add_user(self, name, age, email):
        try:
            c = self.conn.cursor()
            c.execute('INSERT INTO "User" ("Name", "Age", "Email") VALUES (%s, %s, %s)', (name, age, email))
            self.conn.commit()
        except psycopg2.errors.InvalidTextRepresentation:
            self.conn.rollback()
            return "Input error!"
        except psycopg2.errors.ForeignKeyViolation:
            self.conn.rollback()
            return "Foreign key violation!"
        return "User added successfully!"
    
    def add_resume(self, name, file_link, owner_id):
        try:
            c = self.conn.cursor()
            c.execute('INSERT INTO "Resume" ("Name", "File Link", "OwnerID") VALUES (%s, %s, %s)', (name, file_link, owner_id))
            self.conn.commit()
        except psycopg2.errors.InvalidTextRepresentation:
            self.conn.rollback()
            return "Input error!"
        except psycopg2.errors.ForeignKeyViolation:
            self.conn.rollback()
            return "Foreign key violation!"
        return "Resume added successfully!"

    def add_vacancy(self, name, description, date, publisher_id):
        try:
            c = self.conn.cursor()
            c.execute('INSERT INTO "Vacancy" ("Name", "Description", "Creation Date", "PublisherID") VALUES (%s, %s, %s, %s)', 
                      (name, description, date, publisher_id))
            self.conn.commit()
        except psycopg2.errors.InvalidTextRepresentation:
            self.conn.rollback()
            return "Input error!"
        except psycopg2.errors.ForeignKeyViolation:
            self.conn.rollback()
            return "Foreign key violation!"
        return "Vacancy added successfully!"

    def add_resvac(self, resume_id, vacancy_id):
        try:
            c = self.conn.cursor()
            c.execute('INSERT INTO "Resume / Vacancy" ("ResumeID", "VacancyID") VALUES (%s, %s)', (resume_id, vacancy_id))
            self.conn.commit()
        except psycopg2.errors.InvalidTextRepresentation:
            self.conn.rollback()
            return "Input error!"
        except psycopg2.errors.ForeignKeyViolation:
            self.conn.rollback()
            return "Foreign key violation!"
        return "Resume/Vacancy relation added successfully!"

    def get_table(self, table_name):
        c = self.conn.cursor()
        c.execute(f'SELECT * FROM "{table_name}"')
        return c.fetchall()

    def update_user(self, id, name, age, email):
        c = self.conn.cursor()
        c.execute('UPDATE "User" SET "Name"=%s, "Age"=%s, "Email"=%s WHERE "UserID"=%s', (name, age, email, id))
        self.conn.commit()
    
    def update_resume(self, id, name, file_link, owner_id):
        c = self.conn.cursor()
        c.execute('UPDATE "Resume" SET "Name"=%s, "File Link"=%s, "OwnerID"=%s WHERE "ResumeID"=%s', (name, file_link, owner_id, id))
        self.conn.commit()

    def update_vacancy(self, id, name, description, date, publisher_id):
        c = self.conn.cursor()
        c.execute('UPDATE "Vacancy" SET "Name"=%s, "Description"=%s, "Creation Date"=%s, "PublisherID"=%s WHERE "VacancyID"=%s', 
                  (name, description, date, publisher_id, id))
        self.conn.commit()

    def delete(self, table_name, id):
        c = self.conn.cursor()
        c.execute(f'DELETE FROM "{table_name}" WHERE "{table_name}ID"={id}')
        self.conn.commit()

    def generate_user(self, number):
        c = self.conn.cursor()
        c.execute(f'''
                    INSERT INTO public."User" ("Name", "Age", "Email")
                    SELECT
                        substring(md5(random()::text), 1, 16),
                        trunc(random() * 70) + 1,
                        substring(md5(random()::text), 1, 16) || '@email.com'
                    FROM generate_series(1, {number});
                    ''')
        self.conn.commit()
        return f"{number} user generated successfully!"
    
    def generate_resume(self, number):
        try:
            c = self.conn.cursor()
            c.execute(f'''
                        INSERT INTO public."Resume" ("Name", "File Link", "OwnerID")
                        SELECT
                            substring(md5(random()::text), 1, 16),
                            'https://domain.com/files/' ||  substring(md5(random()::text), 1, 8) || '/resume.pdf',
                            (SELECT "UserID" FROM public."User" ORDER BY random() LIMIT 1 
	                         OFFSET (random()*generate_series)::int%(SELECT COUNT(*) FROM "User"))
                        FROM generate_series(1, {number});
                        ''')
            self.conn.commit()
        except psycopg2.errors.DivisionByZero:
            self.conn.rollback()
            return "Generation failed, no users to assign OwnerID"
        return f"{number} resume generated successfully!"

    def generate_vacancy(self, number):
        try:
            c = self.conn.cursor()
            c.execute(f'''
                        INSERT INTO public."Vacancy" ("Name", "Description", "Creation Date", "PublisherID")
                        SELECT
                            SUBSTRING(md5(random()::text), 1, 16),
                            SUBSTRING(md5(random()::text), 1, 128),
                            'now'::timestamp - random() * ('2023-12-31'::timestamp - '2022-01-01'::timestamp),
                            (SELECT "UserID" FROM public."User" ORDER BY random() LIMIT 1 
                             OFFSET (random()*generate_series)::int%(SELECT COUNT(*) FROM "User"))
                        FROM generate_series(1, {number});
                        ''')
            self.conn.commit()
        except psycopg2.errors.DivisionByZero:
            self.conn.rollback()
            return "Generation failed, no users to assign PublisherID"
        return f"{number} vacancy generated successfully!"
    
    def generate_resvac(self, number):
        try:
            c = self.conn.cursor()
            c.execute(f'''
                        INSERT INTO public."Resume / Vacancy" ("ResumeID", "VacancyID")
                        SELECT
                            (SELECT "ResumeID" FROM public."Resume" ORDER BY random() LIMIT 1 
                             OFFSET (random()*generate_series)::int%(SELECT COUNT(*) FROM "Resume")),
                            (SELECT "VacancyID" FROM public."Vacancy" ORDER BY random() LIMIT 1 
                             OFFSET (random()*generate_series)::int%(SELECT COUNT(*) FROM "Vacancy"))
                        FROM generate_series(1, {number});
                        ''')
            self.conn.commit()
        except psycopg2.errors.DivisionByZero:
            self.conn.rollback()
            return "Generation failed, no avaliable ResumeID and/or VacancyID"
        return f"{number} Resume/Vacancy relation generated successfully!"