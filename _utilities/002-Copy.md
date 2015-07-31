---
layout: page
title:  "Copy"
date:   2015-01-27 22:02:36
categories: General-SQL
permalink: /utilities/copy.html
---

What is copy
------------

Postgres ships with several great utilities for moving your data around. The obvious ones are pg\_dump and pg\_restore for of course database backups and restores. A similar utility thats far less talked about, but equally as valuable is Postgres's copy utility. Copy allows you to do
copy data into and out of tables in your database. It supports several modes including:

-   binary
-   tab delimited
-   csv delimited

Whether its for bulk data loading for testing, doing some light weight ETL, or simply grabbing a data extract to send to someone its a utility every developer will want to utilize at some point.

Copy in Action
--------------

Extracting all employees to a tab delimited file:

    \copy (SELECT * FROM employees) TO '~/employees.tsv';

Extracting all employees to a csv delimited file:

    \copy (SELECT * FROM employees) TO '~/employees.csv' WITH (FORMAT CSV);

Extracting all employees to a binary file (note the quotes around the word Binary):

    \copy (SELECT * FROM employees) TO '~/employees.dat' WITH (FORMAT "Binary");

And for loading data into a table the equivalent for each of the above:

    \copy employees FROM '~/employees.tsv';
    \copy employees FROM '~/employees.csv' WITH CSV;
    \copy employees FROM '~/employees.dat' WITH BINARY;
