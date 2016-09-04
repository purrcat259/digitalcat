import os
from neopysqlite.neopysqlite import Pysqlite
from math import ceil

db_path = os.path.join(os.getcwd(), 'db', 'articles.db')

articles_per_page = 5


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


def get_page_count():
    db = Pysqlite(database_name='Articles Database', database_file=db_path)
    all_rows = db.get_all_rows(table='articles')
    article_count = len(all_rows)
    total_page_count = int(ceil(article_count / float(articles_per_page)))
    print('Article count: {}'.format(len(all_rows)))
    print('Articles per page: {}'.format(articles_per_page))
    print('Maximum number of pages: {}'.format(total_page_count))
    return total_page_count


def get_all_articles():
    db = Pysqlite(database_name='Articles Database', database_file=db_path)
    all_rows = db.get_specific_rows(table='articles', filter_string='id IS NOT NULL ORDER BY submit_timestamp DESC')
    converted_rows = [
        convert_db_row_to_dict(row) for row in all_rows
    ]
    return converted_rows


def get_paginated_articles(page_number):
    db = Pysqlite(database_name='Articles Database', database_file=db_path)
    page_indices = {
        'lower': abs((page_number - 1) * articles_per_page + 1),
        'upper': abs((page_number - 1) * articles_per_page + (articles_per_page - 1) + 1)
    }
    paginated_articles = db.get_specific_rows(
        table='articles',
        filter_string='id >= {} AND id <= {} ORDER BY submit_timestamp DESC'.format(
            page_indices['lower'],
            page_indices['upper']
        )
    )
    converted_rows = [
        convert_db_row_to_dict(row) for row in paginated_articles
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

