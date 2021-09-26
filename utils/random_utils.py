import random
import string


def random_username(maxlen=10):
    return "User_" + generate_random_part(maxlen)


def random_project_name_description(maxlen=10):
    random_part = generate_random_part(maxlen)
    return "Project_" + random_part, "Description_" + random_part


def generate_random_part(maxlen):
    symbols = string.ascii_letters
    return "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])
