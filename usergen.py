import pathlib
import random
import re


def read_data(fp="/Users/gabe/USA_01.txt"):
    f = pathlib.Path(fp)
    with f.open(encoding="utf-8") as fin:
        lines = [line.strip().split(":") for line in fin.readlines()]
    return lines


def user_from_line(line):
    first_name = line[2]
    last_name = line[3]
    name = " ".join([first_name, last_name])
    email = first_name[0] + re.sub(r"\W", "", last_name) + "@example.com"
    return name, email


def get_users(lines, n=50):
    lines = [line for line in lines if line[2] and line[3]]
    users = [user_from_line(line) for line in random.sample(lines, n)]
    return users
