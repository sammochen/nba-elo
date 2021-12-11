import axios from "axios";
import fs from "fs";

// First day of the NBA
const firstDay = new Date(2021, 9, 19);

const fetchGames = async () => {
  const games = [];
  const ids = new Set();

  for (let page = 0; ; page++) {
    console.log(`Fetching page ${page}...`);
    const { data } = await axios.get(
      "https://www.balldontlie.io/api/v1/games",
      {
        params: {
          page,
          per_page: 100,
          seasons: [2021],
        },
      }
    );

    for (const game of data.data) {
      if (ids.has(game.id)) continue; // no duplicates
      if (new Date(game.date) < firstDay) continue; // summer league
      if (game.home_team_score === 0 || game.visitor_team_score === 0) continue; // incomplete

      ids.add(game.id);
      games.push(game);
    }

    if (data.meta.next_page === null) break;
  }

  // Sort by chronological order
  games.sort((a, b) => {
    return new Date(a.date) - new Date(b.date);
  });
  return games;
};

const main = async () => {
  const games = await fetchGames();
  fs.writeFileSync("games.json", JSON.stringify(games));
  console.log(`Successfully downloaded ${games.length} games`);
};

main();
