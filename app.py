from flask import Flask, request, jsonify, redirect, render_template
import sqlite3
import os
import random
import string

# initialize app, and configure the database
app = Flask(__name__)
app.config['DATABASE'] = os.path.join(os.getcwd(), 'urls.db')

# helper method for creating short_code for the shortened_url and inserting into database (urls)
def create_shortened_url(long_url):
    short_code = ''.join(random.choice(string.digits) for _ in range(4))

    db = sqlite3.connect(app.config['DATABASE'])
    cursor = db.cursor()
    cursor.execute('INSERT INTO urls (long_url, short_code) VALUES (?, ?)', (long_url, short_code))
    db.commit()
    db.close()

    return short_code

# helper method to get long_url from database that matches the short_url after changing to short_url to redirect.
def get_long_url(short_code):
    db = sqlite3.connect(app.config['DATABASE'])
    cursor = db.cursor()
    cursor.execute('SELECT long_url FROM urls WHERE short_code = ?', (short_code,))
    result = cursor.fetchone()
    db.close()

    if result:
        return result[0]
    else:
        return None

# helper method to get all the urls from the database
def get_all_urls():
    db = sqlite3.connect(app.config['DATABASE'])
    cursor = db.cursor()
    cursor.execute('SELECT * FROM urls')
    urls = cursor.fetchall()
    db.close()
    json_urls = []
    for row in urls:
        json_urls.append({'long_url': row[1], 'short_url': f'http://{request.host}/{row[2]}'})
    return json_urls

# route for local host link to start up the url conversion.
@app.route('/')
def index():
    return render_template('index.html')

# route to shortern the url given a long_url in request body.
@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data.get('long_url')
    short_code = create_shortened_url(long_url)

    return jsonify({'short_url': f'http://{request.host}/{short_code}'})

# route to redirect short_url to a long_url.
@app.route('/<short_code>')
def redirect_to_original(short_code):
    long_url = get_long_url(short_code)

    if long_url is not None:
        return redirect(long_url, code=302)
    else:
        return jsonify({'error': 'Short URL not found'}), 404
    
# route to turn the list of urls into a json format.
@app.route('/list', methods=['GET'])
def list_all_urls():
    urls = get_all_urls()
    return jsonify({'urls': urls})

if __name__ == '__main__':
    app.run(debug=True)