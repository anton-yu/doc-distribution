A non-theatrical film distribution database, using data from IMDb's alternative text interfaces. This database is intended to help cut down on time spent by programmers at Doc Films on manually searching for distributors in IMDb. 

The database is hosted on OpenShift at http://docfilms-distributiondb.rhcloud.com/. As OpenShift is a free hosting service, the app may take a few seconds to load. 

You can search via film title, cast member, or director. For cast members or director, names must be entered exactly as they appear on IMDb (including any punctuation and accent marks).

When searching by title, you can look for multiple films by entering one title per line. You can also search using just part of a title, but any film title containing the input text will be matched. To narrow down results, include the year of the film: i.e. TITLE (YEAR), with the parentheses and space between TITLE and YEAR required.

To Run Locally:

1. Import from IMDb: ./import.sh

2. Optional: Apply any updates to the database

3. python app.py

4. Go to localhost:8080 in your web browser

Based on the OpenShift Flask Quickstart: https://github.com/openshift-quickstart/flask-base
