from model.project_class import Project
from utils.random_utils import random_project_name_description


def test_delete_projects(app):
    app.session.ensure_login_by_administrator()
    username, password = app.session.get_administrator_credentials()

    projects = app.soap.get_projects(username, password)
    assert projects is not None

    if len(projects) == 0:
        create_project_for_test(app)

    projects = app.soap.get_projects(username, password)
    assert projects is not None

    project_for_delete = app.soap.get_first_project(username, password)
    assert project_for_delete is not None
    app.project.delete_first()

    new_projects = app.soap.get_projects(username, password)
    assert new_projects is not None
    new_projects.append(project_for_delete)
    assert sorted(projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)


def create_project_for_test(app):
    project_name, projects_description = random_project_name_description()
    project = Project(name=project_name, description=projects_description)
    app.project.create(project)
