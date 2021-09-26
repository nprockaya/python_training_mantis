from datetime import datetime

from model.project_class import Project


def test_add_projects(app, db):
    app.session.ensure_login_by_administrator()

    projects = db.get_projects()
    # For generating unique project name
    date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    project = Project(name="Name " + date_time, description="Description " + date_time)
    app.project.create(project)
    projects.append(project)
    new_projects = db.get_projects()
    assert sorted(projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
