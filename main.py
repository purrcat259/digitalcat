import sqlite3
import re
import website_config
from flask import Flask, render_template, send_from_directory, g, request, redirect, url_for, flash
from flask_basicauth import BasicAuth
from forms import ItemForm
from os import listdir, getcwd
from os.path import join as join_path

app = Flask(__name__)
app.secret_key = website_config.SECRET_KEY
app.config['BASIC_AUTH_USERNAME'] = 'root'
app.config['BASIC_AUTH_PASSWORD'] = website_config.ROOT_PASSWORD

basic_auth = BasicAuth(app)


@app.before_request
def before_request():
    g.db = sqlite3.connect('db/digitalcat.db')


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/')
def index():
    return render_template('index.html', page_title='Index')


@app.route('/admin')
@basic_auth.required
def admin():
    current_items = g.db.execute('SELECT * from items').fetchall()
    return render_template('admin.html',
                           items=current_items)


@app.route('/admin/submit', methods=['GET', 'POST'])
@basic_auth.required
def submit():
    form = ItemForm(request.form)
    if request.method == 'POST':
        """
        print('Submitted data:\n{}\n{}\n{}\n{}\n{}\n{}'.format(
            form.title.data,
            form.description.data,
            form.image.data,
            form.content.data,
            form.item_type.data,
            form.publish.data,
        ))
        """
        # Temporary validation:
        data = [
            form.title.data,
            form.description.data,
            form.image.data,
            form.content.data,
            form.item_type.data,
            form.publish.data,
        ]
        valid = True
        for item in data:
            if item is None or len(item) == 0:
                valid = False
        if valid:
            try:
                reference = g.db.execute('SELECT * FROM items WHERE type = "{}"'.format(form.item_type.data)).fetchall()[-1]
                reference = int(reference[1]) + 1
                published = 0
                if form.publish.data:
                    published = 1
                g.db.execute('INSERT INTO items VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)', (
                    reference,
                    form.item_type.data,
                    form.title.data,
                    form.description.data,
                    form.image.data,
                    form.content.data,
                    published
                ))
                g.db.commit()
            except Exception as e:
                print('DB Error: {}'.format(e))
                flash('DB Error: {}'.format(e))
                return redirect(url_for('submit'))
            else:
                flash('Form successfully posted')
                return redirect(url_for('admin'))
        else:
            flash('All fields are required')
            return render_template('submit.html', form=form)
    elif request.method == 'GET':
        return render_template('submit.html', form=form)


@app.route('/admin/delete/<item_type>/<int:item_ref>')
@basic_auth.required
def delete_item(item_type, item_ref):
    print('Deleted item: Type: {} Ref: {}'.format(item_type, item_ref))
    g.db.execute('DELETE FROM items WHERE `type` = ? AND `reference` = ?', (item_type, item_ref))
    g.db.commit()
    return redirect(url_for('admin'))

media_folder = 'assets/'  # TODO: Fold into a config


# TODO: create a get_uploaded_image method that uses this, to keep it separate from serving other assets/images
@app.route('/assets/<path:filename>')
def get_file(filename):
    return send_from_directory(media_folder, filename, as_attachment=True)


@app.route('/thoughts')
def thoughts():
    thoughts_list = g.db.execute('SELECT * from items WHERE type = "thought"').fetchall()
    thoughts_list.reverse()
    return render_template('collection.html',
                           page_title='Written thoughts',
                           item_type='thought',
                           items=thoughts_list)


@app.route('/thought/<int:thought_ref>')
def thought(thought_ref):
    data = g.db.execute('SELECT * FROM items WHERE reference = "{}" AND type = "thought"'.format(thought_ref)).fetchall()[0]
    # print(data)
    topic_contents = re.split('\[(.*?)\]', data[6])
    return render_template('item.html',
                           item_type='thought',
                           page_title=data[3],
                           item_contents=topic_contents)


@app.route('/projects')
def projects():
    projects_list = g.db.execute('SELECT * FROM items WHERE type = "project"').fetchall()
    projects_list.reverse()
    return render_template('collection.html',
                           page_title='Projects',
                           item_type='project',
                           items=projects_list)


@app.route('/project/<int:project_ref>')
def project(project_ref):
    data = g.db.execute('SELECT * FROM items WHERE reference = "{}" AND type = "project"'.format(project_ref)).fetchall()[0]
    # print(data)
    project_contents = re.split('\[(.*?)\]', data[6])
    return render_template(
        'item.html',
        item_type='project',
        page_title=data[3],
        item_contents=project_contents)


# API related routes below here
@app.route('/charity')
def charity():
    charity_dir = getcwd() + '/assets/charity'
    charity_files = listdir(charity_dir)
    streamers_available = [streamer.strip('.txt') for streamer in charity_files]
    return render_template(
        'charity.html',
        page_title='Twitch charity stream donations API',
        end_points=streamers_available)


@app.route('/charity/<streamer_required>')
def return_donation_amount(streamer_required):
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
        marquee=False)


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
    print(donation_amount)
    return_string = 'Donations raised: £{} Donation Goal: £{} Percentage Complete: {}%'.format(donation_amount[0], donation_amount[1], donation_amount[2])
    return render_template(
        'donation_api.html',
        streamer=streamer_required,
        amount=return_string,
        marquee=True)

if __name__ == '__main__':
    app.run(debug=True)
