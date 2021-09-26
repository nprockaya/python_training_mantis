from datetime import datetime

from model.project_class import Project


def test_delete_projects(app, db):
    app.session.ensure_login_by_administrator()

    if len(db.get_projects()) == 0:
        create_project_for_test(app)

    projects = db.get_projects()
    project_for_delete = db.get_first_project()
    app.project.delete_first()
    new_projects = db.get_projects()
    new_projects.append(project_for_delete)
    assert sorted(projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)


def create_project_for_test(app):
    # For generating unique project name
    date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    project = Project(name="Name " + date_time, description="Description " + date_time)
    app.project.create(project)
