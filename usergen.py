import random


def get_users(n=50):
    fn_path = "/Users/gabe/first_names_ascii.txt"
    ln_path = "/Users/gabe/last_names_ascii.txt"
    with (
        open(fn_path, encoding="utf-8") as fn_file,
        open(ln_path, encoding="utf-8") as ln_file,
    ):
        first_names = random.sample([name.strip() for name in fn_file.readlines()], n)
        last_names = random.sample([name.strip() for name in ln_file.readlines()], n)
        return [
            {"name": " ".join([first, last]), "email": first[0] + last + "@example.com"}
            for first, last in zip(first_names, last_names)
        ]
