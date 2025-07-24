import json
from collections import defaultdict
from typing import Union, Generator, List


class Analyzer:
    def __init__(self):
        self.REPORT_MAPPER = {
            'response_time': {
                'processor': self.get_response_time,
                'crude': defaultdict(lambda: {'sum_response_time': 0, 'count': 0}), # it's format for crude data
                'table': self.make_table_response_time,
            },
            # Here you can add more analizes
        }
    
    def row_generator(self, filename: str) -> Generator:
        '''
        Return generator with lines for O(1) memory usage

        :param filename: str - path to file
        '''
        with open(filename, 'r') as file:
            for line in file:
                yield line

    def analyze_rows(self, files:List[str], processor_name: str = 'response_time') -> List[List[Union[int, str, float]]]:
        '''
        Universal function for analyze logs

        :param files: List[str] - list of files for analyze
        :param processor_name: str - name of analizer

        :return: List[List[Union[int, str, float]]] - list of lists with data for table
        '''
        processor = self.REPORT_MAPPER[processor_name]['processor']
        base_crud_dict = self.REPORT_MAPPER[processor_name]['crude']
        for filename in files:
            log_gen = self.row_generator(filename)
            while True:
                try:
                    line = next(log_gen)
                except StopIteration:
                    break
                line_dict = json.loads(line)
                
                processor(line_dict, base_crud_dict)
        table_view = self.REPORT_MAPPER[processor_name]['table'](base_crud_dict)
        return table_view
    
    def get_response_time(self, line: dict[str, Union[str, int, float]], crude: dict[str, Union[str, int, float]]) -> None:
        '''
        Analyzer for response time

        :param line: dict[str, Union[str, int, float]] - dict with data from log
        '''
        url = line['url']
        time = float(line['response_time'])

        crude[url]['sum_response_time'] += time
        crude[url]['count'] += 1

    def make_table_response_time(self, crude: dict[str, Union[str, int, float]]):
        '''
        Make table for response time

        :param crude: dict[str, Union[str, int, float]] - dict with data for analyze

        :return: List[List[Union[int, str, float]]] - list of lists with data for table
        '''
        result = []
        for url, response_time in crude.items():
            avg = round(response_time['sum_response_time'] / response_time['count'], 3)
            result.append([url, response_time['count'], avg])
        return result