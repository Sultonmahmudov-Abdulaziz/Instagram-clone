import re

def is_valid_phone(phone):
    pattern = r'^\+998\d{9}$'
    if re.match(pattern, phone):
        return True
    else:
        return False
    

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if re.match(pattern, email):
        return True
    else:
        return False

