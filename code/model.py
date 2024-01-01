from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = 'User'

    UserID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(64), nullable=False)
    Age = Column(Integer, nullable=False)
    Email = Column(String(64), nullable=False)
    resumes = relationship('Resume', back_populates='owner')
    vacancies = relationship('Vacancy', back_populates='publisher')

class Resume(Base):
    __tablename__ = 'Resume'

    ResumeID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(64), nullable=False)
    File_Link = Column(Text, nullable=False)
    OwnerID = Column(Integer, ForeignKey('User.UserID', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    owner = relationship('User', back_populates='resumes')

class Vacancy(Base):
    __tablename__ = 'Vacancy'

    VacancyID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(64), nullable=False)
    Description = Column(String(4096))
    Creation_Date = Column(DateTime(timezone=False), server_default=func.now())
    PublisherID = Column(Integer, ForeignKey('User.UserID', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    publisher = relationship('User', back_populates='vacancies')

class ResumeVacancy(Base):
    __tablename__ = 'ResumeVacancy'

    ResumeID = Column(Integer, ForeignKey('Resume.ResumeID', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    VacancyID = Column(Integer, ForeignKey('Vacancy.VacancyID', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    resume = relationship('Resume')
    vacancy = relationship('Vacancy')

engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class Model:
    def create_tables(self):
        Base.metadata.create_all(engine)

    def add_user(self, name, age, email):
        try:
            user = User(Name=name, Age=age, Email=email)
            session.add(user)
            session.commit()
        except Exception as e:
            session.rollback()
            return f"Error: {e}"
        return "User added successfully!"

    def add_resume(self, name, file_link, owner_id):
        try:
            resume = Resume(Name=name, File_Link=file_link, OwnerID=owner_id)
            session.add(resume)
            session.commit()
        except Exception as e:
            session.rollback()
            return f"Error: {e}"
        return "Resume added successfully!"

    def add_vacancy(self, name, description, date, publisher_id):
        try:
            vacancy = Vacancy(Name=name, Description=description, Creation_Date=date, PublisherID=publisher_id)
            session.add(vacancy)
            session.commit()
        except Exception as e:
            session.rollback()
            return f"Error: {e}"
        return "Vacancy added successfully!"

    def add_resvac(self, resume_id, vacancy_id):
        try:
            resvac = ResumeVacancy(ResumeID=resume_id, VacancyID=vacancy_id)
            session.add(resvac)
            session.commit()
        except Exception as e:
            session.rollback()
            return f"Error: {e}"
        return "Resume/Vacancy relation added successfully!"

    def get_table(self, table_name):
        model_classes = {
            'User': User,
            'Resume': Resume,
            'Vacancy': Vacancy,
            'ResumeVacancy': ResumeVacancy,
        }

        if table_name in model_classes:
            query_result = session.query(model_classes[table_name]).all()
        else:
            return None

        data = []
        if table_name == 'User':
            for row in query_result:
                data.append((row.UserID, row.Name, row.Age, row.Email))
        elif table_name == 'Resume':
            for row in query_result:
                data.append((row.ResumeID, row.Name, row.File_Link, row.OwnerID))
        elif table_name == 'Vacancy':
            for row in query_result:
                data.append((row.VacancyID, row.Name, row.Description, row.Creation_Date, row.PublisherID))
        elif table_name == 'ResumeVacancy':
            for row in query_result:
                data.append((row.ResumeID, row.VacancyID))
        return data

    def update_user(self, id, name, age, email):
        user = session.query(User).get(id)
        user.Name = name
        user.Age = age
        user.Email = email
        session.commit()

    def update_resume(self, id, name, file_link, owner_id):
        resume = session.query(Resume).get(id)
        resume.Name = name
        resume.File_Link = file_link
        resume.OwnerID = owner_id
        session.commit()

    def update_vacancy(self, id, name, description, date, publisher_id):
        vacancy = session.query(Vacancy).get(id)
        vacancy.Name = name
        vacancy.Description = description
        vacancy.Creation_Date = date
        vacancy.PublisherID = publisher_id
        session.commit()

    def delete(self, table_name, id):
        session.query(eval(table_name)).filter_by(**{f"{table_name}ID": id}).delete()
        session.commit()
