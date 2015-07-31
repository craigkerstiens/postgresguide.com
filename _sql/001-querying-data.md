---
layout: page
title:  "Querying Data"
date:   2015-01-27 22:02:36
categories: General-SQL
permalink: /sql/select.html
---

Tables
------

Within a traditional RDBMS a particular data model will be stored within a table. Data may interact across tables, but we'll cover that later with joins. For now we'll start by viewing the tables that are available. Within Postgres we can do this by running the command `\d`:

    craig=# \d
             List of relations
     Schema |   Name    | Type  | Owner 
    --------+-----------+-------+-------
     public | products  | table | craig
     public | purchases | table | craig
     public | users     | table | craig
    (3 rows)

Querying Data
-------------

Lets start by laying out some data. In this case lets start with our users, this is the first part in constructing a query (knowing where your data is coming from). The next part is examining what data we can query. We can again do this with the `\d` command, though this time we'll append the table name to it:

    craig=# \d users
                     Table "public.users"
       Column   |            Type             | Modifiers 
    ------------+-----------------------------+-----------
     id         | integer                     | 
     first_name | character varying(50)       | 
     last_name  | character varying(50)       | 
     email      | character varying(255)      | 
     created_at | timestamp without time zone | 
     updated_at | timestamp without time zone | 
     last_login | timestamp without time zone | 
    

Here we can see we've got a variety of data, lets for starters say we just want the first\_name, last\_name, and email of users. Now that we know the data we want below we can construct our query:

-   The table we need to query
-   The data we want from that table

The syntax for doing this is below, it contains the data you want to retrieve, followed by where its coming from, with a semicolon signaling thats the end of your query:

    craig=# SELECT first_name, last_name, email 
    craig-# FROM users;
     first_name | last_name |           email           
    ------------+-----------+---------------------------
     Craig      | Kerstiens | craig.kerstiens@gmail.com
    (1 row)


This is great when we want to pull back all of the data in a table, but with any size-able dataset this is far less feasible. In such cases what we'll want to do is potentially both limit the amount of data we return as well as filter it. First lets start with filtering.

Filtering Data
--------------

To filter data you can use a combination of filters. The filter is first initially specified with the WHERE condition. An example of any user that has created an account since the start of 2012:

    SELECT email, created_at
    FROM users
    WHERE created_at >= '2012-01-01'

We can also combine this with other conditions using either the AND or the OR clause. To find all users that created accounts in January of 2012:

    SELECT email, created_at
    FROM users
    WHERE created_at >= '2012-01-01'
      AND created_at < '2012-02-01'

