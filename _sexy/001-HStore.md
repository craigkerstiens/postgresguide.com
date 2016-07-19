---
layout: page
title:  "HStore"
date:   2015-01-27 22:02:36
categories:
permalink: /cool/hstore.html
---

*Note: With the release of Postgres 9.4 and JSONB, in most cases it becomes a better approach than simply HStore. For a more in depth comparisson you can check out [this post](https://www.citusdata.com/blog/2016/07/14/choosing-nosql-hstore-json-jsonb/) by [Citus Data](https://www.citusdata.com)*

What is it
----------

HStore is a key value store within Postgres. You can use it similar to how you would use a dictionary within another language, though it's specific to a column on a row.

Enabling HStore
---------------

To enable HStore on your database you run:

    CREATE EXTENSION hstore;

Creating an hStore column
-------------------------

To create a field in a table with the hstore datatype simply use hstore as the column type:

    CREATE TABLE products (
      id serial PRIMARY KEY,
      name varchar,
      attributes hstore
    );

Inserting data
--------------

To insert data you would include it all within single quotes as you would for a text field. The difference with hstore is some extra structure so it knows how to create the dictionary:

    INSERT INTO products (name, attributes) VALUES (
     'Geek Love: A Novel',
     'author    => "Katherine Dunn",
      pages     => 368,
      category  => fiction'
     );


Retrieving data
---------------

    SELECT name, attributes->'author' as author
    FROM products
    WHERE attributes->'category' = 'fiction'
