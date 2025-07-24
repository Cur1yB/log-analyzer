import json
from collections import defaultdict

def log_line_generator(filename):
    with open(filename, 'r') as file:
        for line in file:
            yield line

def log_analyzer(files: list[str]):
    response_time = defaultdict(lambda: {
        'sum_response_time': 0.0,
        'count': 0
    }) # redis?
    for filename in files:
        log_gen = log_line_generator(filename)
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
    print(json.dumps(dict(response_time), indent=2))
    return response_time
        