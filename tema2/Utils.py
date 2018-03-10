import random, string


def generate_random_string():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
