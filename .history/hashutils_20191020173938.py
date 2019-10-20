import hashlib
import random
import string

# Salt the hash to protect user pw


# Turns db pw into a hash
# sha255 reps the new pw being hashed
def make_pw_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


# Verifies user pw upon login
def check_pw_hash(password, hash):
    if make_pw_hash(password) == hash:
        return True
    # Why did he exclude the else clause?
    return False
