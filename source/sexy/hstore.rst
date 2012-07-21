HStore
######

What is it
----------

HStore is a key value store within Postgres. You can use it similar to how you would use a dictionary within another language, though it's specific to a column on a row.

Enabling HStore
---------------

To enable HStore on your database you run:

.. code-block:: sql

   CREATE EXTENSION hstore;


Creating an hStore column
-------------------------

To create a field in a table with the hstore datatype simply use hstore as the column type:

.. code-block:: sql

   CREATE TABLE products (
     id serial PRIMARY KEY,
     name varchar,
     attributes hstore
   );

Inserting data
--------------

To insert data you would include it all within single quotes as you would for a text field. The difference with hstore is some extra structure so it knows how to create the dictionary:

.. code-block:: sql

  INSERT INTO products (name, attributes) VALUES (
   'Geek Love: A Novel',
   'author    => "Katherine Dunn",
    pages     => 368,
    category  => fiction'
   );

Retrieving data
---------------

.. code-block:: sql

   SELECT name, attributes->'device' as device 
   FROM products 
   WHERE attributes->'edition'= 'ebook'