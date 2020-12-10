import random
import hashlib, uuid
import string
import bcrypt


# NUMBER_OF_GENARATED_PASSWORDS = 100000
NUMBER_OF_GENARATED_PASSWORDS = 100
NUMBER_OF_TOP_HUNDRED = int(NUMBER_OF_GENARATED_PASSWORDS*0.10)
NUMBER_OF_TOP_K_HUNDRED = int(NUMBER_OF_GENARATED_PASSWORDS*0.80)
NUMBER_OF_RANDOM = int(NUMBER_OF_GENARATED_PASSWORDS*0.05)
NUMBER_OF_RANDOM_HUMANLIKE = int(NUMBER_OF_GENARATED_PASSWORDS*0.05)


top100_passwords = list(open('10-million-password-list-top-100.txt'))
top100_000_passwords = list(open('10-million-password-list-top-1000000.txt'))[:100001]

passwords_md5 = open("passwordsMD5.txt","w+")
passwords_sha_1 = open("passwordsSHA-1.txt","w+")
passwords_bcrypt = open("passwordsBcrypt.txt","w+")

passwords = []

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def random_change_string(input):
    methodId = random.randint(0, 3)
    if(methodId == 0):
        return input.capitalize()
    elif(methodId == 1):
        return  input.lower()
    elif(methodId == 2):
        return input.upper()
    elif(methodId == 3):
        return input[::-1]

def set_top_100():
    random_numbers = random.sample(range(0, 100), NUMBER_OF_TOP_HUNDRED)
    for index in random_numbers:
        passwords.append(top100_passwords[index][:-1])


def set_top_100_000():
    random_numbers = random.sample(range(0, 100000), NUMBER_OF_TOP_K_HUNDRED)
    for index in random_numbers:
        passwords.append(top100_000_passwords[index][:-1])

def generate_random_password():
    password_length = random.randint(6,10)
    password = ''
    for _ in range(password_length):
        password += chr(random.randint(97, 122))
    return password

def set_random():
    for _ in range(NUMBER_OF_RANDOM):
        passwords.append(generate_random_password())

def set_random_humanlike():
    for _ in range(NUMBER_OF_RANDOM):
        passwords.append(random_change_string(top100_000_passwords[random.randint(0, 100000)][:-1]))

def generate_passwords():
    set_top_100()
    set_top_100_000()
    set_random()
    set_random_humanlike()
    print(passwords)

generate_passwords()
for password in passwords:
     passwords_md5.write(str(hashlib.md5(password.encode()).hexdigest())+'\n')
passwords_md5.close()

passwords = []
generate_passwords()
for password in passwords:
    salt = get_random_string(8)
    passwords_sha_1.write(str(hashlib.sha1((password+salt).encode()).hexdigest())+'.'+salt+'\n')
passwords_sha_1.close()

passwords = []
generate_passwords()
for password in passwords:
    salt = bcrypt.gensalt()
    passwords_bcrypt.write(str(bcrypt.hashpw(password.encode(), salt))+'\n')
passwords_bcrypt.close()
