import re


def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    match = re.match(pattern, email)
    return bool(match)


def contains_only_numbers(string):
    return string.isdigit()


def has_no_numbers_or_special_chars(string):
    allowed_characters = ['á', 'é', 'í', 'ó', 'ú', 'ñ', 'Ñ', 'Á', 'É', 'Í', 'Ó', 'Ú', ' ']
    for char in string:
        if not char.isalpha() and char not in allowed_characters:
            return False
    return True


def extract_number(string):
    number = int(string[1:-2])
    return number

