Non-Theatrical Film Distribution Database
=========================================

Background
----------

This database uses data from IMDb's alternative text interfaces to determine the non-theatrical film distributors for given titles. This tool is intended to help programmers at Doc Films reduce the time spent manually searching for distributors on IMDb or other websites, and to provide that distribution information in a single resource. 

Usage
-----

The database is currently hosted on OpenShift at http://docfilms-distributiondb.rhcloud.com/. As I'm only using the free hosting service, the app may take a few seconds to load. 

You can search via film title, cast member, or director. For cast members or director, names must be entered exactly as they appear on IMDb (including any punctuation and accent marks).

Searches by title are case insensitive and will match partial titles (i.e. Moonlight will appear as a result for "moon"). To narrow down results, include the year of the film in parentheses afterward (i.e. "moon 2009"). You can also search for multiple films at a time, one title per line.


Based on the OpenShift Flask Quickstart: https://github.com/openshift-quickstart/flask-base
