---
layout: page
title:  "Psql"
date:   2015-01-27 22:02:36
categories: General-SQL
permalink: /utilities/psql.html
---

What is psql
------------

Psql is the interactive terminal for working with Postgres. Theres an abundance of flags available for use when working with psql, but lets focus on some of the most important ones, then how to connect:

-   -h the host to connect to
-   -U the user to connect with
-   -P the port to connect to (default is 5432)

    psql -h localhost -U username databasename

The other option is to use a full string and let psql parse it:

    psql "dbname=dbhere host=hosthere user=userhere password=pwhere port=5432 sslmode=require"

Once you've connected you can begin querying immediately. In addition to basic queries you can also use certain commands. Running \\\\? will give you a list of all available commands, though a few key ones are called out the the tips below.

Tips
----

### List tables in database

    # \d
          List of relations
     Schema |   Name    | Type  | Owner 
    --------+-----------+-------+-------
     public | employees | table | craig
    (1 row)

### Describe a table

    # \d employees 
               Table "public.employees"
      Column   |         Type          | Modifiers 
    -----------+-----------------------+-----------
     id        | integer               | 
     last_name | character varying(50) | 
     salary    | integer               | 
    Indexes:
        "idx_emps" btree (salary)
