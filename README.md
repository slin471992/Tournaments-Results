Project: Tournament Results  - [Shumei Lin]
================================

Required Libraries and Dependencies
-----------------------------------
Requires Python v2.7 to be installed.
Requires Vagrant VM to be installed.
For information to install and run Vagrant VM, please follow steps on the following webpage:
https://udacity.atlassian.net/wiki/display/BENDH/Vagrant+VM+Installation

How to Run Project
------------------
- Download and unzip the project file.
- Replace files in /fullstack/vagrant/tournament directory with files in the project file.
- Launch Git Bash terminal window, type vagrant ssh to log in.
- From Git Bash, navigate to the project's directory, which should do by typing cd /vagrant/tournament.
- Open psql by typing psql.
- In psql command line create a tournament database by typing CREATE DATABASE tournament.
- Connect to the tournament database by typing \c tournament.
- After successful connection, create tables in the tournament database from the tournament.sql file by typing \i tournament.sql.
- Exit psql by typing \q.
- Run the tournament test file by typing python tournament_test.py in Git Bash.

