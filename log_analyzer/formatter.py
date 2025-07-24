from tabulate import tabulate
from typing import Union, List

HEADERS_TABLE_MAPPER = {
    'average': ['', 'handler', 'total', 'avg_response_time'],
    # if need to add another headers for another analizes, add it here
}

class Output:
    
    @staticmethod
    def create_table(table: List[Union[int, str, float]], sort_by: int = 1, report_name:str = 'average'):
        '''
        Create table view, it's universal

        :param table: list of lists, each list is a row
        :param sort_by: int - index of column to sort by (excluding the column with number of row)
        :param headers: list of str - headers of table (default is None for response time)

        :return: str - it's a table
        '''
        sorted_table = sorted(table, key=lambda x: x[sort_by], reverse=True)
        
        tabulated_table = tabulate(sorted_table, headers=HEADERS_TABLE_MAPPER.get(report_name), showindex=True)
        return tabulated_table

REPORT_FORMATTERS_MAPPER = {
    'average': Output.create_table,
    # You can add more report formaters here
}