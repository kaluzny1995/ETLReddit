import argparse
import datetime as dt

import util
import error
from model import AppConfig
from provider import SupabasePostgresRedditProvider, SupabasePostgresCommentProvider, SupabasePostgresSentimentAnalysisProvider
from service import SentimentAnalysisService

logger = util.setup_logger(name="run_etl",
                           log_file=f"logs/run_etl/run_etl_{dt.datetime.now().isoformat()}.log")


def get_config() -> AppConfig:
    return AppConfig.from_json()


def parse_args(defaults: AppConfig) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reddits ETL Python 3.11 application.")

    parser.add_argument("script", type=str, choices=["sentiment_analysis", "vectorization"],
                        help="ETL script to run")
    parser.add_argument("phrase", type=str,
                        help="phrase which contain reddits to do the ETL with")
    parser.add_argument("-b", "--batch_size", type=int, required=False, default=defaults.batch_size,
                        help=f"size of inserted batch of reddits into database, default: {defaults.batch_size}")
    parser.add_argument("--use_multiprocessing", required=False, default=defaults.is_multiprocessing_used,
                        help=f"flag whether to use multiprocessing while processing entries, default: {defaults.is_multiprocessing_used}",
                        action="store_true")
    parser.add_argument("--num_processes", type=int, required=False, default=defaults.num_processes,
                        help=f"number of processes if multiprocessing is used, default: {defaults.num_processes}")

    return parser.parse_args()


def run_sentiment_analysis(args: argparse.Namespace) -> None:
    """ Executes sentiment analysis script """

    phrase = args.phrase
    script_name = args.script
    batch_size = args.batch_size
    is_multiprocessing_used = args.use_multiprocessing
    num_processes = args.num_processes

    # Show parameters
    print("Reddits phrase:", phrase)
    print("ETL script name:", script_name)
    print("Batch size:", batch_size)
    print("Use multiprocessing:", is_multiprocessing_used)
    print("Number of processes:", num_processes)
    print()

    logger.info(f"Reddits phrase: {phrase}")
    logger.info(f"ETL script name: {script_name}")
    logger.info(f"Batch size: {batch_size}")
    logger.info(f"Use multiprocessing: {is_multiprocessing_used}")
    logger.info(f"Number of processes: {num_processes}")

    # load source file dates
    supabase_postgres_reddit_provider = SupabasePostgresRedditProvider(logger=logger)
    source_file_dates = sorted(supabase_postgres_reddit_provider.get_file_dates(phrase=phrase))
    print("Source file dates:\n", source_file_dates)
    logger.info(f"Source file dates: {source_file_dates}")

    # load target files dates
    supabase_postgres_sentiment_analysis_provider = SupabasePostgresSentimentAnalysisProvider(logger=logger)
    target_file_dates = sorted(supabase_postgres_sentiment_analysis_provider.get_file_dates(phrase=phrase))
    print("Target file dates:\n", target_file_dates)
    logger.info(f"Target file dates: {target_file_dates}")
    recent_target_file_date = None if len(target_file_dates) == 0 else target_file_dates[-1]
    print("Recent target file date:", recent_target_file_date)
    logger.info(f"Recent target file date: {recent_target_file_date}")
    print()

    # determine the missing file dates to load the data for
    missing_file_dates = source_file_dates if recent_target_file_date is None \
        else list(filter(lambda fd: fd > recent_target_file_date, source_file_dates))
    if len(missing_file_dates) == 0:
        print("No new files available. Finishing.")
        logger.info(f"No new files available. Finishing.")
        raise error.NoNewDataError("No new files available for ETL.")
    print(f"\nLoading data for the following dates:\n{missing_file_dates}\n")
    logger.info(f"Loading data for the following dates: {missing_file_dates}")

    # get reddit and comment entries
    reddits = supabase_postgres_reddit_provider.get_reddits(phrase=phrase, file_dates=missing_file_dates)
    supabase_postgres_comment_provider = SupabasePostgresCommentProvider(logger=logger)
    comments = supabase_postgres_comment_provider.get_comments(phrase=phrase, file_dates=missing_file_dates)
    entries = reddits + comments

    # process reddit and comment entries
    print("Reddit and comment entries loaded:", len(entries))
    logger.info(f"Reddit and comment entries loaded: {len(entries)}")
    sentiment_analysis_service = SentimentAnalysisService(is_multiprocessing_used=is_multiprocessing_used,
                                                          num_processes=num_processes, logger=logger)
    sentiment_analyses = sentiment_analysis_service.run_etl(entries)
    print(f"Sentiment analyses processed: {len(sentiment_analyses)}.\n")
    logger.info(f"Sentiment analyses processed: {len(sentiment_analyses)}.")

    # insert sentiment analyses
    supabase_postgres_sentiment_analysis_provider.insert_sentiment_analyses(sentiment_analyses,
                                                                            batch_size=batch_size)


def run_vectorization(args: argparse.Namespace) -> None:
    """ Executes texts vectorization script """
    raise NotImplementedError("The texts vectorization script has not been implemented yet.")


def main():
    print("---- Reddits ETL app ----\n")
    logger.info("---- Reddits ETL app ----")

    config = get_config()
    args = parse_args(config)

    # run ETL script
    etl_scripts = dict({
        'sentiment_analysis': run_sentiment_analysis,
        'vectorization': run_vectorization
    })
    etl_scripts[args.script](args)

    print("\nDone.")
    logger.info("Done.")


if __name__ == "__main__":
    main()
