import axios from "axios";
import fs from "fs";

const fetchGames = async () => {
  const games = [];
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
      games.push(game);
    }

    if (data.meta.next_page === null) break;
  }
  return games;
};

const main = async () => {
  const games = await fetchGames();
  fs.writeFileSync("games.json", JSON.stringify(games));
};

main();
