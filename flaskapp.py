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
      if title.isspace() or title is "" or not title:
        continue
      year_start = title.rfind('(')
      year_end = title.rfind(')')
      year = ""
      if year_start != -1 and year_end != -1 and year_end - year_start == 5:
        year = title[year_start+1:year_end]
        query = '%' + title[:year_start-1] + '%'
      else:
        query = '%' + title + '%'
      if 'shorts' not in request.form:
        if year:
          results = g.db.execute('SELECT Title, Year, Runtime, IMDb_Distributor, Distributor FROM Films WHERE Title LIKE ? AND Year = ? AND Runtime > 55', [query, year]).fetchall()          
        else:
          results = g.db.execute('SELECT Title, Year, Runtime, IMDb_Distributor, Distributor FROM Films WHERE Title LIKE ? AND Runtime > 55', [query]).fetchall()
      else:
        if year:
          results = g.db.execute('SELECT Title, Year, Runtime, IMDb_Distributor, Distributor FROM Films WHERE Title LIKE ? AND Year = ?', [query, year]).fetchall()          
        else:
          results = g.db.execute('SELECT Title, Year, Runtime, IMDb_Distributor, Distributor FROM Films WHERE Title LIKE ?', [query]).fetchall()
      for r in results:
        films.insert(0, r)
    return render_template('results.html', films = films)  
  elif request.form['inputCast']:
    cast = request.form['inputCast']
    # query = '%' + cast + '%'
    # films = g.db.execute('SELECT Name, Title, Year, Runtime, IMDb_Distributor, Distributor FROM Films JOIN People JOIN Appearances WHERE People.Person_ID = Appearances.Person_ID AND Films.Film_ID = Appearances.Film_ID AND Name LIKE ? ORDER BY Year', [query]).fetchall()
    if 'shorts' not in request.form:
      films = g.db.execute('SELECT Title, Year, Runtime, IMDb_Distributor, Distributor FROM Films JOIN People JOIN Appearances WHERE People.Person_ID = Appearances.Person_ID AND Films.Film_ID = Appearances.Film_ID AND Name = ? AND Runtime > 55 ORDER BY Year', [cast]).fetchall()
    else:
      films = g.db.execute('SELECT Title, Year, Runtime, IMDb_Distributor, Distributor FROM Films JOIN People JOIN Appearances WHERE People.Person_ID = Appearances.Person_ID AND Films.Film_ID = Appearances.Film_ID AND Name = ? ORDER BY Year', [cast]).fetchall()      
    return render_template('results.html', person = cast, films = films)
  else:
    director = request.form['inputDirector']
    # query = '%' + director + '%'
    # films = g.db.execute('SELECT Name, Title, Year, Runtime, IMDb_Distributor, Distributor FROM Films JOIN People JOIN Directs WHERE People.Person_ID = Directs.Person_ID AND Films.Film_ID = Directs.Film_ID AND Name LIKE ? ORDER BY Year', [query]).fetchall()
    if 'shorts' not in request.form:
      films = g.db.execute('SELECT Title, Year, Runtime, IMDb_Distributor, Distributor FROM Films JOIN People JOIN Directs WHERE People.Person_ID = Directs.Person_ID AND Films.Film_ID = Directs.Film_ID AND Name = ? AND Runtime > 55 ORDER BY Year', [director]).fetchall()
    else:
      films = g.db.execute('SELECT Title, Year, Runtime, IMDb_Distributor, Distributor FROM Films JOIN People JOIN Directs WHERE People.Person_ID = Directs.Person_ID AND Films.Film_ID = Directs.Film_ID AND Name = ? ORDER BY Year', [director]).fetchall()
    return render_template('results.html', person = director, films = films)

if __name__ == '__main__':
  app.run()
