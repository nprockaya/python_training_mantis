class SessionHelper:

    def __init__(self, app):
        self.app = app

    def login(self, user_name, password):
        wd = self.app.wd
        self.app.open_homepage()
        wd.find_element_by_name("username").send_keys(user_name)
        wd.find_element_by_name("password").send_keys(password)
        wd.find_element_by_css_selector("input[type='submit']").click()

    def logout(self):
        wd = self.app.wd
        wd.find_element_by_link_text("Logout").click()

    def ensure_logout(self):
        if self.is_logged_in():
            self.logout()

    def is_logged_in(self):
        wd = self.app.wd
        return len(wd.find_elements_by_link_text("Logout")) > 0

    def get_logged_user(self):
        wd = self.app.wd
        return wd.find_element_by_css_selector("td.login-info-left span").text

    def is_logged_in_as(self, user_name):
        return self.get_logged_user() == user_name

    def ensure_login_by_administrator(self):
        web_admin_config = self.app.config["web_admin"]
        username = web_admin_config['username']
        password = web_admin_config['password']
        if self.is_logged_in():
            if self.is_logged_in_as(username):
                return
            else:
                self.logout()
        self.login(username, password)
