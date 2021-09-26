from utils.random_utils import random_username


def test_signup_new_account(app):
    username = random_username()
    email = username + "@localhost"
    password = "test"
    app.james.ensure_user_exists(username, password)
    app.signup.new_user(username, email, password)
    assert app.soap.can_login(username, password)
