import pymysql

from model.project_class import Project


class DbFixture:
    def __init__(self, host_value, name_value, user_value, password_value):
        self.host = host_value
        self.name = name_value
        self.user = user_value
        self.password = password_value
        self.connection = pymysql.connect(host=host_value, database=name_value, user=user_value,
                                          password=password_value, autocommit=True)

    def get_projects(self):
        projects = []
        cursor = self.connection.cursor()
        try:
            cursor.execute("select id, name, description from mantis_project_table")
            for row in cursor:
                (id, name, description) = row
                projects.append(Project(id=str(id), name=name, description=description))
        finally:
            cursor.close()
        return projects

    def get_first_project(self):
        project = None
        cursor = self.connection.cursor()
        try:
            cursor.execute("select id, name, description from mantis_project_table limit 1")
            for row in cursor:
                (id, name, description) = row
                project = Project(id=str(id), name=name, description=description)
        finally:
            cursor.close()
        return project

    def destroy(self):
        self.connection.close()