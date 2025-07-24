from tabulate import tabulate

def create_table(data: dict):
    table = []
    for i, (url, data) in enumerate(data.items()):
        avg = round(data['sum_response_time'] / data['count'], 3)
        table.append([i, url, data['count'], avg])
    sorted_table = sorted(table, key=lambda x: x[2], reverse=True)
    tabulated_table = tabulate(sorted_table, headers=['', 'handler', 'total', 'avg_response_time'])
    return tabulated_table