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
- Recursive CTEs (Is your head already spining??)

Examples
--------------------------

1. Normal CTE :

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

