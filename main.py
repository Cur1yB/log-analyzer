from analizer import Analyzer
from parser import parse_args
from formatter import Output

def main():
    file, report_name, date = parse_args()
    files = file.split(' ')
    analizer = Analyzer()
    data = analizer.analyze_rows(files)
    # if need other formats (plain, html, csv etc.), there you can add mapper
    output = Output.create_table(data)
    print(output)




if __name__ == "__main__":
    main()
