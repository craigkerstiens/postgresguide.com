Installing Postgres
===================

For Mac
~~~~~~~

brew update
brew install postgresql

Now that its installed lets set it up to initialize a DB and startup:

initdb /usr/local/var/postgres
cp /usr/local/Cellar/postgresql/9.0.1/org.postgresql.postgres.plist ~/Library/LaunchAgents
launchctl load -w ~/Library/LaunchAgents/org.postgresql.postgres.plist
pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start

For Linux
~~~~~~~~~

sudo apt-get install postgresql


Finally lets connect.