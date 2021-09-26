from model.project_class import Project
from utils.random_utils import random_project_name_description


def test_add_projects(app):
    app.session.ensure_login_by_administrator()
    username, password = app.session.get_administrator_credentials()

    projects = app.soap.get_projects(username, password)
    assert projects is not None

    project_name, projects_description = random_project_name_description()
    project = Project(name=project_name, description=projects_description)
    app.project.create(project)
    projects.append(project)

    new_projects = app.soap.get_projects(username, password)
    assert new_projects is not None
    assert sorted(projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
