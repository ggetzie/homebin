import csv
import re

dm = re.compile(r"(^\D+)(\d{1,3} \d{1,3} [NS]), (\d{1,3} \d{1,3} [EW])")


def convert_to_decimal(coord):
    # coord is in the format "33 00N"
    # we want to convert it to decimal degrees
    # 33 00N -> 33.0
    # 33 00S -> -33.0
    # 33 00E -> 33.0
    # 33 00W -> -33.0

    deg, mins, direction = coord.split()
    deg = int(deg)
    mins = int(mins)
    if direction in ["N", "E"]:
        return deg + mins / 60
    else:
        return -(deg + mins / 60)


def parse_line(line):
    # line is in the format "Afghanistan33 00N, 65 00E"
    # but some lines may have multiple entries such as:
    # "Ashmore and Cartier Islands12 25 S, 123 20 Enote - Ashmore Reef - 12 14 S, 123 05 E; Cartier Islet - 12 32 S, 123 32 E"
    m = dm.match(line)
    country, latitude, longitude = m.groups()
    latitude = convert_to_decimal(latitude)
    longitude = convert_to_decimal(longitude)
    return country, round(latitude, 3), round(longitude, 3)


def get_lines(filename="countries_center.txt"):
    with open(filename, "r") as f:
        return [parse_line(line) for line in f.readlines()]


def main():
    lines = get_lines()
    with open("countries_center.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["country", "latitude", "longitude"])
        writer.writerows(lines)


def match_countries():
    with open("countries_center.csv", "r") as f:
        reader = csv.DictReader(f)
        country_centers = {
            row["country"]: (float(row["latitude"]), float(row["longitude"]))
            for row in reader
        }
    lines = []
    with open("BookSales.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            country = row["Country"]
            if country in country_centers:
                lines.append((country, row["Sales"], *country_centers[country]))
            else:
                print(f"Country {country} not found")

    with open("BookSalesWithCoordinates.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["country", "sales", "latitude", "longitude"])
        writer.writerows(lines)
