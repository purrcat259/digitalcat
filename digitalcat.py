import markdown
import os
from flask import Flask, render_template, send_from_directory, Markup

app = Flask(__name__)

article_data = []
project_data = []
cached = False


def cache_texts():
    global cached
    if not cached:
        text_data = []
        for text_type in ['articles', 'projects']:
            path = os.path.join(os.getcwd(), 'static', 'text', text_type)
            files = os.listdir(path=path)
            for file in files:
                file_path = os.path.join(os.getcwd(), 'static', 'text', text_type, file)
                data = dict()
                data['title'] = file.replace('.md', '')
                data['type'] = text_type.replace('s', '')
                data['path'] = file_path
                with open(file_path, mode='r') as textfile:
                    text = textfile.readlines()
                    # Remove the first line and store it as the description
                    data['description'] = text.pop(0).strip()
                    # Store the rest as the contents
                    data['contents'] = ''
                    for line in text:
                        data['contents'] += line
                    # print(data['contents'])
                    text_data.append(data)
                    print('Stored file with name: ' + file)
        global article_data
        article_data = [data for data in text_data if data['type'] == 'article']
        global project_data
        project_data = [data for data in text_data if data['type'] == 'project']
        cached = True


def return_requested_data(data_type='', title=''):
    if data_type == 'article':
        global article_data
        for article in article_data:
            if article['title'] == title:
                return article
    else:
        global project_data
        for project in project_data:
            if project['title'] == title:
                return project
    return dict()


items = [
    {
        'title': 'Hello Friend'
    },
    {
        'title': 'How have you been'
    }
]


@app.route('/')
def index():
    # cache_texts()
    return render_template('list.html', page_title='Digitalcat Homepage', items=items)


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


@app.route('/articles')
def articles():
    global article_data
    return render_template('list.html',
                           page_title='Digitalcat Articles',
                           item_type='article',
                           items=article_data)


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


@app.route('/projects')
def projects():
    global project_data
    return render_template('list.html',
                           page_title='Digitalcat Projects',
                           item_type='project',
                           items=project_data)


@app.route('/project/<title>')
def project(title):
    data = return_requested_data(data_type='project', title=title)
    try:
        text = Markup(markdown.markdown(data['contents']))
    except KeyError:
        text = 'Project found, try another name?'
    return render_template('item.html',
                           title=title,
                           item_type='project',
                           text=text)


if __name__ == '__main__':
    # cache_texts()
    app.run(host='127.0.0.1', port=9000, debug=True)
    # app.run(host='0.0.0.0', port=9000, debug=False)
