import os
from neopysqlite.neopysqlite import Pysqlite

db_path = os.path.join(os.getcwd(), 'db', 'articles.db')

db = Pysqlite(database_name='Articles Database', database_file=db_path)


def convert_db_row_to_dict(db_row):
    return {
        'id': db_row[0],
        'title': db_row[1],
        'contents': db_row[2],
        'url_name': db_row[3],
        'timestamp': db_row[4]
    }


def get_all_articles():
    all_rows = db.get_all_rows(table='articles')
    converted_rows = [
        convert_db_row_to_dict(row) for row in all_rows
    ]
    return converted_rows
