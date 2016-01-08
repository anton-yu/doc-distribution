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

def add_films (films):
    infile = open("distributors.list", "r") 

    film_id = 0

    Swank = ["Disney", "Warner", "Columbia", "Weinstein", "MGM", "Miramax", "Paramount", "Focus Features", "Lionsgate", "New Line", "Dreamworks", "RADiUS-TWC", "Tristar", "Metro-Goldwyn-Mayer", "United Artists", "RKO", "Dreamworks", "TriStar", "Sony Pictures Releasing", "Buena Vista"]
    Criterion = ["Fox", "Open Road"]

    for line in infile:
        if line[0] != '"': # skip TV episodes 
            if "(USA)" in line: # TODO: start with subset of films
                if "VHS" in line or "DVD" in line or "SUSPENDED" in line:
                    continue  
                if "theatrical" in line or "all media" in line: 
                    # parse title and year from first open parenthesis (denoting year)
                    index = line.find('(') # find index of opening parenthesis 
                    if line[index+7] is '(' or "(II)" in line[index+7:] or "(VG)" in line or "V)" in line:
                        continue 
                    title = line[0:index-1] # use index to parse title 
                    year = line[index+1:index+5] # use index to parse year
                    if year[0] != '1' and year[0] != '2':
                        continue # TODO: can't be parentheses in film title
                    if line[index+5] == '/':
                        index += 6

                    # parse imdb_distributor
                    rest = line[index+6:].lstrip() 
                    index = rest.find('[')
                    index2 = rest.find('(')
                    if index == -1 or index > index2: # the '[us]' substring doesn't appear or it appears after something like '(III)'
                        imdb_distr = rest[0:index2]
                    else: # use the first index
                        imdb_distr = rest[0:index]

                    if imdb_distr[0:1] == '"':
                        continue
                    imdb_distr = imdb_distr.rstrip();

                    if "Path" in imdb_distr:
                        imdb_distr = "Pathe Freres"

                    distributor = imdb_distr
                    if any(x in distributor for x in Swank):
                        distributor = "Swank"
                    elif any(x in distributor for x in Criterion):
                        distributor = "Criterion"

                    # add new Film object to films dict
                    key = title + year
                    if key in films: # in case of re-releases/updated distributor, go with newest one
                        films.pop(key, None)
                    films[key] = Film(film_id, title, year, imdb_distr, distributor) 
                    film_id += 1

    infile.close()

def add_runtimes (films):
    infile = open("running-times.list", "r") 

    for line in infile:
        if line[0] != '"': # skip TV episodes 
            index = line.find('(') # find index of opening parenthesis      
            title = line[0:index-1] # use index to parse title 
            year = line[index+1:index+5] # use index to parse year
            key = title + year

            index2 = line.find('\t')
            if index2 <= 0:
                continue
            rest = line[index2+1:]
            runtime = filter(lambda x: x.isdigit(), rest)

            if key in films:
                f = films[key]
                if f.runtime != 0:
                    if "USA" not in rest:
                        continue
                f.runtime = runtime

    infile.close()

def update_titles (films):
    infile = open("aka-titles.list", "r")

    title = ""
    year = ""

    for line in infile:
        if line[0] != '"': # skip TV episodes
            if not line[0].isspace():
                index = line.find('(') # find index of opening parenthesis      
                title = line[0:index-1] # use index to parse title 
                year = line[index+1:index+5] # use index to parse year
            else:
                line = line[8:]
                if "International: English title" in line or "USA" in line and "dubbed" not in line:
                    key = title + year
                    if key in films:
                        f = films[key]
                        index = line.find('(')
                        f.title = line[0:index-1] # update new title
                        title = "" # to be safe

    infile.close()

def add_people (films, person_id, input_file, join_table_file, output_file, skip):
    join_file = open(join_table_file, "w")
    outfile = open(output_file, "w")

    with open(input_file) as infile:
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
            elif index > 0: # new director 
                comma = line.find(',')
                person = line[comma+2:index] + " " + line[:comma]
            else:
                index = 2 # 3 tabs before every other film name per person

            # check and append the film
            year_index = line.find('(')
            title = line[index+1:year_index-1]
            year = line[year_index+1:year_index+5] 

            if '"' in title or "(V)" in title or "(VG)" in title or "SUSPENDED" in title:
                continue
            else:
                key = title + year
                if key in films:
                    film = films[key]
                    filmography.append(film)

    infile.close()
    join_file.close()
    outfile.close()

def main():

    films = {} # dict of films, key = title + year, value = object
    person_id = 0

    add_films(films) # parse films from distributors.list
    add_runtimes(films)
    update_titles(films)

    outfile = open("films.txt", "w")
    for key in films:
        f = films[key]
        outfile.write(str(f.id) + "|" + f.title + "|" + f.year + "|" + str(f.runtime) + "|" + f.imdb_distr + "|" + f.distr + '\n')
    outfile.close()

    add_people(films, person_id, "directors.list", "directs.txt", "directors.txt", 235) # parse directors from directors.list
    add_people(films, person_id, "actors.list", "actor_appears.txt", "actors.txt", 239)
    add_people(films, person_id, "actresses.list", "actress_appears.txt", "actresses.txt", 241)

if __name__ == '__main__':
    main()
