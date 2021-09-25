import json
import os.path

import pytest

from fixture.application import Application
from fixture.db import DbFixture

fixture = None
target = None


@pytest.fixture()
def app(request):
    global fixture
    browser = request.config.getoption("--browser")
    web_config = load_config(request.config.getoption("--target"))["web"]
    web_admin_config = load_config(request.config.getoption("--target"))["web_admin"]
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=web_config["base_url"])
    fixture.session.ensure_login(web_admin_config["username"], web_admin_config["password"])
    return fixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def final():
        fixture.session.ensure_logout()
        fixture.destroy()

    request.addfinalizer(final)
    return fixture


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")


@pytest.fixture(scope="session")
def db(request):
    db_config = load_config(request.config.getoption("--target"))["db"]
    db_fixture = DbFixture(host_value=db_config["host"], name_value=db_config["name"], user_value=db_config["user"],
                           password_value=db_config["password"])

    def final():
        db_fixture.destroy()

    request.addfinalizer(final)
    return db_fixture


def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as open_file:
            target = json.load(open_file)
    return target
