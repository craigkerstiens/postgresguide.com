Common Table Expressions AKA WITH Queries
################

What are they
-------------

From Documentation : "WITH provides a way to write auxiliary statements for use in a larger query. These statements, which are often referred to as Common Table Expressions or CTEs, can be thought of as defining temporary tables that exist just for one query. Each auxiliary statement in a WITH clause can be a SELECT, INSERT, UPDATE, or DELETE; and the WITH clause itself is attached to a primary statement that can also be a SELECT, INSERT, UPDATE, or DELETE."

CTEs help to break huge complicated queries into simpler modules. Apart from making the query more readable, there is huge benefit of getting a subquery materialized once and for all which can be refereed by your main query (by name, we'll get to detail in a while) so that the sub query is not computed-recomputed everytime.
To summarize CTE is kinda short-hand for creating temp table, which we would create usually using something like this :

.. code-block:: sql

	CREATE TEMP TABLE foo AS SELECT...

CTEs in PostgeSQL can be divided in 3 kinds :

- Normal CTEs (Allows to make the results of queries available to other queries in the same statement. Only SLECTs.)
- Writable CTEs (Normal CTEs +  UPDATEs, DELETEs and INSERTs)
- Recursive CTEs (Is your head already spinning??)

Examples
--------------------------

1. Normal CTE :
~~~~~~~~~~~~~~~~~~~~~

The following CTE is equal to a normal select from employee table

.. code-block:: sql

	With all_employees AS (	
		Select empid, name, salary, deptid FROM employee
	)
	Select * From all_employees;

Now, consider that you know well in advance for a query that you will need to select a particular group of Emplyees (beloning to a particular Department)
The above code can be modified to use a where clause.

.. code-block:: sql

	With all_employees AS (	
	  Select empid, name, salary, deptid FROM employee Where deptid = 2
	)
	Select * From all_employees;

You can also have chained CTEs, i.e more than one CTEs in one statement, where one CTE uses resultset of previous CTE
For Example:

.. code-block:: sql

	With all_employees AS (	
	  Select empid, name, salary, deptid FROM employee Where deptid = 2
	),all_employees_with_deptname As(
	  Select e.*,d.deptname From all_employees e
	  Join department d
	  On e.deptid = d.deptid
	)
	Select * From all_employees_with_deptname;

In the above example the all_employees_with_deptname uses all_employees's resultset as a table.

2. Writable CTE :
~~~~~~~~~~~~~~~~~~~~~

Writable CTEs allow you to modify data apart from normal CTE functionality, they are ideal for using for UPSERT/MERGE functionality.

.. code-block:: sql

	With delete_employee AS (	
	  delete empid = 1 returning *
	)
	Select * from delete employee

It is similar to a normal DELETE but now consider that you keep a count of total employees in your department table so when you perform a delete operation in employee you also need those changes to reflect in department count.

.. code-block:: sql
	With delete_employee AS (	
	  delete empid = 1 returning *
	),summarise_deletion AS (
	select deptid, count(*) AS count from update_emplyee 
	group by deptid),update_dept_count_on_del As(
	update department d set staffcount = staffcount - count From summarise_deletion Where d.deptid = summarise_deletion.deptid
	)
	Select deptid, count(*) From update_dept_count_on_del;
	
The above query will calculate deleted emplyees per department and update the department table with respective count (i.e. subtracting the count).

Check `this<http://thombrown.blogspot.in/2011/11/writeable-common-table-expressions.html>`_ if you have time and want to learn in depth about wCTE.

3. Recursive CTE :
~~~~~~~~~~~~~~~~~~~~~

This particular CTE is very useful for handling graph like tables specifically when you need to find a list of child of a particular row upto n-level depth.

The following query returns sum of all the multiples of 3 or 5 below 1000, which `First Problem on Project Euler.<http://projecteuler.net/problem=1>`_
	
	WITH RECURSIVE t1(a, b) AS (
    VALUES(0,0)
    UNION ALL
        SELECT CASE CAST(b AS BOOLEAN)
                      WHEN b % 3 = 0 THEN b
                      WHEN b % 5 = 0 THEN b
                END,
                b + 1
          FROM t1
         WHERE b < 1000
	)
	SELECT sum(a) FROM t1

Now Consider you have a table which is something like

.. code-block:: sql

	Create Table Node (
	NodeId INTEGER PRIMARY KEY,
	ParentNodeId INTEGER NOT NULL ,
	...
	)
	
If you want to find all the children of a particular node (Say a node with NodeId 10):

.. code-block:: sql

	WITH RECURSIVE NodeList AS (
	SELECT Node.* FROM Node Where NodeId = 10
	UNION ALL
	SELECT first.* FROM Node AS first
	JOIN
	NodeList AS second
	ON (first.ParentNodeId = second.NodeId)
	)
	SELECT * FROM NodeList ORDER BY Order NodeId;