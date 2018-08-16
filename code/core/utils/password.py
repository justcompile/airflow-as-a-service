import random
import string


def password_generator():
    lower_case_letter = random.choice(string.ascii_lowercase)
    upper_case_letter = random.choice(string.ascii_uppercase)

    other_characters = [
        random.choice(string.ascii_letters + string.digits + '!-_.')
        for index in range(random.randint(12, 30))
    ]

    all_together = [lower_case_letter, upper_case_letter] + other_characters

    random.shuffle(all_together)

    return ''.join(all_together)
