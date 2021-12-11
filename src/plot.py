import json
import matplotlib.pyplot as plt

import matplotlib.dates as mdates
from datetime import datetime


def main():
    data = json.load(open("data.json"))
    for ind, obj in enumerate(data):

        value = obj["value"]
        for i in range(1, len(value)):
            if value[i][0] == value[i - 1][0]:
                print("bad")

        dates = [datetime.fromtimestamp(e[0]) for e in obj["value"]]
        elos = [e[1] for e in obj["value"]]
        plt.step(
            dates,
            elos,
            where="post",
            label=obj["team"],
            linewidth=2,
        )
        plt.text(dates[-1], elos[-1], f'{obj["team"]}')

    plt.title("NBA Elo Rankings", fontname="Helvetica Condensed")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_minor_locator(mdates.DayLocator())
    plt.xticks(rotation=90)
    plt.savefig("output.jpg", dpi=200)


main()