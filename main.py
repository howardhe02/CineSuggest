"""
This program will run our entire program!
Please type in: run_program('data/MoviesOnStreamingPlatforms_updated.csv')
to run the function. Enjoy!
For run_program_fast, it will take very long to scrape data, so if you
want to see how data is scraped fast, call run_fast_scrape(item) where
item is whatever you want to scrape.
"""
import csv
import os
import movie_class
import movie_select
import questionnaire
import scrape


def run_program(file: str = 'data/MoviesOnStreamingPlatforms_updated.csv') -> None:
    """This function runs everything in order, from the start questions to the end
    recommendations. This uses the default dataset given."""

    # Get user data of liked movies
    movies = []
    movies_search = []

    with open(file, encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            movies.append(row[2])
            movies_search.append(f"{row[2]} movie poster low resolution jpg")

    movies = sorted(movies[:40])
    movies_search = sorted(movies_search[:40])
    liked_movies, disliked_movies = movie_select.run_function(movies, movies_search)

    # Create tree and update it so the scores exist
    movie_tree = movie_class.load_movietree(file, [])
    movie_tree.score = movie_tree.new_score()
    movie_tree.remove_subtrees('')  # Prunes all trees with missing data in them

    movie_genres, movie_languages = get_movie_genres_and_languages(file)

    user_preferences = get_user_preferences(movie_genres)

    movie_tree.movie_filter(*user_preferences, movie_genres, movie_languages)

    # Remove disliked movies from recommendations
    for disliked_movie in disliked_movies:
        movie_tree.remove_subtrees(disliked_movie)

    recommended_movies = movie_tree.find_best_movies([], 12, liked_movies)

    if not recommended_movies:
        questionnaire.no_movies()
    else:
        recommended_movies_search = [f"{movie} movie poster low resolution jpg" for movie in recommended_movies]
        movie_select.display_movies(recommended_movies, recommended_movies_search)


def run_fast_scrape(item: str) -> None:
    """
    Scrapes one image of your choice (very fast).
    The image will be downloaded in the scrapefast folder located
    in the Google Image Scraper master directory.
    """
    path = os.path.normpath(os.getcwd() + "\\Google-Image-Scraper-master\\scrapefast")
    scrape.run_scrapy([item], 3, (0, 0), (10000, 10000), path)


def run_program_fast(file: str = 'data/MoviesOnStreamingPlatforms_updated.csv') -> None:
    """This function runs everything in order, from the start questions to the end
    recommendations. This uses the default dataset given.
    The fast version does not scrape images at the start, but only images at the end.
    This will only scrape 12 images, which is the faster version."""

    # Get user data of liked movies
    movies = []

    with open(file, encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            movies.append(row[2])

    movies = sorted(movies[:40])
    liked_movies, disliked_movies = movie_select.run_function_fast(movies)

    # Create tree and update it so the scores exist
    movie_tree = movie_class.load_movietree(file, [])
    movie_tree.score = movie_tree.new_score()
    movie_tree.remove_subtrees('')  # Prunes all trees with missing data in them

    movie_genres, movie_languages = get_movie_genres_and_languages(file)

    user_preferences = get_user_preferences(movie_genres)

    movie_tree.movie_filter(*user_preferences, movie_genres, movie_languages)

    # Remove disliked movies from recommendations
    for disliked_movie in disliked_movies:
        movie_tree.remove_subtrees(disliked_movie)

    recommended_movies = movie_tree.find_best_movies([], 12, liked_movies)

    if not recommended_movies:
        questionnaire.no_movies()
    else:
        recommended_movies_search = [f"{movie} movie poster low resolution jpg" for movie in recommended_movies]
        movie_select.display_movies(recommended_movies, recommended_movies_search)


def get_movie_genres_and_languages(file: str):
    """Extracts movie genres and languages from the dataset."""
    movie_genres = set()
    movie_languages = set()

    with open(file, encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)

        for row in reader:
            row_genres = row[13].split(',')
            for genre in row_genres:
                movie_genres.add(genre.strip())

            row_languages = row[15].split(',')
            for language in row_languages:
                movie_languages.add(language.strip())

    movie_genres.discard('')
    return movie_genres, movie_languages


def get_user_preferences(movie_genres):
    """Collects user preferences via questionnaire."""
    user_age = questionnaire.age()
    user_runtime = questionnaire.movie_runtime()
    user_early_year = questionnaire.oldest_years()
    user_later_year = questionnaire.newest_years(user_early_year)
    user_genres = questionnaire.genres(movie_genres)
    user_non_english_languages = questionnaire.languages()
    return user_age, user_runtime, user_early_year, user_later_year, user_genres, user_non_english_languages
