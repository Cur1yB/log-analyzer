from log_analyzer.analizer import Analyzer
from log_analyzer.parser import parse_args
from log_analyzer.formatter import REPORT_FORMATTERS_MAPPER


def main():
    file, report_name, date = parse_args()
    files = file.split(" ")
    analizer = Analyzer()

    data = analizer.analyze_rows(
        files, processor_name=report_name, date_for_analize=date
    )
    # if need other formats (plain, html, csv etc.), there you can add it in mapper
    output = REPORT_FORMATTERS_MAPPER[report_name](
        table=data,
        sort_by=1,
        report_name=report_name,
    )
    print(output)


if __name__ == "__main__":
    main()
