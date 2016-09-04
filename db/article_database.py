import os
from neopysqlite.neopysqlite import Pysqlite

db_path = os.path.join(os.getcwd(), 'db', 'articles.db')


class ArticleNotFoundException(Exception):
    pass


def convert_db_row_to_dict(db_row):
    return {
        'id': db_row[0],
        'title': db_row[1],
        'contents': db_row[2],
        'url_name': db_row[3],
        'timestamp': db_row[4]
    }


def get_all_articles():
    db = Pysqlite(database_name='Articles Database', database_file=db_path)
    all_rows = db.get_specific_rows(table='articles', filter_string='id IS NOT NULL ORDER BY submit_timestamp')
    converted_rows = [
        convert_db_row_to_dict(row) for row in all_rows
    ]
    return converted_rows


def get_specific_article(article_url_name):
    db = Pysqlite(database_name='Articles Database', database_file=db_path)
    row = db.get_specific_rows(
            table='articles',
            filter_string='url_name == "{}"'.format(article_url_name))
    # handle not finding an article
    if not row:
        raise ArticleNotFoundException
    return convert_db_row_to_dict(row[0])

