#!/bin/bash --

# Example file 

sqlite3 -batch distributors.db <<"EOF"
UPDATE People SET Name = "Charlie Chaplin" WHERE Name = "Charles Chaplin";
EOF
