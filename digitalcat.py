import logging
from logging.handlers import RotatingFileHandler
from db import article_database
from flask import Flask, render_template, send_from_directory, redirect, request
from time import time as current_time

app = Flask(__name__)

debug_mode = False
max_page_count = 0
media_folder = 'assets/'  # TODO: Fold into a config
log_path = 'logs/website.log'


def run_setup():
    print('------------------------')
    print('--- Starting website ---')
    if debug_mode:
        print('------ DEBUG MODE ------')
    print('------------------------')
    global max_page_count
    max_page_count = article_database.get_page_count()
    handler = RotatingFileHandler(log_path, maxBytes=1000000, backupCount=2)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)


def log_visit(route_name='', enter_time=0):
    app.logger.info('{},{},{},{}'.format(
        current_time(),
        request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
        route_name,
        current_time() - enter_time
    ))


def get_page_data(current_page):
    return {
        'current_page': current_page,
        'max_page': max_page_count,
        'has_previous': current_page > 1,
        'has_next': current_page < max_page_count
    }


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
@app.route('/<int:page_number>')
def index(page_number=1):
    enter_time = current_time()
    if page_number > max_page_count:
        page_number = max_page_count
    paginated_articles = article_database.get_paginated_articles(page_number)
    log_visit(route_name='index_{}'.format(page_number), enter_time=enter_time)
    return render_template(
        'article_list.html',
        page_title='Digitalcat Homepage',
        articles=paginated_articles,
        page_data=get_page_data(page_number)
    )


@app.route('/article/<article_url_name>')
def article(article_url_name):
    enter_time = current_time()
    try:
        article = article_database.get_specific_article(article_url_name=article_url_name)
    except article_database.ArticleNotFoundException:
        log_visit(route_name='article_404_{}'.format(article_url_name), enter_time=enter_time)
        return redirect('page_not_found')
    log_visit(route_name='article_{}'.format(article_url_name), enter_time=enter_time)
    return render_template('article.html', page_title='Article', article=article)

run_setup()

if __name__ == '__main__':
    if debug_mode:
        app.run(host='127.0.0.1', port=9000, debug=True)
    else:
        app.run(host='0.0.0.0', port=9000, debug=False)
