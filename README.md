Non-Theatrical Film Distribution Database
=========================================

Background
----------

This database uses data from IMDb's alternative text interfaces to determine the non-theatrical film distributors for given titles. This tool is intended to help programmers at Doc Films reduce the time spent manually searching for distributors on IMDb or other websites, and to provide that distribution information in a single resource. 

Update: As of 2017, IMDb has altered its datasets, which no longer include distributors, so no new films will be added for the moment.

Usage
-----

The database is currently hosted on AWS Elastic Beanstalk at http://docdb-dev.us-west-1.elasticbeanstalk.com.  

You can search via film title, cast member, or director. For cast members or director, names must be entered exactly as they appear on IMDb (including any punctuation and accent marks).

Searches by title are case insensitive and will match partial titles (i.e. Moonlight will appear as a result for "moon"). To narrow down results, include the year of the film in parentheses afterward (i.e. "moon 2009"). You can also search for multiple films at a time, one title per line.
