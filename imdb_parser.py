#!/usr/bin/python

# Information courtesy of
# IMDb
# (http://www.imdb.com).
# Used with permission.

class Film:
  
  def __init__(self, film_id, title, year, imdb_distr, distributor):
    self.id = film_id
    self.title = title
    self.year = year
    self.imdb_distr = imdb_distr
    self.distr = distributor
    self.runtime = 0
    self.updated = False # used in update_title

def parse_key(line):
  '''Parse out the title and year (the key in our films dict)'''
  index = line.find('(')       
  title = line[0:index-1] 
  year = line[index+1:index+5] 
  key = title + year
  return index, title, year, key

def add_films(films):
  '''Parse films and add them into a dict'''
  with open("distributors.list", "r") as infile: 
    film_id = 0
    for line in infile:
      if line[0] != '"': # skip TV episodes 
        to_remove = ["(II)", "(I)", "(VG)", "V)"]
        if any(x in line for x in to_remove):          
          continue 
        
        # parse out the title and year (the key in our films dict)
        index, title, year, key = parse_key(line)
        if year[0] != '1' and year[0] != '2':
          continue # TODO: can't be parentheses in film title

        if line[index+5] == '/':
          index += 6

        if "(USA)" in line and ("theatrical" in line or "all media" in line):
          imdb_distr, distributor = parse_distr(films, key, line, index) 
        else: 
          if key in films:
            continue 

        films[key] = Film(film_id, title, year, imdb_distr, distributor) 
        film_id += 1

def add_runtimes(films):
  with open("running-times.list", "r") as infile: 
    for line in infile:
      if line[0] != '"': # skip TV episodes 
        index, title, year, key = parse_key(line)

        index = line.find('\t') # runtime located after the tab
        if index <= 0:
          continue

        stop = line[index+1:].find('(') + index + 1 # sometimes extraneous info after runtime
        if stop > index + 1:
          rest = line[index+1:stop]
        else:
          rest = line[index+1:]

        runtime = filter(lambda x: x.isdigit(), rest)

        if key in films:
          f = films[key]
          if f.runtime != 0:
            if "USA" not in rest:
              continue
          f.runtime = runtime

def update_titles(films):
  with open("aka-titles.list", "r") as infile: 
    title = ""
    year = ""

    for line in infile:
      if line[0] != '"': # skip TV episodes
        if not line[0].isspace():
          index, title, year, key = parse_key(line)    
        else:
          line = line[8:]
          if "International: English title" in line or "USA" in line:
            filtered = ["dubbed", "working title", "script title", "informal title", "promotional", "alternative title", "complete title"]
            if any(x in line for x in filtered):
              continue 

            key = title + year
            if key in films:
              f = films[key]
              if not f.updated and "UK" in line:
                continue
              else:
                f.updated = True 
              index = line.find('(')
              f.title = line[0:index-1] # update new title

            if "imdb display" in line:
              title = "" # don't overwrite this anymore

def parse_distr(films, key, line, index):
  '''Parse out the imdb_distributor and the correct distributor for us'''
  rest = line[index+6:].lstrip() 

  index = rest.find('[')
  index2 = rest.find('(')
  if index == -1 or index > index2: # the '[us]' substring doesn't appear or it appears after something like '(III)'
    imdb_distr = rest[0:index2]
  else: 
    imdb_distr = rest[0:index]

  if imdb_distr[0:1] == '"':
    return "", ""
  imdb_distr = imdb_distr.rstrip();
  imdb_distr = imdb_distr.decode('cp1252').encode('utf-8')

  distributor = imdb_distr 
  
  Swank = ["Disney", "Warner", "Columbia", "Weinstein", "MGM", "Miramax", "Paramount", "Focus Features", "Lionsgate", "New Line", "Dreamworks", "DreamWorks", "RADiUS-TWC", "Tristar", "Metro-Goldwyn-Mayer", "United Artists", "RKO", "Dreamworks", "TriStar", "Sony Pictures Releasing", "Buena Vista", "Samuel Goldwyn Company", "Selznick", "CBS Films", "Orion Pictures", "Open Road"]
  Criterion = ["Fox"]
  if any(x in distributor for x in Swank):
    distributor = "Swank"
  elif any(x in distributor for x in Criterion):
    distributor = "Criterion Pictures"
  elif "Palisade Tartan" in distributor: 
    distributor = "Kino Lorber"

  # add new Film object to films dict
  if key in films: # in case of re-releases/updated distributor, go with newest one
    films.pop(key, None)

  return imdb_distr, distributor 

def update_distr(films): 
  with open("updates.tsv", "r") as infile, open("output.tsv", "w") as outfile: 
    for line in infile:
      index, title, year, key = parse_key(line)

      rest = line[index+1:]
      index2 = rest.find('|')
      distr = '"' + rest[index2+1:-1] + '"'

      outfile.write("UPDATE Films SET Distributor = %s WHERE Title = %s AND Year = %s;" % (distr, title, year) + '\n')

      if key in films:
        f = films[key]
        f.distr = rest[index2+1:-1]

def add_people(films, person_id, input_file, join_table_file, output_file, skip):
  with open(input_file, "r") as infile, open(output_file, "w") as outfile, open(join_table_file, "w") as join_file:
    for i in xrange(skip):
      infile.next()

    person = " "
    filmography = [] # list of Film objects with person 

    for line in infile:
      index = line.find('\t')

      if index == -1: # empty line, end of current person's list
        if filmography: # add person to outfile db
          outfile.write(str(person_id) + "|" + person + "\n")
        for d in filmography: # current person has films we want to store
          join_file.write(str(person_id) + "|" + str(d.id) + "\n")
        person_id += 1
        filmography = []
        continue
      elif index > 0: # new person 
        comma = line.find(',')
        parenthesis = line.find('(') # e.g. L_NAME, F_NAME (I)
        if parenthesis > 0 and parenthesis < index:
          index -= 4
        person = line[comma+2:index] + " " + line[:comma]
        person = person.decode('cp1252').encode('utf-8')
      else:
        index = 2 # 3 tabs before every other film name per person

      # check and append the film
      year_index, title, year, key = parse_key(line)

      if '"' in title or "(V)" in title or "(VG)" in title or "SUSPENDED" in title:
        continue
      else:
        if key in films:
          film = films[key]
          filmography.append(film)

def main():

  films = {} # dict of films, key = title + year, value = object
  person_id = 0

  add_films(films) # parse films from distributors.list
  add_runtimes(films)
  update_titles(films)

  with open("films.txt", "w") as outfile:
    for key in films:
      f = films[key]
      f.title = f.title.decode('cp1252').encode('utf-8')
      outfile.write(str(f.id) + "|" + f.title + "|" + f.year + "|" + str(f.runtime) + "|" + f.imdb_distr + "|" + f.distr + '\n')

  add_people(films, person_id, "directors.list", "directs.txt", "directors.txt", 235) # parse directors from directors.list
  add_people(films, person_id, "actors.list", "actor_appears.txt", "actors.txt", 239)
  add_people(films, person_id, "actresses.list", "actress_appears.txt", "actresses.txt", 241)

if __name__ == '__main__':
    main()
