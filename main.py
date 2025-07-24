from analizer import log_analyzer
from parser import parse_args
from tabulator import create_table
from tabulate import tabulate

def main():
    file, report_name, date = parse_args()
    files = file.split(' ')
    id = 0
    data = log_analyzer(files)
    table = create_table(data)
    print(table)




if __name__ == "__main__":
    main()
