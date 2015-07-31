---
layout: page
title:  "Users"
date:
categories: setup
permalink: /setup/users.html
---

Adding a User
-------------

Once you've initially installed Postgres you should be able to connect almost immediately with psql -h localhost. This will put you inside your database to begin working. Of course the next step before doing anything else is to create a user account for yourself.

    craig=# CREATE USER craig WITH PASSWORD 'Password';
    CREATE ROLE

New user craig is created with password Password.

Next step is to create a database and grant access to the user craig

    craig=# CREATE DATABASE pgguide;
    CREATE DATABASE

Now new database pgguide is created. Now we will grant access to craig.

    craig=# GRANT ALL PRIVILEGES ON DATABASE pgguide to craig;
    GRANT

Now craig has all privileges on database pgguide. There are several different kinds of privilege: SELECT, INSERT, UPDATE, DELETE, RULE, REFERENCES, TRIGGER, CREATE, TEMPORARY, EXECUTE, and USAGE.

    craig=# GRANT SELECT ON DATABASE pgguide to craig;
    GRANT

`GRANT SELECT` allows craig ONLY to do select query on database pgguide


