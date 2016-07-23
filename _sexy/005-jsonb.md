---
layout: page
title:  "JSON"
date:   2016-07-23 22:02:36
categories: General-SQL
permalink: /cool/json.html
---

JSON arrived in Postgres with 9.2, though in reality the more usable version arrived in Postgres 9.4 as JSONB. JSONB is an on disk binary representatin of JSON, this means it's more efficiently stored and indexable. If you're looking for a comparisson of hstore, JSON, and JSONB check out this [blog post](https://www.citusdata.com/blog/2016/07/14/choosing-nosql-hstore-json-jsonb/).

Creating JSONB columns
---------------------

To create a JSONB simply specify the JSONB type on `CREATE TABLE`:

    CREATE TABLE products (
      id serial PRIMARY KEY,
      name varchar,
      attributes JSONB
    );

Inserting data
--------------

Inserting JSON into your new column should be fairly straightforward:

    INSERT INTO products (name, attributes) VALUES (
     'Geek Love: A Novel', '{
     	"author": "Katherine Dunn",
        "pages": 368,
        "category": "fiction"}'
     );

Indexing
--------

The most flexible and debatably most powerful method of indexing is to use a `GIN` index. A GIN index will index every single column and key within your JSONB document. Adding a GIN index should be pretty straightforward:

    CREATE INDEX idx_products_attributes ON products USING GIN (attributes);


Querying
--------

There's a number of extra operators you can use when working with JSONB. These will help you filter to various keys, extract values, etc. A few of the most common ones include:

*Extracting an attribute*

    SELECT attributes->'category' FROM products;

*Extracting an attribute as text**

    SELECT attributes->>'category' FROM products;

*Some key holds some value*

    SELECT * 
    FROM products 
    WHERE attributes->'category' ? 'fiction';