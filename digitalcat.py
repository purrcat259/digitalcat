from db import article_database
from flask import Flask, render_template, send_from_directory, redirect

app = Flask(__name__)

debug_mode = True
max_page_count = 0
media_folder = 'assets/'  # TODO: Fold into a config


def run_setup():
    print('------------------------')
    print('--- Starting website ---')
    if debug_mode:
        print('------ DEBUG MODE ------')
    print('------------------------')
    global max_page_count
    max_page_count = article_database.get_page_count()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
@app.route('/<int:page_number>')
def index(page_number=1):
    if page_number > max_page_count:
        page_number = max_page_count
    paginated_articles = article_database.get_paginated_articles(page_number)
    return render_template('article_list.html', page_title='Digitalcat Homepage', articles=paginated_articles)


@app.route('/article/<article_url_name>')
def article(article_url_name):
    try:
        article = article_database.get_specific_article(article_url_name=article_url_name)
    except article_database.ArticleNotFoundException:
        return redirect('page_not_found')
    return render_template('article.html', page_title='Article', article=article)


@app.route('/contact')
def contact():
    return render_template('contact.html', page_title='Digitalcat Contact')


# TODO: create a get_uploaded_image method that uses this, to keep it separate from serving other assets/images
@app.route('/assets/<path:filename>')
def get_file(filename):
    return send_from_directory(media_folder, filename, as_attachment=True)


if __name__ == '__main__':
    run_setup()
    if debug_mode:
        app.run(host='127.0.0.1', port=9000, debug=True)
    else:
        app.run(host='0.0.0.0', port=9000, debug=False)
