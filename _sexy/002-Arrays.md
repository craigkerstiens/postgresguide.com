---
layout: page
title:  "Arrays"
date:   2015-01-27 22:02:36
categories: General-SQL
permalink: /cool/arrays.html
---

Postgres allows columns to be defined as arrays of variable length. The type of the array can be an inbuilt type, a user-defined type or an enumerated type.

Declaring array columns in tables:

    CREATE TABLE rock_band
    (
       name text,
       members text[]
    )

The above command will create a table rock_band with a text type column for the name of the band, and a column ‘members’ with a one-dimesional array to represent names of the members.

Inserting array values
----------------------

    INSERT INTO rock_band
    VALUES
    ('Led Zeppelin',
    '{"Page", "Plant", "Jones", "Bonham"}'
    )

Note that the array literals are double-quoted. Single quotes will give an error.

Querying the table will display:

    postgres=# select * from rock_band;
          name    |       members          
    --------------+---------------------------
     Led Zeppelin | {Page,Plant,Jones,Bonham}
    (1 row)


An alternative syntax to insert is to use the array constructor:

    INSERT INTO rock_band
    VALUES
    ('Pink Floyd',
      ARRAY['Barrett', 'Gilmour']
    )

When using the ARRAY constructor, the values are single-quoted.

    postgres=# select * from rock_band;
          name    |       members          
    --------------+---------------------------
     Led Zeppelin | {Page,Plant,Jones,Bonham}
     Pink Floyd   | {Barrett,Gilmour}
    (2 rows)

Accessing arrays
----------------

Array values can be accessed using subscripts or slices:

    postgres=# select name from rock_band where members[2] = 'Plant';
        name   
    --------------
     Led Zeppelin
    (1 row)

    postgres=# select members[1:2] from rock_band;
          members      
    -------------------
     {Page,Plant}
     {Barrett,Gilmour}
    (2 rows)

Modifying arrays
----------------

Arrays can be updated as a single element or as a whole:

Single-element update:

    postgres=# UPDATE rock_band set members[2] = 'Waters' where name = 'Pink Floyd';
    UPDATE 1
    postgres=# select * from rock_band where name = 'Pink Floyd';
        name    |   members      
    ------------+------------------
     Pink Floyd | {Barrett,Waters}
    (1 row)

Whole array update:

    postgres=# UPDATE rock_band set members = '{"Mason", "Wright", "Gilmour"}' where name = 'Pink Floyd';
    UPDATE 1 
    postgres=# select * from rock_band where name = 'Pink Floyd';    
    name        |        members      
    ------------+------------------------
     Pink Floyd | {Mason,Wright,Gilmour}
    (1 row)

Searching in arrays
-------------------

To search for an array that has a particular value, the keyword ANY isused.

    postgres=# select name from rock_band where 'Mason' = ANY(members);
        name    
    ------------
     Pink Floyd
    (1 row)

    postgres=# select name from rock_band where 'Barrett' = ANY(members);
     name
    ------
    (0 rows)


To search if all values of the array match a value, ALL is used.

> Article contributed by
> :   [Chandrakant Gopalan](http://cgopalan.tumblr.com).
>

