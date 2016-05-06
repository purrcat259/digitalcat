import markdown
from flask import Flask, render_template, send_from_directory
from os import listdir, getcwd
from os.path import join as join_path

app = Flask(__name__)


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


# TODO: Rename to articles
@app.route('/thoughts')
def thoughts():
    thoughts_list = []
    # thoughts_list = g.db.execute('SELECT * from items WHERE type = "thought"').fetchall()
    # thoughts_list.reverse()
    return render_template('collection.html',
                           page_title='Written thoughts',
                           item_type='thought',
                           items=thoughts_list)


@app.route('/thought/<int:thought_ref>')
def thought(thought_ref):
    # data = g.db.execute('SELECT * FROM items WHERE reference = "{}" AND type = "thought"'.format(thought_ref)).fetchall()[0]
    # print(data)
    # topic_contents = re.split('\[(.*?)\]', data[6])
    topic_contents = []
    return render_template('item.html',
                           item_type='thought',
                           page_title=data[3],
                           item_contents=topic_contents)


@app.route('/projects')
def projects():
    # projects_list = g.db.execute('SELECT * FROM items WHERE type = "project"').fetchall()
    # projects_list.reverse()
    projects_list = []
    return render_template('collection.html',
                           page_title='Projects',
                           item_type='project',
                           items=projects_list)


# TODO: Use names of markdown files as reference strings rather than ints
@app.route('/project/<int:project_ref>')
def project(project_ref):
    # data = g.db.execute('SELECT * FROM items WHERE reference = "{}" AND type = "project"'.format(project_ref)).fetchall()[0]
    # print(data)
    # project_contents = re.split('\[(.*?)\]', data[6])

    project_contents = []
    return render_template(
        'item.html',
        item_type='project',
        page_title='',
        item_contents=project_contents)

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
    app.run(host='127.0.0.1', port=9000, debug=True)
    # app.run(host='0.0.0.0', port=9000, debug=False)
