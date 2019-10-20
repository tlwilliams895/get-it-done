import hashlib
import random
import string

# Salt the hash to protect user pw
# Will randomly choose 5 different letters for the pw


def make_salt():
    return ''.join([random.choice(string.ascii_letters) for x in range(5)])


# Turns db pw into a hash
# sha255 reps the new pw being hashed
def make_pw_hash(password, salt=None):
    if not salt:
        salt = make_salt()
    salt = make_salt()
    hash = hashlib.sha256(str.encode(password + salt)).hexdigest()
    return '{0},{1}'.format(hash, salt)
    # return value will combine the pw and salt together for stronger pw protection


# Verifies user pw upon login
def check_pw_hash(password, hash):
    salt = hash.split(',')[1]
    if make_pw_hash(password, salt) == hash:
        return True
    # Why did he exclude the else clause?
    return False
