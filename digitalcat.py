import os
from flask import Flask, render_template, send_from_directory, Markup

app = Flask(__name__)

articles = [
    {
        'id': 1,
        'title': 'Hello Friend',
        'contents': 'blablabla',
        'url_name': 'hello-friend',
        'timestamp': 1472302423
    },
    {
        'id': 2,
        'title': 'How have you been',
        'contents': 'This is another article',
        'url_name': 'how-have-you-been',
        'timestamp': 1472302430
    }
]


def get_article_data(article_url_name):
    for article in articles:
        if article['url_name'] == article_url_name:
            return article
    # TODO: Return a special case article with no data to forward the route to 404
    return None


@app.route('/')
def index():
    return render_template('article_list.html', page_title='Digitalcat Homepage', articles=articles)


@app.route('/article/<article_url_name>')
def article(article_url_name):
    article = get_article_data(article_url_name=article_url_name)
    return render_template('article.html', page_title='Article', article=article)


@app.route('/contact')
def contact():
    return render_template('contact.html', page_title='Digitalcat Contact')

media_folder = 'assets/'  # TODO: Fold into a config


# TODO: create a get_uploaded_image method that uses this, to keep it separate from serving other assets/images
@app.route('/assets/<path:filename>')
def get_file(filename):
    return send_from_directory(media_folder, filename, as_attachment=True)

"""
@app.route('/article/<title>')
def article(title):
    data = return_requested_data(data_type='article', title=title)
    try:
        text = Markup(markdown.markdown(data['contents']))
    except KeyError:
        text = 'Article not found, try another name?'
    return render_template('item.html',
                           title=title,
                           item_type='article',
                           text=text)
"""

if __name__ == '__main__':
    # cache_texts()
    app.run(host='127.0.0.1', port=9000, debug=True)
    # app.run(host='0.0.0.0', port=9000, debug=False)
