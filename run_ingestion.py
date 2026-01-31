import os
import argparse
import datetime as dt

import util
import error
from model import AppConfig
from provider import JsonFileObjectProvider, \
    SupabasePostgresRedditProvider, SupabasePostgresCommentProvider, SupabasePostgresAuthorProvider, \
    JsonRedditProvider, JsonCommentProvider, JsonAuthorProvider


logger = util.setup_logger(name="run_ingestion",
                           log_file=f"logs/run_ingestion/run_ingestion_{dt.datetime.now().isoformat()}.log")


def get_config() -> AppConfig:
    return AppConfig.from_json()


def parse_args(defaults: AppConfig) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reddits ingestion Python 3.11 application.")

    parser.add_argument("phrase", type=str, help="phrase which contain reddits to do the ETL with")
    parser.add_argument("-b", "--batch_size", type=int, required=False, default=defaults.batch_size,
                        help=f"size of inserted batch of reddits into database, default: {defaults.batch_size}")
    parser.add_argument("--load_authors", required=False, default=defaults.is_author_loaded,
                        help=f"flag whether to load reddit authors information, default: {defaults.is_author_loaded}",
                        action="store_true")

    return parser.parse_args()


def get_source_folder_path(folder_name: str) -> str:
    """ Returns the absolute JSON files source folder path """
    return f"{os.path.abspath(os.path.join(os.getcwd(), os.pardir))}/{folder_name}"


def main():
    print("---- Reddits ingestion app ----\n")
    logger.info("---- Reddits ingestion app ----")

    config = get_config()
    args = parse_args(config)

    phrase = args.phrase
    batch_size = args.batch_size
    is_author_loaded = args.load_authors

    # Show parameters
    print("Reddits phrase:", phrase)
    print("Batch size:", batch_size)
    print("Authors loaded:", is_author_loaded)
    print()

    files_reddit_source_folder = config.files_reddit_source_folder_pattern.format(phrase=phrase)
    files_author_source_folder = config.files_author_source_folder_pattern.format(phrase=phrase)
    json_reddit_file_object_provider = JsonFileObjectProvider(get_source_folder_path(files_reddit_source_folder))
    json_author_file_object_provider = JsonFileObjectProvider(get_source_folder_path(files_author_source_folder))

    # load source file dates
    source_file_dates = sorted(map(util.get_start_date_string_from_filename,
                                   json_reddit_file_object_provider.get_file_names()))
    print("Source file dates:\n", source_file_dates)

    # load target files dates
    supabase_postgres_reddit_provider = SupabasePostgresRedditProvider()
    target_file_dates = sorted(supabase_postgres_reddit_provider.get_file_dates(phrase=phrase))
    print("Target file dates:\n", target_file_dates)
    recent_target_file_date = None if len(target_file_dates) == 0 else target_file_dates[-1]
    print("Recent target file date:", recent_target_file_date)
    print()

    # determine the missing file dates to load the data for
    missing_file_dates = source_file_dates if recent_target_file_date is None \
        else list(filter(lambda fd: fd > recent_target_file_date, source_file_dates))
    if len(missing_file_dates) == 0:
        print("No new files available. Finishing.")
        logger.info(f"No new files available. Finishing.")
        raise error.NoNewFileError("No new files available for ingestion.")
    print(f"\nLoading data for the following dates:\n{missing_file_dates}\n")
    logger.info(f"Loading data for the following dates: {missing_file_dates}")

    # insert reddits
    json_reddit_provider = JsonRedditProvider(json_reddit_file_object_provider)
    reddits = json_reddit_provider.get_reddits(missing_file_dates, phrase=phrase)
    print("Reddits processed:", len(reddits))
    logger.info(f"Reddits processed: {len(reddits)}")
    supabase_postgres_reddit_provider.insert_reddits(reddits, batch_size=batch_size)

    json_comment_provider = JsonCommentProvider(json_reddit_file_object_provider)
    comments = json_comment_provider.get_comments(missing_file_dates, phrase=phrase)
    print("Comments processed:", len(comments))
    logger.info(f"Comments processed: {len(comments)}")
    supabase_postgres_comment_provider = SupabasePostgresCommentProvider()
    supabase_postgres_comment_provider.insert_comments(comments, batch_size=batch_size)

    if is_author_loaded:
        supabase_postgres_author_provider = SupabasePostgresAuthorProvider()
        existing_names = supabase_postgres_author_provider.get_names()

        json_author_provider = JsonAuthorProvider(json_author_file_object_provider)
        authors = json_author_provider.get_authors(missing_file_dates)
        authors = list(filter(lambda a: a.name not in existing_names, authors))
        print("Authors processed:", len(authors))
        logger.info(f"Authors processed: {len(authors)}")
        supabase_postgres_author_provider.insert_authors(authors, batch_size=batch_size)

    print("\nDone.")
    logger.info("Done.")


if __name__ == "__main__":
    main()
