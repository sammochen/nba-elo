import { assert } from "console";
import elorank from "elo-rank";
import fs from "fs";

// first day of regular season is october 19th
const firstDay = new Date(2021, 9, 15);
const EloRank = new elorank();

const main = async () => {
  const games = JSON.parse(fs.readFileSync("games.json"));
  console.log(`Parsing ${games.length} games`);

  // Traverse in chronological order
  games.sort((a, b) => {
    return new Date(a.date) - new Date(b.date);
  });

  const validGames = games.filter((game) => {
    // unfinished game
    if (game.home_team_score === 0 || game.visitor_team_score === 0) {
      return false;
    }

    if (new Date(game.date) < firstDay) {
      // pre season
      return false;
    }

    assert(game.home_team_score !== game.visitor_team_score);
    return true;
  });

  const allTeams = new Set();

  for (const game of games) {
    const home = game.home_team.abbreviation;
    const visitor = game.visitor_team.abbreviation;

    allTeams.add(home);
    allTeams.add(visitor);
  }

  const dataPoints = new Map(); // team -> date/elo[]
  for (const team of allTeams) {
    dataPoints.set(team, [[firstDay.getTime() / 1000, 1500]]);
  }

  const gameIds = new Set();
  for (const game of validGames) {
    if (gameIds.has(game.id)) continue;
    gameIds.add(game.id);

    const home = game.home_team.abbreviation;
    const visitor = game.visitor_team.abbreviation;
    const date = new Date(game.date).getTime() / 1000;

    const [lastHomeTime, homeElo] = dataPoints.get(home).slice(-1)[0];
    const [lastVisitorTime, visitorElo] = dataPoints.get(visitor).slice(-1)[0];

    if (lastHomeTime === date || lastVisitorTime === date) {
      console.error(game);
      return;
    }

    const homeExpectedScore = EloRank.getExpected(homeElo, visitorElo);
    const visitorExpectedScore = EloRank.getExpected(visitorElo, homeElo);

    const homeScore = game.home_team_score > game.visitor_team_score ? 1 : 0;
    const visitorScore = 1 - homeScore;

    const updatedHomeElo = EloRank.updateRating(
      homeExpectedScore,
      homeScore,
      homeElo
    );
    const updatedVisitorElo = EloRank.updateRating(
      visitorExpectedScore,
      visitorScore,
      visitorElo
    );

    dataPoints.get(home).push([date, updatedHomeElo]);
    dataPoints.get(visitor).push([date, updatedVisitorElo]);
  }

  const dataAsList = [];
  dataPoints.forEach((value, key) => {
    dataAsList.push({ team: key, value: value });
  });

  fs.writeFileSync("data.json", JSON.stringify(dataAsList));
};

main();
