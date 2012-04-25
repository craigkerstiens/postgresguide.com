Execution Plan
##############

What is an Execution Plan
-------------------------

Postgres has a great ability to show you how it will actually execute a query under the covers. This is known as an `execution plan` and which is exposed by **explain**. Understanding this tells you how you can optimize your database with indexes to improve performance. The hard part for most users is understanding the output of these. While there's many pieces that are involved in understanding there's a few key primers most developers should know.

More About Explain
------------------

Every query within Postgres has an execution plan when executed. There are three forms of running **explain** to expose this to you:

- The generic form (only shows what is likely to happen)
- Analyze form (which actually runs the query and outputs what does happen)
- Verbose form (stay away)

Explain can be run on many statements with most common being `SELECT` statements, though you can also use it on:

- INSERT
- UPDATE
- DELETE
- EXECUTE
- DECLARE

Using Explain
-------------

Given a query: 

.. code-block:: sql
   
   SELECT last_name FROM employees where salary >= 50000;

We can inspect how Postgres will execute it with:

.. code-block:: sql
   
   EXPLAIN SELECT last_name FROM employees where salary >= 50000;
                             QUERY PLAN                          
   --------------------------------------------------------------
    Seq Scan on employees  (cost=0.00..16.50 rows=173 width=118)
      Filter: (salary >= 50000)

We can both execute the query and inspect the path/time it took with:

.. code-block:: sql
   
   EXPLAIN ANALYZE SELECT last_name FROM employees where salary >= 50000;
                                               QUERY PLAN                                               
   --------------------------------------------------------------------------------------------------------
    Seq Scan on employees  (cost=0.00..16.50 rows=173 width=118) (actual time=0.018..0.018 rows=0 loops=1)
      Filter: (salary >= 50000)
    Total runtime: 0.053 ms


Understanding Execution Plans
-----------------------------

Perhaps the hardest part of execution plans is actually understanding what they mean. First a brief disclaimer, this is not to be an end all be all reference, but rather a basic starting place to understanding the queries and optimizing your database.

If you run an `EXPLAIN ANALYZE` on the above table with 2 million rows you might see something like:

.. image:: http://cl.ly/1f3o2w3x1a41402B2g1R/1.%20psql-1.png
   :width: 650

But lets take a look at what it actually means

.. image:: http://f.cl.ly/items/2F1A2T0a3h1v1d2u213O/1.%20psql-2.png
   :width: 650

There's a couple of key items here. Often times you want to look for when a `sequential scan` is occurring, but more importantly you want to look at what the three items above are. The startup time, the maximum time and finally the number of rows returned. In this case, because we ran EXPLAIN ANALYZE, we have not only the estimated on the left, but the actual on the right as well:

.. image:: http://cl.ly/3i1x2D3R3w3D1I0R1h3W/1.%20psql-4.png
   :width: 650

In this case we see there's a high time spent and a sequential scan. As a result we may want to try to add an index and examine the results:

.. code-block:: sql

   CREATE INDEX idx_emps on employees (salary);

With this we've now cut our query time from 295 ms to 1.7 ms:

.. image:: http://cl.ly/1j1B0w2X2k0c281M2K3E/1.%20psql-10.png
   :width: 650
