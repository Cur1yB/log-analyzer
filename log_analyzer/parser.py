from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser(description='Log Analyzer for processing *.log file[s], where each line is JSON object.')
    parser.add_argument(
        "--file",
        type=str,
        required=True,
        help="Path to file | files separated by space",
    )
    parser.add_argument("--report", type=str, default="average", help="Report type")
    parser.add_argument("--date", type=str, default=None, help="Date in format YYYY-MM-DD")
    args = parser.parse_args()
    file = args.file
    report_name = args.report
    date = args.date
    return file, report_name, date
