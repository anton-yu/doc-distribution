import sqlite3
from flask import Flask, render_template, json, request, g
app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')

DATABASE = './distributors.db'

@app.before_request
def get_db():
  g.db = sqlite3.connect(DATABASE)

@app.teardown_request
def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
      db.close()

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/', methods=['POST'])
def title_query():
  if request.form['inputTitles']:
    titles = request.form['inputTitles'].split('\r\n')
    films = []
    for title in titles:
      print title
      query = '%' + title + '%'
      if 'shorts' not in request.form:
        results = g.db.execute('SELECT * FROM Films WHERE Title LIKE ? AND Runtime > 55', [query]).fetchall()
      else:
        results = g.db.execute('SELECT * FROM Films WHERE Title LIKE ?', [query]).fetchall()
      for r in results:
        films.insert(0, r)
    return render_template('index.html', films = films, show = 'true')  
  elif request.form['inputCast']:
    cast = request.form['inputCast']
    # query = '%' + cast + '%'
    # films = g.db.execute('SELECT Name, Title, Year, Runtime, IMDb_Distributor, Distributor FROM Films JOIN People JOIN Appearances WHERE People.Person_ID = Appearances.Person_ID AND Films.Film_ID = Appearances.Film_ID AND Name LIKE ? ORDER BY Year', [query]).fetchall()
    if 'shorts' not in request.form:
      films = g.db.execute('SELECT Name, Title, Year, Runtime, IMDb_Distributor, Distributor FROM Films JOIN People JOIN Appearances WHERE People.Person_ID = Appearances.Person_ID AND Films.Film_ID = Appearances.Film_ID AND Name = ? AND Runtime > 55 ORDER BY Year', [cast]).fetchall()
    else:
      films = g.db.execute('SELECT Name, Title, Year, Runtime, IMDb_Distributor, Distributor FROM Films JOIN People JOIN Appearances WHERE People.Person_ID = Appearances.Person_ID AND Films.Film_ID = Appearances.Film_ID AND Name = ? ORDER BY Year', [cast]).fetchall()      
    return render_template('index.html', person = cast, films = films, show = 'true')
  else:
    director = request.form['inputDirector']
    # query = '%' + director + '%'
    # films = g.db.execute('SELECT Name, Title, Year, Runtime, IMDb_Distributor, Distributor FROM Films JOIN People JOIN Directs WHERE People.Person_ID = Directs.Person_ID AND Films.Film_ID = Directs.Film_ID AND Name LIKE ? ORDER BY Year', [query]).fetchall()
    if 'shorts' not in request.form:
      films = g.db.execute('SELECT Name, Title, Year, Runtime, IMDb_Distributor, Distributor FROM Films JOIN People JOIN Directs WHERE People.Person_ID = Directs.Person_ID AND Films.Film_ID = Directs.Film_ID AND Name = ? AND Runtime > 55 ORDER BY Year', [director]).fetchall()
    else:
      films = g.db.execute('SELECT Name, Title, Year, Runtime, IMDb_Distributor, Distributor FROM Films JOIN People JOIN Directs WHERE People.Person_ID = Directs.Person_ID AND Films.Film_ID = Directs.Film_ID AND Name = ? ORDER BY Year', [director]).fetchall()
    return render_template('index.html', person = director, films = films, show = 'true')

if __name__ == '__main__':
  app.run()
