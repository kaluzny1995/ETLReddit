import argparse

from pydantic import BaseModel


class ETLParams(BaseModel):
    phrase: str
    script_name: str
    batch_size: int
    is_filled_missing_dates: bool
    start_date: str
    date_interval: str
    is_until_previous_day: bool
    is_multiprocessing_used: bool
    num_processes: int

    class ConfigDict:
        frozen = True

    @staticmethod
    def from_argparse_namespace(args: argparse.Namespace) -> 'ETLParams':
        return ETLParams(
            phrase=args.phrase,
            script_name=args.script,
            batch_size=args.batch_size,
            is_filled_missing_dates=not args.skip_missing_dates,
            start_date = "N/A" if args.skip_missing_dates else args.start_date,
            date_interval = "N/A" if args.skip_missing_dates else args.interval,
            is_until_previous_day = False if args.skip_missing_dates else not args.until_today,
            is_multiprocessing_used = not args.no_multiprocessing,
            num_processes = 1 if args.no_multiprocessing else args.num_processes
        )
