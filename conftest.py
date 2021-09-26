import json
import os.path

import ftputil
import pytest

from fixture.application import Application
from fixture.db import DbFixture

fixture = None
target = None


@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--target"))


@pytest.fixture()
def app(request, config):
    global fixture
    browser = request.config.getoption("--browser")
    web_config = config["web"]
    web_admin_config = config["web_admin"]
    if fixture is None or not fixture.is_valid():
        fixture = Application(config=config, browser=browser)
    fixture.session.ensure_login(web_admin_config["username"], web_admin_config["password"])
    return fixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def final():
        fixture.session.ensure_logout()
        fixture.destroy()

    request.addfinalizer(final)
    return fixture


@pytest.fixture(scope="session")
def db(request, config):
    db_config = config["db"]
    db_fixture = DbFixture(host_value=db_config["host"], name_value=db_config["name"], user_value=db_config["user"],
                           password_value=db_config["password"])

    def final():
        db_fixture.destroy()

    request.addfinalizer(final)
    return db_fixture


@pytest.fixture(scope="session", autouse=True)
def configure_server(request, config):
    ftp_config = config['ftp']
    install_server_configuration(ftp_config['host'], ftp_config['username'], ftp_config['password'])

    def final():
        restore_server_configuration(ftp_config['host'], ftp_config['username'], ftp_config['password'])

    request.addfinalizer(final)


def install_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.back"):
            remote.remove("config_inc.php.back")
        if remote.path.isfile("config_inc.php"):
            remote.rename("config_inc.php", "config_inc.php.back")
        remote.upload(os.path.join(os.path.dirname(__file__), "resources/config_inc.php"), "config_inc.php")


def restore_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.back"):
            if remote.path.isfile("config_inc.php"):
                remote.remove("config_inc.php")
            remote.rename("config_inc.php.back", "config_inc.php")


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")


def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as open_file:
            target = json.load(open_file)
    return target
