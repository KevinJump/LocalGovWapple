LocalGovWapple
==============

A hacked together script, using wappalyzer
- on localgov sites

three scripts 

DbCleanSetup.py
----------------
creates a blank sqlite3 db with all
the councils from councilsites.txt

GetWapple.py
------------
Runs Wappalyzer agains all sites in the db

Wapple_tocsv.py
---------------
Dumps the sqlite db to a csv file, so you
can do stuff like pivot tables in google

At the end you also have a SQLite DB with
all the sites in a sites table

and all the collected features in the features
table, so you could just use the db if you
wanted. 
