import argparse
import json
from pathlib import Path
from typing import Iterator
from urllib.parse import quote
from urllib.request import urlopen


class WeatherData:
    def __init__(self, city: str, temperature: int, country: str) -> None:
        self.city = city
        self.temperature = temperature
        self.country = country


def read_cities(file_name: Path) -> Iterator[str]:
    with file_name.open("r", encoding="utf-8-sig") as file:
        cities = (line.strip() for line in file)
        yield from (city for city in cities if city)


def get_weather(city: str) -> WeatherData:
    city_for_url = quote(city)
    url = "https://wttr.in/" + city_for_url + "?format=j1"

    with urlopen(url, timeout=20) as response:
        data = json.load(response)

    temperature = int(data["current_condition"][0]["temp_C"])
    country = data["nearest_area"][0]["country"][0]["value"]

    return WeatherData(city, temperature, country)


def temperature_to_string(temperature: int | float) -> str:
    if temperature == int(temperature):
        temperature = int(temperature)

    sign = "+" if temperature > 0 else ""
    return sign + str(temperature) + " °C"


def make_report(weather_list: list[WeatherData]) -> str:
    city_lines = [
        weather.city
        + ", "
        + weather.country
        + " "
        + temperature_to_string(weather.temperature)
        for weather in weather_list
    ]

    countries = {
        weather.country: [
            item.temperature
            for item in weather_list
            if item.country == weather.country
        ]
        for weather in weather_list
    }

    country_lines = (
        country
        + " — cities: "
        + str(len(temperatures))
        + "; avg: "
        + temperature_to_string(round(sum(temperatures) / len(temperatures), 1))
        + "; min: "
        + temperature_to_string(min(temperatures))
        + "; max: "
        + temperature_to_string(max(temperatures))
        for country, temperatures in countries.items()
    )

    return "\n".join(city_lines + ["", "Statistics by country:"] + list(country_lines))


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Get current weather and group cities by country."
    )
    parser.add_argument(
        "cities_file",
        type=Path,
        help="Text file containing one city per line",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="File for saving the result",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    weather_list = [get_weather(city) for city in read_cities(args.cities_file)]
    report = make_report(weather_list)

    print(report)

    if args.output:
        args.output.write_text(report + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
