---
layout: page
title:  "CTEs (Common Table Expressions)"
date:   2015-01-27 22:02:36
categories: General-SQL
permalink: /cool/ctes.html
---

Long complex SQL queries aren't always the most readable thing. CTEs (as a gross over simplification) are somewhat akin to a view, but only during that specific query. In effect you can build up multiple different CTEs that reference earlier ones you created, thus making more composable and readable SQL. You can also recursively call them, allowing you to do things that you would otherwise need procedural language for. 

The broad structure of a CTE is:

    WITH your_cte_name AS (
        SELECT foo, bar
        FROM your_table
    )

You can chain them together in a basic form such as:

    WITH your_cte_name AS (
        SELECT foo, bar
        FROM your_table
    ),
    cte_number_2_name AS (
        SELECT foo
        FROM your_cte_name
    )

You can find a more fully formed below, or read further over at [craigkerstiens.com](http://www.craigkerstiens.com/2013/11/18/best-postgres-feature-youre-not-using/):

    WITH user_task AS 
	(
	    SELECT 
	        u.id AS user_id,
	        p.id AS project_id,
	        u.email,
	        array_agg(t.name) AS task_list,
	        p.title
	    FROM
	        project p,
	        task t,
	        user_ u
	    WHERE
	            u.id = t.user_id
	        AND p.id = t.project_id
	    GROUP BY
	        u.id,
	        p.id
	),

	--- Calculates the total task per each project
	total_task_per_project AS 
	(
	    SELECT 
	        t.project_id,
	        count(*) as task_count
	    FROM 
	        task t
	    GROUP BY 
	        t.project_id
	),

	--- Calculates the projects per each user
	task_per_project_per_user AS 
	(
	    SELECT 
	        t.user_id,
	        t.project_id,
	        count(*) as task_count
	    FROM 
	        task t
	    GROUP BY 
	        t.user_id, 
	        t.project_id
	),

	--- Gets user ids that have over 50% of task assigned
	overloaded_user AS 
	(
	    SELECT 
	        tpu.user_id,
	        tpu.project_id
	    FROM 
	        task_per_project_per_user tpu,
	        total_task_per_project pp
	    WHERE
	            tpu.project_id = pp.project_id
	        AND tpu.task_count > (pp.task_count / 2)
	)

	SELECT 
	    ut.email,
	    ut.task_list,
	    ut.title
	FROM 
	     user_task ut,
	     overloaded_user ou
	WHERE
	         ut.user_id = ou.user_id
	     AND ut.project_id = ou.project_id
	;