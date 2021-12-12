import json
from datetime import datetime, timedelta

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager

## Constants
nbaBlue = "#1d428a"
nbaRed = "#c8102e"

startDay = datetime(2021, 10, 15)
endDay = datetime(2021, 12, 15)
rightDay = endDay + timedelta(15)
today = datetime(2021, 12, 13)


def initFonts(defaultFont):
    # Load font
    font_dirs = ["./fonts"]
    font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
    for font_file in font_files:
        font_manager.fontManager.addfont(font_file)

    # Set default to Helvetica Condensed
    matplotlib.rcParams["font.sans-serif"] = defaultFont
    matplotlib.rcParams["font.family"] = "sans-serif"


def prePlot():
    backgroundColor = "#eee"

    # Change background color
    plt.figure().patch.set_facecolor(backgroundColor)
    plt.gca().set_facecolor(backgroundColor)

    # line for today
    plt.plot([today, today], [1200, 1800], color="#bbb", linewidth=1)


def getHighlight():
    highlight = [False] * 30

    highlight[0] = True  # DET
    highlight[4] = True  # HOU
    highlight[25] = True  # MIL
    highlight[28] = True  # GSW
    highlight[29] = True  # PHX
    return highlight


def main():
    initFonts("Helvetica Condensed")

    # Load data
    data = json.load(open("data.json"))
    colors = json.load(open("team-colors.json"))
    data.sort(key=lambda e: e["value"][-1][1])  # Sort from bad to good

    highlight = getHighlight()

    for ind, obj in enumerate(data):
        dates = [startDay]
        dates += [datetime.fromtimestamp(e[0]) for e in obj["value"]]
        dates += [endDay]

        elos = [1500]
        elos += [e[1] for e in obj["value"]]
        elos += [elos[-1]]

        team = obj["team"]
        mainColor = colors[team]["mainColor"]
        mainHex = colors[team]["colors"][mainColor]["hex"]

        plt.step(
            dates,
            elos,
            where="post",
            label=team,
            linewidth=2.5,
            color=mainHex,
            alpha=(0.8 if highlight[ind] else 0.05),
            solid_capstyle="round",
        )

        if highlight[ind]:
            plt.annotate(
                f"{30 - ind}. {team} ({elos[-1]})",
                xy=(rightDay, elos[-1]),
                xytext=(-5, 0),
                textcoords="offset points",
                color=mainHex,
                ha="right",
                va="center",
                annotation_clip=False,
                size=10,
                fontweight="bold",
            )

    plt.suptitle("NBA Elo Ratings", color=nbaBlue, size=15, fontweight="bold")
    plt.title("19/10/21 — 12/12/21", size=10, fontweight="bold")

    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1)
    plt.xlim(startDay, rightDay)
    plt.ylim(1290, 1710)

    axes = plt.gca()
    axes.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%b"))
    axes.xaxis.set_major_locator(matplotlib.dates.MonthLocator())
    axes.xaxis.set_minor_locator(matplotlib.dates.DayLocator())
    plt.xticks(rotation=90)

    axes.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(100))
    axes.yaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(50))

    plt.savefig("output.jpg", dpi=400)


main()
