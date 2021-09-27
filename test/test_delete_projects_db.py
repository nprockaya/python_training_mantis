from model.project_class import Project
from utils.random_utils import random_project_name_description


def test_delete_projects_db(app, db):
    app.session.ensure_login_by_administrator()

    if len(db.get_projects()) == 0:
        create_project_for_test(app)

    projects = db.get_projects()

    # Get id of first project from UI and get this project from DB by id
    project_for_delete_id = app.project.get_first_project_id()
    project_for_delete = db.get_project_by_id(project_for_delete_id)

    app.project.delete_first()

    new_projects = db.get_projects()
    new_projects.append(project_for_delete)
    assert sorted(projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)


def create_project_for_test(app):
    project_name, projects_description = random_project_name_description()
    project = Project(name=project_name, description=projects_description)
    app.project.create(project)
