import logging


# def dict_fetch_all(cursor):
#     columns = [col[0] for col in cursor.description]
#     return [
#         dict(zip(columns, row))
#         for row in cursor.fetchall()
#     ]

def list_of_dicts(list):
    dist = {}
    lists = []
    colume1 = list.columns
    for i in range(len(list)):
        for j in range(len(colume1)):
            dist[colume1[j]] = list[i].id

        lists.append(dist)
        dist = {}
    return lists


def get_max_rows_excel(sheet_object):
    rows = 0
    for max_row, row in enumerate(sheet_object, 1):
        if not all(col.value is None for col in row):
            rows += 1
    return rows