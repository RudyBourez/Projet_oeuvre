import secrets
import string

def generate_password(pwd_length:int):
    
    letters = string.ascii_letters
    digits = string.digits
    special_chars = string.punctuation
    
    alphabet = letters+digits+special_chars
    password = ""
    
    for i in range(pwd_length):
        password += ''.join(secrets.choice(alphabet))
        
    return password