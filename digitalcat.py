import os
from flask import Flask, render_template, send_from_directory, Markup

app = Flask(__name__)

items = [
    {
        'title': 'Hello Friend',
        'contents': 'blablabla',
        'time_submitted': 1472302423
    },
    {
        'title': 'How have you been',
        'contents': 'This is another article',
        'time_submitted': 1472302430
    }
]


@app.route('/')
def index():
    return render_template('article_list.html', page_title='Digitalcat Homepage', items=items)


@app.route('/contact')
def contact():
    return render_template('contact.html', page_title='Digitalcat Contact')


@app.route('/', subdomain='test')
def test():
    return 'test'


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
