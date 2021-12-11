import json
from datetime import datetime

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager


def initFonts():
    font_dirs = ["./fonts"]
    font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
    for font_file in font_files:
        font_manager.fontManager.addfont(font_file)

    matplotlib.rcParams["font.sans-serif"] = "Helvetica Condensed"
    matplotlib.rcParams["font.family"] = "sans-serif"


def main():
    initFonts()

    data = json.load(open("data.json"))
    colors = json.load(open("team-colors.json"))
    for obj in data:
        value = obj["value"]
        for i in range(1, len(value)):
            if value[i][0] == value[i - 1][0]:
                print("bad")

        dates = [datetime.fromtimestamp(e[0]) for e in obj["value"]]
        elos = [e[1] for e in obj["value"]]

        # Get primary and secondary colors
        mainColor = colors[obj["team"]]["mainColor"]
        mainHex = colors[obj["team"]]["colors"][mainColor]["hex"]

        plt.step(
            dates,
            elos,
            where="post",
            label=obj["team"],
            linewidth=1,
            color=mainHex,
            alpha=1,
        )

        plt.text(dates[-1], elos[-1], f'{obj["team"]}')

    plt.title("NBA Elo Ratings, 2021 Season")
    plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%b"))
    plt.gca().xaxis.set_major_locator(matplotlib.dates.MonthLocator())
    plt.xticks(rotation=90)
    plt.savefig("output.jpg", dpi=200)


main()
