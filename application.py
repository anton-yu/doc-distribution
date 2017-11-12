import sqlite3
from flask import Flask, render_template, request, g

application = Flask(__name__)
application.debug=True

DATABASE = './distributors.db'

@application.before_request
def get_db():
  g.db = sqlite3.connect(DATABASE)

@application.teardown_request
def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
      db.close()

@application.route('/')
def index():
  return render_template('index.html')

@application.route('/', methods=['POST'])
def query():
  base_query = 'SELECT Title, Year, Runtime, IMDb_Distributor, Distributor FROM Films '

  if request.form['inputTitles']:
    titles = request.form['inputTitles'].split('\r\n')
    films = lookup_titles(titles, base_query)
    return render_template('results.html', films = films)  
  elif request.form['inputCast']:
    cast = request.form['inputCast']
    base_query += 'JOIN People JOIN Appearances WHERE People.Person_ID = Appearances.Person_ID AND Films.Film_ID = Appearances.Film_ID AND Name = ? '

    if 'shorts' not in request.form:
      base_query += 'AND Runtime > 55 '

    films = g.db.execute(base_query + 'ORDER BY Year', [cast]).fetchall()     
    return render_template('results.html', person = cast, films = films)
  else:
    director = request.form['inputDirector']
    base_query += 'JOIN People JOIN Directs WHERE People.Person_ID = Directs.Person_ID AND Films.Film_ID = Directs.Film_ID AND Name = ? '
    if 'shorts' not in request.form:
      base_query += 'AND Runtime > 55 '

    films = g.db.execute(base_query + 'ORDER BY Year', [director]).fetchall()
    return render_template('results.html', person = director, films = films)

def lookup_titles(titles, base_query):
  '''Look up titles of the form Title (Optional: Year)'''
  films = []

  for title in titles:
    if title.isspace() or title is "" or not title:
      continue
  
    year_start = title.rfind('(') 
    year_end = title.rfind(')')
    year = ""
    if year_end == len(title) - 1 and year_end - year_start == 5:
      year = title[year_start + 1:year_end]
      query = '%' + title[:year_start - 1] + '%'
    else:
      query = '%' + title + '%'
  
    base_query += 'WHERE Title LIKE ? '
    if 'shorts' not in request.form:
      base_query += 'AND Runtime > 55 '
    if year: 
      base_query += ' AND Year = ?'
      results = g.db.execute(base_query, [query, year]).fetchall()
    else:
      results = g.db.execute(base_query, [query]).fetchall()

    for r in results:
      films.insert(0, r)
      
  return films 

if __name__ == '__main__':
    application.run()
