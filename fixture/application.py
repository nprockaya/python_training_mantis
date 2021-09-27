from selenium import webdriver

from fixture.james import JamesHelper
from fixture.mail import MailHelper
from fixture.project import ProjectHelper
from fixture.session import SessionHelper
from fixture.signup import SignupHelper
from fixture.soap import SoapHelper


class Application:
    def __init__(self, config, browser="firefox"):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "edge":
            self.wd = webdriver.Edge()
        elif browser == "opera":
            self.wd = webdriver.Opera()
        else:
            raise ValueError("Unrecognized browser %s" % browser)
        self.base_url = config['web']['base_url']
        self.james = JamesHelper(self)
        self.soap = SoapHelper(self)
        self.mail = MailHelper(self)
        self.signup = SignupHelper(self)
        self.session = SessionHelper(self)
        self.project = ProjectHelper(self)
        self.config = config

    def open_homepage(self):
        wd = self.wd
        wd.get(self.base_url)

    def destroy(self):
        self.wd.quit()

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False
