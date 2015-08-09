---
layout: page
title:  "Indexes"
date:   2015-01-27 22:02:36
categories:
permalink: /performance/indexes.html

---
Indexes
=======

What is an Index
----------------

An index is a specific structure that organizes a reference to your data that makes it easier to look up. In Postgres it is a copy of the item you wish to index combined with a reference to the actual data location. When accessing data, Postgres will either use some form of an index if it exists or a sequential scan. A sequential scan is when it searches over all of the data before returning the results.

Advantages and Disadvantages
----------------------------

Indexes are great for accessing your data faster. In most cases adding an index to a column will allow you to query the data faster. However, the trade off is that for each index you have you will insert data at a slower pace. Essentially when you insert your data with an index it must
write data to two places as well as maintain the sort on the index as you insert data. Certain indexes additionally will be more effective than others, such as indexes on numbers or timestamps (text is expensive).

Indexes in action
-----------------

Lets jump straight to it and create an index on the given table:

![image](http://f.cl.ly/items/2I0a2u3z1x1Q0h2t3f1M/Untitled%202.png)

    CREATE INDEX idx_salary ON employees(salary);

You can create an index on one or many columns at a time. If you commonly filter against multiple columns in your database you can create your indexes against both columns:

    CREATE INDEX idx_salary ON employees(last_name, salary);

Tips
----

### Create Index Concurrently

When Postgres creates your index, similar to other databases, it holds a lock on the table while its building the index. For smaller datasets this can be quite quick, but often by the time your adding an index it has grown to a large amount of data. This means that to get performance improvements you must essentially experience downtime, at least for that table. Postgres has the ability to create this index without locking the table. By using CREATE INDEX CONCURRENTLY your index will be built without a long lock on the table while its built. An example use would
be:

    CREATE INDEX CONCURRENTLY idx_salary ON employees(last_name, salary);

### When your index is smarter than you

It is not always fastest for Postgres to make use of an index. Most of the time you should trust Postgres to do the right thing. An example case is when your query returns a large percentage of the data that exists in a table, it may not use the index. This is because it is easiest to scan the table once, versus using the index then making additional lookups.

### Count

Since Postgres version 9.2, count(*) queries can be optimized with indexes thanks to index-only scans. However in previous versions, count(*) queries are costly because Postgres has to do a sequential scan. 


### Foreign Keys and Indexes

Some ORMs when they create Foreign Keys will also create an index for you. Its of note that Postgres does not automatically create an index when creating the foreign key, it is a separate step which you must do if not using an ORM.

### [Covering Indexes](https://wiki.postgresql.org/wiki/Index-only_scans#Covering_indexes)

Also since Postgres version 9.2, queries that touch only an index can be much faster. For this reason, it can be useful to include important data with an index. Performance can be particularly improved if the newly-created index has many fewer columns than the table being indexed, since many fewer pages must be retrieved from the disk in order to satisfy the query.

Further Reading
---------------

If you're looking for further reading I'd highly recommend checking out the book [PostgreSQL 9.0 High Performance](http://www.amazon.com/gp/product/184951030X/ref=as_li_qf_sp_asin_tl?ie=UTF8&tag=mypred-20&linkCode=as2&camp=1789&creative=9325&creativeASIN=184951030X). Greg Smith, the author, is a personal friend and knows Postgres Performance extremely well, there's not a more definitive reference for postgres performance.
