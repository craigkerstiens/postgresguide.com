---
layout: page
title:  "Views"
date:   2015-01-27 22:02:36
categories: General-SQL
permalink: /sql/views.html
---

What is a View
--------------

According to [wikipedia](http://en.wikipedia.org/wiki/View_%28database%29) "a view consists of a stored query accessible as a virtual table in a relational
database or a set of documents in a document-oriented database composed of the result set of a query or map and reduce functions."

In simpler terms a view is simply a logical table that automatically connects the pieces of underlying data. It does not actually duplicate or persist the data as its viewed in a logical form.

Why use a View
--------------

Views are useful for many cases. Views are a great way to simplify your data model when providing it to others to work with. Additionally it can simplify working with your data for yourself as well. If you find yourself routinely joining two sets of data in a similar way a view may ease the process of duplicating that many times.

When working with others not familiar with SQL a view is a great way to provide your un-normalized data.

A View in Action
----------------

Lets take an example of some tables:

![image](http://f.cl.ly/items/072Q3Y073Z0o413b3N2x/Untitled%202-1.png)

![image](http://f.cl.ly/items/2Q470O2S2f2v1u091r3h/Untitled%202-2.png)

![image](http://f.cl.ly/items/2I0a2u3z1x1Q0h2t3f1M/Untitled%202.png)

To get your employees and their departments you'd often write a query that looks something similar to:

    SELECT 
      employees.last_name, 
      employees.salary, 
      departments.department
    FROM 
      employees, 
      employee_departments,
      departments
    WHERE 
      employees.id = employee_departments.employee_id
      AND departments.id = employee_departments.department_id

In this case its not too complicated, though it does become tedious each time you wish to report against employes and their departments. This can be greatly simplified by creating a view which will automatically do these joins for you:

    CREATE OR REPLACE VIEW employee_view AS
    SELECT 
      employees.last_name, 
      employees.salary, 
      departments.department
    FROM 
      employees, 
      employee_departments,
      departments
    WHERE 
      employees.id = employee_departments.employee_id
      AND departments.id = employee_departments.department_id


Now you can simply query your new table directly:

    SELECT *
    FROM employee_view

And have it yield just as it would with the join above:

    last_name    salary   department
    Jones        45000    Accounting 
    Adams        50000    Sales
    Johnson      40000    Marketing
    Williams     37000    Accounting
    Smith        55000    Sales

