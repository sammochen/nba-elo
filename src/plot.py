import json
from datetime import datetime, timedelta

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager

## Constants
nbaBlue = "#1d428a"
nbaRed = "#c8102e"

startLineDay = datetime(2021, 10, 18)
today = datetime(2021, 12, 14)
endLineDay = today + timedelta(1)

numberLineDay = endLineDay + timedelta(3)
ratingLineDay = numberLineDay + timedelta(4)

leftBorderDay = startLineDay
rightBorderDay = ratingLineDay + timedelta(5)


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

    plt.figure(figsize=(7, 6), dpi=200)
    plt.plot([today, today], [1200, 1800], color="#ddd", linewidth=0.5)


def postPlot():
    plt.title(
        "NBA Elo Ratings (2021 Season, 19/10 - 12/12)",
        color=nbaBlue,
        size=15,
        fontweight="bold",
    )

    plt.subplots_adjust(
        left=0.09,
        right=1 - 0.09,
        bottom=0.07,
        top=1 - 0.07,
    )
    plt.xlim(leftBorderDay, rightBorderDay)
    plt.ylim(1290, 1710)

    axes = plt.gca()
    axes.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%b"))
    axes.xaxis.set_major_locator(matplotlib.dates.MonthLocator())
    plt.xticks(rotation=90)

    plt.ylabel("Elo Rating")

    axes.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(100))
    axes.yaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(50))


def space(nums, gap):
    ans = nums[:]
    delta = 0.1
    while True:
        moved = False
        for i, x in enumerate(ans):
            above = False
            below = False
            for j, y in enumerate(ans):
                if i == j:
                    continue
                if x <= y <= x + gap:
                    above = True
                if x - gap <= y <= x:
                    below = True
            if above and not below:
                moved = True
                ans[i] -= delta
            if below and not above:
                moved = True
                ans[i] += delta
        if not moved:
            break
    return ans


def main():
    initFonts("Helvetica Condensed")

    prePlot()

    # Load data
    data = json.load(open("data.json"))
    colors = json.load(open("team-colors.json"))
    data.sort(key=lambda e: e["value"][-1][1])  # Sort from bad to good

    highlightTeams = ["PHX", "BKN", "DET"]
    highlightTeams = None

    highlightOpacity = 0.7
    opacity = 0.05

    textSize = 8

    y = [x["value"][-1][1] for x in data]
    spacedY = space(y, 7.5)
    for ind, obj in enumerate(data):
        dates = [startLineDay]
        dates += [datetime.fromtimestamp(e[0]) for e in obj["value"]]
        dates += [endLineDay]

        elos = [1500]
        elos += [e[1] for e in obj["value"]]
        elos += [elos[-1]]

        team = obj["team"]
        mainColor = colors[team]["mainColor"]
        mainHex = colors[team]["colors"][mainColor]["hex"]

        highlight = True if highlightTeams is None else team in highlightTeams

        plt.step(
            dates,
            elos,
            where="post",
            label=team,
            linewidth=1.2,
            color=mainHex,
            alpha=highlightOpacity if highlight else opacity,
            solid_capstyle="round",
        )

        if highlight:
            plt.annotate(
                f"{30 - ind}.",
                xy=(numberLineDay, spacedY[ind]),
                xytext=(0, 0),
                textcoords="offset points",
                color=mainHex,
                ha="right",
                va="center",
                annotation_clip=False,
                size=textSize,
                fontweight="bold",
            )
            plt.annotate(
                f" {team} ",
                xy=(numberLineDay, spacedY[ind]),
                xytext=(0, 0),
                textcoords="offset points",
                color=mainHex,
                ha="left",
                va="center",
                annotation_clip=False,
                size=textSize,
                fontweight="bold",
            )
            plt.annotate(
                f"({elos[-1]})",
                xy=(ratingLineDay, spacedY[ind]),
                xytext=(0, 0),
                textcoords="offset points",
                color=mainHex,
                ha="left",
                va="center",
                annotation_clip=False,
                size=textSize,
                fontweight="bold",
            )

    postPlot()
    plt.savefig("elo.jpg", dpi=400)


main()
