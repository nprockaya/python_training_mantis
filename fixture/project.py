class ProjectHelper:

    def __init__(self, app):
        self.app = app

    def open_projects_page(self):
        wd = self.app.wd
        wd.find_element_by_xpath("//a[.='Manage']").click()
        wd.find_element_by_xpath("//a[.='Manage Projects']").click()

    def create(self, project):
        wd = self.app.wd
        self.app.open_homepage()
        self.open_projects_page()
        wd.find_element_by_xpath("//input[@value='Create New Project']").click()
        wd.find_element_by_name("name").click()
        wd.find_element_by_name("name").clear()
        wd.find_element_by_name("name").send_keys(project.name)
        wd.find_element_by_name("description").click()
        wd.find_element_by_name("description").clear()
        wd.find_element_by_name("description").send_keys(project.description)
        wd.find_element_by_xpath("//input[@value='Add Project']").click()

    def delete_first(self):
        wd = self.app.wd
        self.app.open_homepage()
        self.open_projects_page()
        wd.find_elements_by_css_selector("tr.row-1")[0].find_elements_by_css_selector("*")[1].click()
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
