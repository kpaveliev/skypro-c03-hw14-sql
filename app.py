from flask import Flask, render_template, request, jsonify
from dao import NetflixDAO

# Initiate Flask app, load config and DAO
app = Flask(__name__)
app.config.from_pyfile('config.py')
db = NetflixDAO(app.config.get('DB_NETFLIX'))


# View functions for interactive version (optional)
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/movie/')
def title_index():
    title = request.args.get('s')
    query_result = db.get_title(title)
    return render_template('list.html', film=query_result)


# View functions API
@app.route('/movie/<title>')
def title(title):
    query_result = db.get_title(title)
    return query_result


@app.route('/movie/<int:year_from>/to/<int:year_to>')
def titles_years(year_from, year_to):
    query_result = db.get_titles_for_years(year_from, year_to)
    return jsonify(query_result)


@app.route('/rating/<group>')
def titles_group(group):
    query_result = db.get_titles_for_group(group)
    return jsonify(query_result)


@app.route('/genre/<genre>')
def titles_genre(genre):
    query_result = db.get_titles_for_genre(genre)
    return jsonify(query_result)


# Start app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

