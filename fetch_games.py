# fetch_games.py
# Pulls a sample of games from the RAWG API and saves them to MySQL.

import os
import requests
from dotenv import load_dotenv
from database import get_connection

load_dotenv()

RAWG_API_KEY = os.getenv("rawgKey")
if not RAWG_API_KEY:
    raise ValueError("rawgKey not found — check your .env file and variable name")

BASE_URL = "https://api.rawg.io/api/games"


def fetch_top_games(count=50):
    """
    Requests a batch of top-rated games from RAWG.
    Returns a list of game dicts (raw JSON from the API).
    """
    params = {
        "key": RAWG_API_KEY,
        "ordering": "-rating",
        "page_size": count,
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    data = response.json()
    return data["results"]


def clean_game(game):
    """
    Takes one raw game dict from the API and pulls out just the
    fields we need, in the shape our table expects.
    """
    genre_names = [g["name"] for g in game.get("genres", [])]
    genre = ", ".join(genre_names) if genre_names else "Unknown"

    platform_list = game.get("platforms") or []
    platform_names = [p["platform"]["name"] for p in platform_list]
    platforms = ", ".join(platform_names) if platform_names else None

    return {
        "title": game["name"],
        "release_date": game.get("released") or "Unknown",
        "genre": genre,
        "platforms": platforms,
        "metacritic": game.get("metacritic"),
        "rating": game.get("rating"),
    }


def save_games(games):
    """
    Inserts a list of cleaned game dicts into the games table.

    Note: this table has no unique key tied to RAWG's data, so
    re-running this script will insert duplicate rows. Clear the
    table first (or add a unique constraint) if that matters to you.
    """
    conn = get_connection()
    cursor = conn.cursor()

    inserted = 0

    for raw_game in games:
        g = clean_game(raw_game)

        cursor.execute("""
            INSERT INTO games (
                title, release_date, genre, platforms, metacritic, rating
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            g["title"],
            g["release_date"],
            g["genre"],
            g["platforms"],
            g["metacritic"],
            g["rating"],
        ))
        inserted += 1

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Inserted {inserted} games.")


if __name__ == "__main__":
    print("Fetching games from RAWG...")
    games = fetch_top_games(count=50)
    save_games(games)