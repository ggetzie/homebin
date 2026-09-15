#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
import random
import argparse


def get_users(n=50):
    fn_path = "/Users/gabe/datasets/first_names_ascii.txt"
    ln_path = "/Users/gabe/datasets/last_names_ascii.txt"
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate random user data")
    parser.add_argument(
        "-n",
        "--number",
        type=int,
        default=50,
        help="Number of users to generate (default: 50)",
    )
    args = parser.parse_args()
    users = get_users(args.number)
    for user in users:
        print(user)
