import markdown
import os
from flask import Flask, render_template, send_from_directory, Markup

app = Flask(__name__)

article_data = []
project_data = []


def cache_texts():
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
    global article_data
    article_data = [data for data in text_data if data['type'] == 'article']
    global project_data
    project_data = [data for data in text_data if data['type'] == 'project']


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


@app.route('/')
def index():
    return render_template('index.html', page_title='Index')


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
    article_names = [art['title'] for art in article_data]
    return render_template('list.html',
                           title='Articles',
                           item_type='article',
                           items=article_names)


@app.route('/article/<title>')
def article(title):
    contents = return_requested_data(data_type='article', title=title)
    return render_template('item.html',
                           title=title,
                           item_type='article',
                           contents=contents)


@app.route('/projects')
def projects():
    global project_data
    return render_template('list.html',
                           title='Projects',
                           item_type='project',
                           items=project_data)


@app.route('/project/<title>')
def project(title):
    data = return_requested_data(data_type='project', title=title)
    text = Markup(markdown.markdown(data['contents']))
    return render_template('item.html',
                           title=title,
                           item_type='project',
                           text=text)


@app.route('/contact')
def contact():
    return 'test'

"""
# @basic_auth.required
# API related routes below here
@app.route('/charity')
def charity():
    charity_dir = getcwd() + '/assets/charity'
    charity_files = listdir(charity_dir)
    streamers_available = [streamer.replace('.txt', '') for streamer in charity_files]
    return render_template(
        'charity.html',
        page_title='Twitch charity stream donations API',
        end_points=streamers_available)


@app.route('/charity/gameblast')
def return_gameblast_total():
    gameblast_file = getcwd() + '/assets/charity/gameblast.txt'
    try:
        with open(gameblast_file, 'r') as file:
            donation_amount = file.readline()
    except FileNotFoundError:
        return 'API ERROR: FNF'
    donation_amount = '£' + donation_amount
    return render_template(
        'donation_api.html',
        streamer='Gameblast16',
        amount=donation_amount,
        marquee=False,
        gameblast=True)


@app.route('/charity/<streamer_required>')
def return_donation_amounts(streamer_required):
    charity_dir = getcwd() + '/assets/charity'
    charity_files = listdir(charity_dir)
    # Get only the names of the streamers. Files should called name.txt
    streamers_available = [streamer[:len(streamer) - 4] for streamer in charity_files]  # remove the .txt without strip
    if streamer_required not in streamers_available:
        return 'API ERROR: Streamer endpoint not available'
    try:
        # re-append the .txt to access the file
        with open(join_path(charity_dir, streamer_required + '.txt'), 'r') as file:
            donation_amount = file.readline().split(' ')
    except FileNotFoundError:
        return 'API ERROR: File could not be opened'
    return_string = '£{} / £{} {}%'.format(donation_amount[0], donation_amount[1], donation_amount[2])
    return render_template(
        'donation_api.html',
        streamer=streamer_required,
        amount=return_string,
        marquee=False,
        gameblast=False)


@app.route('/charity/<streamer_required>/total')
def return_donation_amount_total(streamer_required):
    charity_dir = getcwd() + '/assets/charity'
    charity_files = listdir(charity_dir)
    # Get only the names of the streamers. Files should called name.txt
    streamers_available = [streamer[:len(streamer) - 4] for streamer in charity_files]  # remove the .txt without strip
    if streamer_required not in streamers_available:
        return 'API ERROR: Streamer endpoint not available'
    try:
        # re-append the .txt to access the file
        with open(join_path(charity_dir, streamer_required + '.txt'), 'r') as file:
            donation_amount = file.readline().split(' ')
    except FileNotFoundError:
        return 'API ERROR: File could not be opened'
    return_string = '£{}'.format(donation_amount[0])
    return render_template(
        'donation_api.html',
        streamer=streamer_required,
        amount=return_string,
        marquee=False,
        gameblast=False)


@app.route('/charity/<streamer_required>/marquee')
def return_donation_amount_marquee(streamer_required):
    charity_dir = getcwd() + '/assets/charity'
    charity_files = listdir(charity_dir)
    # Get only the names of the streamers. Files should called name.txt
    streamers_available = [streamer[:len(streamer) - 4] for streamer in charity_files]  # remove the .txt without strip
    if streamer_required not in streamers_available:
        return 'API ERROR: Streamer endpoint not available'
    try:
        # re-append the .txt to access the file
        with open(join_path(charity_dir, streamer_required + '.txt'), 'r') as file:
            donation_amount = file.readline().split(' ')
    except FileNotFoundError:
        return 'API ERROR: File could not be opened'
    return_string = 'Donations raised: £{} Donation Goal: £{} Percentage Complete: {}%'.format(donation_amount[0], donation_amount[1], donation_amount[2])
    return render_template(
        'donation_api.html',
        streamer=streamer_required,
        amount=return_string,
        marquee=True,
        gameblast=False)


# W: 1300, H: 500
@app.route('/charity/<streamer_required>/text')
def return_donation_amount_text(streamer_required):
    charity_dir = getcwd() + '/assets/charity'
    charity_files = listdir(charity_dir)
    # Get only the names of the streamers. Files should called name.txt
    streamers_available = [streamer[:len(streamer) - 4] for streamer in charity_files]  # remove the .txt without strip
    if streamer_required not in streamers_available:
        return 'API ERROR: Streamer endpoint not available'
    try:
        # re-append the .txt to access the file
        with open(join_path(charity_dir, streamer_required + '.txt'), 'r') as file:
            donation_amount = file.readline().split(' ')
    except FileNotFoundError:
        return 'API ERROR: File could not be opened'
    return_string = 'Amount raised: £{} Goal: £{} Goal completion: {}%'.format(donation_amount[0], donation_amount[1], donation_amount[2])
    return render_template(
        'donation_api.html',
        streamer=streamer_required,
        amount=return_string,
        marquee=False,
        gameblast=False)
"""


if __name__ == '__main__':
    cache_texts()
    app.run(host='127.0.0.1', port=9000, debug=True)
    # app.run(host='0.0.0.0', port=9000, debug=False)
