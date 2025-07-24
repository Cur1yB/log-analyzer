def main():
    log_analyzer('example2.log')

def log_line_generator(filename):
    with open(filename, 'r') as file:
        for line in file:
            yield line
import json
from collections import defaultdict
def log_analyzer(filename):
    log_gen = log_line_generator(filename)
    response_time = {} # redis?
    while True:
        try:
            line = next(log_gen)
        except StopIteration:
            break
        string_dict = json.loads(line)
        url = string_dict['url']
        # defaultdict?
        if url not in response_time:
            response_time[url] = {
                'sum_response_time': string_dict['response_time'],
                'count': 1
            }
        else:
            response_time[url]['sum_response_time'] += string_dict['response_time']
            response_time[url]['count'] += 1
    for url, data in response_time.items():
        avg = round(data['sum_response_time'] / data['count'], 3)
        print(f'{url} - {avg} - {data["count"]}')
        

if __name__ == "__main__":
    main()
