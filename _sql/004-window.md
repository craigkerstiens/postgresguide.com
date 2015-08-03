---
layout: page
title:  "Window functions"
date:   2015-01-27 22:02:36
categories: General-SQL
permalink: /sql/window.html
---

What are they
-------------

The [Postgres docs](http://www.postgresql.org/docs/9.1/static/tutorial-window.html) actually do a great job of explaining what window functions are: "A window function performs a calculation across a set of table rows that are somehow related to the current row. This is comparable to the type of calculation that can be done with an aggregate function. But unlike regular aggregate functions, use of a window function does not cause rows to become grouped into a single output row — the rows retain their separate identities. Behind the scenes, the window function is able to access more than just the current row of the query result.". However, even as clear as that is the value of them may not be immediately clear, so perhaps its easiest to see them in action.

Window Functions in Action
--------------------------

Lets take an example table:

![image](http://f.cl.ly/items/3U200N113O2U2g1j2g3V/Untitled%202-3.png)

Lets assume that you wanted to find the highest paid person in each department. There's a chance you could do this by creating a complicated stored procedure, or maybe even some very complex SQL. Most developers would even opt for pulling the data back into their preferred language and then looping over results. With window functions this gets much easier.

First we can rank each individual over a certain grouping:


    SELECT last_name,
           salary,
           department,
           rank() OVER (
            PARTITION BY department
            ORDER BY salary
            DESC)
    FROM employees;

    last_name    salary   department    rank
    Jones        45000    Accounting    1
    Williams     37000    Accounting    2
    Smith        55000    Sales         1
    Adams        50000    Sales         2
    Johnson      40000    Marketing     1

Hopefully its clear from here how we can filter and find only the top paid employee in each department:

    SELECT *
    FROM
        (
            SELECT last_name,
                   salary,
                   department,
                   rank() OVER (
                    PARTITION BY department
                    ORDER BY salary
                    DESC
                   )
            FROM employees)
        sub_query
    WHERE rank = 1;

    last_name    salary   department    rank
    Jones        45000    Accounting    1
    Smith        55000    Sales         1
    Johnson      40000    Marketing     1

The best part of this is Postgres will optimize the query for you versus parsing over the entire result set if you were to do this yourself in PL/pgSQL or in your applications code.
