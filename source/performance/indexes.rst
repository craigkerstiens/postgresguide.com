Indexes
#######

What is an Index
----------------

An index is a specific structure that organizes a reference to your data that makes it easier to look up. In Postgres it is a copy of the item you wish to index combined with a reference to the actual data location. When accessing data, Postgres will either use some form of an index if it exists or a sequential scan. A sequential scan is when it searches over all of the data before returning the results.

Advantages and Disadvantages
----------------------------

Indexes are great for accessing your data faster. In most cases adding an index to a column will allow you to query the data faster. However, the trade off is that for each index you have you will insert data at a slower pace. Essentially when you insert your data with an index it must write data to two places as well as maintain the sort on the index as you insert data. Certain indexes additionally will be more effective than others, such as indexes on numbers or timestamps (text is expensive).

Indexes in action
-----------------

Lets jump straight to it and create an index on the given table:

.. image:: http://f.cl.ly/items/2I0a2u3z1x1Q0h2t3f1M/Untitled%202.png
   :height: 300

.. code-block:: sql

   CREATE INDEX idx_salary ON employees(salary);

You can create an index on one or many columns at a time. If you commonly filter against multiple columns in your database you can create your indexes against both columns:

.. code-block:: sql

   CREATE INDEX idx_salary ON employees(last_name, salary);

Tips
----

When your index is smarter than you
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In all cases an index will not be be used by Postgres. Most of the time you should trust Postgres to do the right thing. An example case is when your query returns a large percentage of the data that exists in a table, it may not use the index. This is because it is easiest to scan the table once, versus using the index then making additional lookups.

Count
~~~~~

One other case for Postgres that is currently costly due to sequential scans is count(*). There is not another way for Postgres to count the rows in a result set other than doing the full scan of the data.

Foreign Keys and Indexes
~~~~~~~~~~~~~~~~~~~~~~~~

Some ORMs when they create Foreign Keys will also create an index for you. Its of note that Postgres does not automatically create an index when creating the primary key, it is a separate step which you must do if not using an ORM.

Further Reading
---------------

If you're looking for further reading I'd highly recommend checking out the book `PostgreSQL 9.0 High Performance <http://www.amazon.com/gp/product/184951030X/ref=as_li_qf_sp_asin_tl?ie=UTF8&tag=mypred-20&linkCode=as2&camp=1789&creative=9325&creativeASIN=184951030X>`_. Greg Smith, the author, is a personal friend and knows Postgres Performance extremely well, there's not a more definitive reference for postgres performance.
