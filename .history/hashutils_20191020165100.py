import hashlib

# Turns db pw into a hash
# sha255 reps the new pw being hashed


def make_pw_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


# Verifies user pw upon login
def check_pw_hash(password, hash):
    pass
