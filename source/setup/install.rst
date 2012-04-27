Installing Postgres
===================

For Mac
-------

`Homebrew <http://mxcl.github.com/homebrew/>`_ is a simple package manager for
Mac. If you are using a different package manager, please follow its
documentation to install Postgres.

::

    brew install postgresql

Homebrew does not start postgres for you (or create a database). As such, it
provides some instructions after installation which is available below and by
running ``brew info postgresql``.

::

    # Create the database cluster
    initdb /usr/local/var/postgres
    # Start postgres
    pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start
    # Set postgres to start on boot
    cp /usr/local/Cellar/postgresql/9.0.1/org.postgresql.postgres.plist ~/Library/LaunchAgents
    launchctl load -w ~/Library/LaunchAgents/org.postgresql.postgres.plist

For Linux
---------

Here are installation commands for various linux distributions:

* Ubuntu/Debian: ``sudo apt-get install postgresql``
* CentOS/Redhat: ``sudo yum install postgresql-server``
    - Warning: Many Centos/Redhat installations provide *very* old versions of
      postgres.
* Archlinux: ``sudo pacman -S postgresql``
    - Warning: Archlinux will not start the database for you.

