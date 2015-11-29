---
layout: page
title:  "Tracking Disk Usage"
date:   2015-11-27
categories: General-SQL
permalink: /tips/disk-usage.html

---

Apart from general OS level disk usage commands like `du -sh` or `df -H`, there might be situations where we might to track database/table/index size individually.

Postgres offers a convenient way to do this by means of queries and as well as psql command shortcuts.


Measuring database size
-----------------------
	
Database size can be easily found out by using the psql comamand shortcut `\l+`, which lists all the databases with their size as well.This is pretty handy when you are in the psql shell.
But if you wan't to query this information perhaps from JDBC i.e outside of the psql shell then you can run the following query which give the size of the database.
	
	learning=# select pg_size_pretty(pg_database_size('learning'));
 	pg_size_pretty
	----------------
 	1007 MB
	(1 row)



Measuring table size
-----------------------

From the shell, there is a command similar to database size.Using `\d+` will show all the tables with their size.
The following will give the same via a query.

	learning=# select pg_size_pretty(pg_relation_size('users'));
 	pg_size_pretty
	----------------
	194 MB
	(1 row)	


Measuring index size
---------------------
The above same query can be used to see index size as below.

	learning=# select pg_size_pretty(pg_relation_size('users_pkey'));
 	pg_size_pretty
	----------------
 	43 MB
	(1 row)

Measuring table size along with indexes
----------------------------------------

Indexes are stored separately from tables.But if you wan't to find the total size of a table along with all of the indexes, then the below query can be used.

	learning=# select pg_size_pretty(pg_total_relation_size('users'));
 	pg_size_pretty
	----------------
 	698 MB
	(1 row)

This technique does not apply to foreign tables.You might wan't to refer to the appropriate wrapper you are using.





