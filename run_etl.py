import argparse
import datetime as dt

import util
from model import AppConfig, ETLParams
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
    parser.add_argument("--skip_missing_dates", required=False, default=defaults.is_missing_dates_skipped,
                        help=f"flag whether not to add blank records for periods without any data, default: {defaults.is_missing_dates_skipped}",
                        action="store_true")
    parser.add_argument("--start_date", type=str, required=False, default=defaults.start_date,
                        help=f"start date of missing file dates detection, default: {defaults.start_date}")
    parser.add_argument("--interval", type=str, required=False, choices=["h", "d", "m", "y"], default=defaults.date_interval,
                        help=f"period between every file date if for missing dates blank records are added, default: {defaults.date_interval}")
    parser.add_argument("--until_today", required=False, default=defaults.is_until_today,
                        help=f"flag whether to insert blank records until the current datetime, ie. moment of script launch (if no data for present date), default: {defaults.is_until_today}",
                        action="store_true")
    parser.add_argument("--no_multiprocessing", required=False, default=defaults.is_no_multiprocessing_used,
                        help=f"flag whether not to use multiprocessing while processing entries, default: {defaults.is_no_multiprocessing_used}",
                        action="store_true")
    parser.add_argument("--num_processes", type=int, required=False, default=defaults.num_processes,
                        help=f"number of processes if multiprocessing is used, default: {defaults.num_processes}")

    return parser.parse_args()


def run_sentiment_analysis(args: argparse.Namespace) -> None:
    """ Executes sentiment analysis script """
    etl_params = ETLParams.from_argparse_namespace(args)

    # Show parameters
    print("Reddits phrase:", etl_params.phrase)
    print("ETL script name:", etl_params.script_name)
    print("Batch size:", etl_params.batch_size)
    print("Fill in for missing dates:", etl_params.is_filled_missing_dates)
    print("Start date of searching missing dates:", etl_params.start_date)
    print("File date interval:", etl_params.date_interval)
    print("Is filled in until previous date:", etl_params.is_until_previous_day)
    print("Use multiprocessing:", etl_params.is_multiprocessing_used)
    print("Number of processes:", etl_params.num_processes)
    print()

    logger.info(f"Reddits phrase: {etl_params.phrase}")
    logger.info(f"ETL script name: {etl_params.script_name}")
    logger.info(f"Batch size: {etl_params.batch_size}")
    logger.info(f"Fill in for missing dates: {etl_params.is_filled_missing_dates}")
    logger.info(f"Start date of searching missing dates: {etl_params.start_date}")
    logger.info(f"File date interval: {etl_params.date_interval}")
    logger.info(f"Is filled in until previous date: {etl_params.is_until_previous_day}")
    logger.info(f"Use multiprocessing: {etl_params.is_multiprocessing_used}")
    logger.info(f"Number of processes: {etl_params.num_processes}")

    sentiment_analysis_service = SentimentAnalysisService(logger=logger)
    sentiment_analysis_service.run_etl(**etl_params.model_dump())


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
