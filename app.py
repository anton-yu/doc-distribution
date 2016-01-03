#!/usr/bin/python

import sqlite3
from flask import Flask, render_template, json, request, g
app = Flask(__name__)

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
  if request.form['inputTitle']:
    title = request.form['inputTitle']
    # sql = "select * from films where title like '%"+title+"%'"
    # films = g.db.execute(sql).fetchall()
    films = g.db.execute('SELECT * FROM Films WHERE Title = ?', [title]).fetchall()
    return render_template('index.html', films = films)
  elif request.form['inputCast']:
    cast = request.form['inputCast']
    films = g.db.execute('SELECT Name, Title, Year, Runtime, IMDb_Distributor, Distributor FROM Films JOIN People JOIN Appearances WHERE People.Person_ID = Appearances.Person_ID AND Films.Film_ID = Appearances.Film_ID AND Name = ? ORDER BY Year', [cast]).fetchall()
    return render_template('index.html', person = cast, films = films)
  else:
    director = request.form['inputDirector']
    films = g.db.execute('SELECT Name, Title, Year, Runtime, IMDb_Distributor, Distributor FROM Films JOIN People JOIN Directs WHERE People.Person_ID = Directs.Person_ID AND Films.Film_ID = Directs.Film_ID AND Name = ? ORDER BY Year', [director]).fetchall()
    return render_template('index.html', person = director, films = films)

if __name__ == '__main__':
  app.run()
