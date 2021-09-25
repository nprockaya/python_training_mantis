def test_login(app):
    # Executing automatically by ensure_login function
    # app.session.login("administrator", "root")
    assert app.session.is_logged_in_as("administrator")
