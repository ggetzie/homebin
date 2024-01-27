import random
import string

CHARSETS = {
    "alpha": string.ascii_letters,
    "lower": string.ascii_lowercase,
    "upper": string.ascii_uppercase,
    "alphanum": string.ascii_letters + string.digits,
    "all": string.ascii_letters + string.digits + "!@$%^&*_|#",
}


def random_string(length=10, charset="all"):
    chars = CHARSETS[charset]
    return "".join([random.SystemRandom().choice(chars) for _ in range(length)])
