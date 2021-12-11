import json
from datetime import datetime

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager

nbaBlue = "#17408B"


def initFonts():
    font_dirs = ["./fonts"]
    font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
    for font_file in font_files:
        font_manager.fontManager.addfont(font_file)

    matplotlib.rcParams["font.sans-serif"] = "Helvetica Condensed"
    matplotlib.rcParams["font.family"] = "sans-serif"


def main():
    initFonts()

    startDay = datetime(2021, 10, 15)
    endDay = datetime(2021, 12, 15)
    postDay = datetime(2021, 12, 31)

    plt.title("NBA Elo Ratings, 2021 Season", color=nbaBlue)

    data = json.load(open("data.json"))
    colors = json.load(open("team-colors.json"))

    textPoints = []  # x, y, newy, team, color
    for obj in data:

        dates = (
            [startDay] + [datetime.fromtimestamp(e[0]) for e in obj["value"]] + [endDay]
        )
        elos = [1500] + [e[1] for e in obj["value"]] + [obj["value"][-1][1]]

        team = obj["team"]
        mainColor = colors[team]["mainColor"]
        mainHex = colors[team]["colors"][mainColor]["hex"]

        plt.step(
            dates,
            elos,
            where="post",
            label=team,
            linewidth=1,
            color=mainHex,
            alpha=1,
        )

        textPoints.append([dates[-1], elos[-1], elos[-1], team, mainHex])

    # Adjust final text y positions
    textPoints.sort(key=lambda e: e[1])
    minElo = textPoints[0][1]
    maxElo = textPoints[-1][1]

    for i in range(len(textPoints)):
        textPoints[i][2] = minElo + i * (maxElo - minElo) / 29

    for i, point in enumerate(textPoints):
        x, y, newy, team, mainHex = point

        plt.annotate(
            f"{30 - i}. {team} ({y})",
            xy=(postDay, newy),
            xytext=(-5, 0),
            textcoords="offset points",
            color=mainHex,
            ha="right",
            va="center",
            annotation_clip=False,
            fontsize=7.5,
        )

    plt.xlim(startDay, postDay)
    plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%b"))
    plt.gca().xaxis.set_major_locator(matplotlib.dates.MonthLocator())
    plt.xticks(rotation=90)
    plt.savefig("output.jpg", dpi=300)


main()
