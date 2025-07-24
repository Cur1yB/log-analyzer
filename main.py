def main():
    log_analyzer('example1.log')

def log_line_generator(filename):
    with open(filename, 'r') as file:
        for line in file:
            yield line
import json
from collections import defaultdict
def log_analyzer(filename):
    log_gen = log_line_generator(filename)
    response_time = defaultdict(lambda: {
        'sum_response_time': 0.0,
        'count': 0
    }) # redis?
    while True:
        try:
            line = next(log_gen)
        except StopIteration:
            break
        
        string_dict = json.loads(line)
        url = string_dict['url']
        time = float(string_dict['response_time'])

        response_time[url]['sum_response_time'] += time
        response_time[url]['count'] += 1
    
    for number, (url, data) in enumerate(response_time.items()):
        avg = round(data['sum_response_time'] / data['count'], 3)
        print(f'{number}. {url} - {data["count"]} - {avg}')
        

if __name__ == "__main__":
    main()
