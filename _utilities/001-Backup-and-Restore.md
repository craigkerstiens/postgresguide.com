---
layout: page
title:  "Backup and Restore"
date:   2015-01-27 22:02:36
permalink: /utilities/backup-restore.html
---

What is it
----------

Hopefully its clear to anyone reading this what backup and restore is in regards to your database. But, in case you're entirely new to databases and even more so computers, a backup is simply a full copy of your database schema and data, with restore being the ability to use that backed up data and load it into your database or another database.

Note: Backup and restore is done on an entire database or entire table, and not meant for extracts of data. In that case you would use copy.

Backup
------

[pg\_dump](http://www.postgresql.org/docs/8.4/static/app-pgdump.html) is the utility for backing up your database. There are a few key knobs you have when dumping your database. These include:

-   Plaintext format (readable and large) vs. binary format (unreadable and small) vs. tarball (ideal for restore)
-   All of your database or specific schemas/tables

So lets get started with some backing up - if you need a reminder of your databases you can list them with:

    psql -l

Then carry out the dump with:

    pg_dump database_name_here > database.sql

The above will create the plaintext dump of your database. To create a form more suitable you a persistent backup and storage you can use either of the below:

    pg_dump -Fc database_name_here > database.bak # compressed binary format
    pg_dump -Ft database_name_here > database.tar # tarball

Restore
-------

When restoring, there are a few more options that you'll want to consider:

-   If the database already exists
-   The format of your backup

If your database already exists you only need to run the following:

    pg_restore -Fc database.bak # restore compressed binary format
    pg_restore -Ft database.tar # restore tarball

However, if you're creating your database new from the restore you'll want to run a command similar to the following:

    pg_restore -Fc -C database.bak # restore compressed binary format
    pg_restore -Ft -C database.tar # restore tarball
