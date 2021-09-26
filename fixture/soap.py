from suds import WebFault
from suds.client import Client

from model.project_class import Project


class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = Client("http://localhost/mantisbt/api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_projects(self, username, password):
        client = Client("http://localhost/mantisbt/api/soap/mantisconnect.php?wsdl")
        try:
            projects = client.service.mc_projects_get_user_accessible(username, password)
            return list(map(lambda x: Project(id=x.id, name=x.name, description=x.description), projects))
        except WebFault:
            return None

    def get_first_project(self, username, password):
        projects = sorted(self.get_projects(username, password), key=lambda project: project.name)
        if projects is not None and len(projects) > 0:
            return projects[0]
        else:
            return None
