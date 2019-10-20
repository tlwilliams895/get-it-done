import hashlib
import random
import string

# Salt the hash to protect user pw
# Will randomly choose 5 different letters for the pw


def make_salt():
    return ''.join([random.choice(string.ascii_letters) for x in range(5)])


# Turns db pw into a hash
# sha255 reps the new pw being hashed
def make_pw_hash(password):
    salt = make_salt()
    hash = hashlib.sha256(str.encode(password + salt)).hexdigest()
    return '{0},{1}'.format(hash, salt)
    # return value will combine the pw and salt together for stronger pw protection


# Verifies user pw upon login
def check_pw_hash(password, hash):
    if make_pw_hash(password) == hash:
        return True
    # Why did he exclude the else clause?
    return False
