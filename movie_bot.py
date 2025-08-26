from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os

GENRE_LINKS = {
    "action": "https://www.rottentomatoes.com/browse/movies_at_home/genres:action",
    "comedy": "https://www.rottentomatoes.com/browse/movies_at_home/genres:comedy",
    "drama": "https://www.rottentomatoes.com/browse/movies_at_home/genres:drama",
    "horror": "https://www.rottentomatoes.com/browse/movies_at_home/genres:horror",
    "romance": "https://www.rottentomatoes.com/browse/movies_at_home/genres:romance",
    "sci-fi": "https://www.rottentomatoes.com/browse/movies_at_home/genres:sci_fi",
    "documentary": "https://www.rottentomatoes.com/browse/movies_at_home/genres:documentary",
    "animation": "https://www.rottentomatoes.com/browse/movies_at_home/genres:animation"
}

def fetch_movies(genre_choice, num_movies=5, filename="movie_recommendations.csv"):
    """
    Scrapes movie titles for a genre using Selenium and saves to a CSV.
    """
    if genre_choice not in GENRE_LINKS:
        print(f"🚫 Sorry, '{genre_choice}' is not a valid genre.")
        return

    target_url = GENRE_LINKS[genre_choice]
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    print(f"🌐 Fetching '{genre_choice.title()}' movies from Rotten Tomatoes...\n")
    browser = webdriver.Chrome(options=options)

    try:
        browser.get(target_url)
        time.sleep(4) # Wait for data to load

        tiles = browser.find_elements(By.CSS_SELECTOR, 'a.js-tile-link')[:num_movies]
        collected = []

        for idx, tile in enumerate(tiles):
            try:
                movie_title = tile.find_element(By.CSS_SELECTOR, 'span.p--small').text.strip()
            except Exception:
                movie_title = "Unknown Title"
            print(f"Movie {idx + 1}: {movie_title}")
            collected.append({"Title": movie_title, "Genre": genre_choice.title()})

        if not collected:
            print("⚠️ No movies found. Try another genre.")
            return

        df_movies = pd.DataFrame(collected)
        full_path = os.path.join(os.path.dirname(__file__), filename)
        df_movies.to_csv(full_path, mode="a", header=not os.path.exists(full_path), index=False)
        print(f"\n✅ Successfully saved {len(df_movies)} movies in {filename}")

    except PermissionError:
        print("❗ File is open elsewhere. Please close it and try again.")
    except Exception as err:
        print(f"⚡ Unexpected error: {err}")
    finally:
        browser.quit()

def preview_saved_movies(filename="movie_recommendations.csv", last_n=5):
    """
    Shows a preview of the last few saved movies.
    """
    preview_path = os.path.join(os.path.dirname(__file__), filename)
    if not os.path.exists(preview_path):
        print("No movies have been saved yet.")
        return
    try:
        data = pd.read_csv(preview_path)
        print(f"\nLast {last_n} movies saved:")
        print(data.tail(last_n))
    except Exception as err:
        print(f"Error reading saved movies: {err}")

if __name__ == "__main__":
    print("🎞️ Welcome to the Personalized Movie Bot!\nChoose from the following genres:")
    print(", ".join(GENRE_LINKS.keys()))
    user_genre = input("\nEnter your favorite genre: ").lower().strip()

    while user_genre not in GENRE_LINKS:
        user_genre = input("Invalid genre. Please enter one of the listed genres: ").lower().strip()

    try:
        user_count = int(input("How many movie suggestions do you want (1-10)? "))
        if user_count < 1 or user_count > 10:
            print("Limiting to 5 movies.")
            user_count = 5
    except ValueError:
        print("Defaulting to 5 movies.")
        user_count = 5

    fetch_movies(user_genre, num_movies=user_count)
    preview_saved_movies(last_n=user_count)

    print("\nThank you for using Movie Bot! 🎉")
    time.sleep(7)