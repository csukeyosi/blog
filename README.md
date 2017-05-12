# Tournament
A Python module that uses the PostgreSQL database to keep track of players and matches in a game tournament.

Prerequisites
-------------
1. Python
2. psycopg2
2. PostgreSQL

How to Build Up the Database
-----------------------------
Log into the PostgreSQL from the command line: `psql`.

Use the command `\i tournament.sql` to import the whole file into psql at once. 

Log out from PostgreSQL `\q`.

How to Run the Test Cases
-------------------------
After building up the database, use the command `python tournament_test.py` to run the test cases.
