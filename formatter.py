from tabulate import tabulate
from typing import Union, List


class Output:
    @staticmethod
    def create_table(table: List[Union[int, str, float]], sort_by: int = 1, headers=None):
        '''
        Create table view, it's universal

        :param table: list of lists, each list is a row
        :param sort_by: int - index of column to sort by (excluding the column with number of row)
        :param headers: list of str - headers of table (default is None for response time)

        :return: str - it's a table
        '''
        if not headers:
            headers = ['', 'handler', 'total', 'avg_response_time']
        sorted_table = sorted(table, key=lambda x: x[sort_by], reverse=True)
        # add number of row
        for i, row in enumerate(sorted_table):
            row.insert(0, i)
        # Mmm... so much curry there
 
        tabulated_table = tabulate(sorted_table, headers=headers)
        return tabulated_table
