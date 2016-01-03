#!/bin/bash --

# Retrieve input files from IMDb
URLS=(ftp://ftp.fu-berlin.de/pub/misc/movies/database/distributors.list.gz, 
  ftp://ftp.fu-berlin.de/pub/misc/movies/database/directors.list.gz, 
  ftp://ftp.fu-berlin.de/pub/misc/movies/database/actors.list.gz,
  ftp://ftp.fu-berlin.de/pub/misc/movies/database/actresses.list.gz,
  ftp://ftp.fu-berlin.de/pub/misc/movies/database/running-times.list.gz )

curl ftp://ftp.fu-berlin.de/pub/misc/movies/database/distributors.list.gz | gzip -d > distributors.list
curl ftp://ftp.fu-berlin.de/pub/misc/movies/database/directors.list.gz | gzip -d > directors.list
curl ftp://ftp.fu-berlin.de/pub/misc/movies/database/actors.list.gz | gzip -d > actors.list
curl ftp://ftp.fu-berlin.de/pub/misc/movies/database/actresses.list.gz | gzip -d > actresses.list
curl ftp://ftp.fu-berlin.de/pub/misc/movies/database/running-times.list.gz | gzip -d > runtimes.list

# for ((i=0;i<${#URLS[@]};++i)); do
#   curl ${URLS[i]} | gzip -d > ${FILES[i]}
# done

# Parse IMDb's input files
python imdb_parser.py

# Create SQLite database
sqlite3 -batch distributors.db <<"EOF"
DROP TABLE IF EXISTS Films;
DROP TABLE IF EXISTS People;
DROP TABLE IF EXISTS Directs;
DROP TABLE IF EXISTS Appearances;
CREATE TABLE Films (Film_ID integer primary key, Title text, Year integer, Runtime integer, IMDb_Distributor text, Distributor text);
CREATE TABLE People (Person_ID integer, Name text);
CREATE TABLE Directs (Person_ID integer, Film_ID integer);
CREATE TABLE Appearances (Person_ID integer, Film_ID integer);
.separator "|"
.import films.txt Films
.import directors.txt People
.import directs.txt Directs
.import actors.txt People
.import actresses.txt People
.import actor_appears.txt Appearances
.import actress_appears.txt Appearances
UPDATE Films SET Distributor = "Park Circus" WHERE Title = "Stella Dallas";
EOF

# Clean up 
rm *.list
rm *.txt