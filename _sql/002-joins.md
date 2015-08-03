---
layout: page
title:  "Joins"
date:   2015-01-27 22:02:36
categories: General-SQL
permalink: /sql/joins.html
---

What are they?
--------------

Joins are when you combine data from two different tables. The means in which you combine them depend on the type of join you use. There's multiple ways to join data, and we'll walk through each of those for starters lets look at an initial example to accomplish and the join that does it.

All of these examples will be based on our example schema:

    craig=# \d
             List of relations
     Schema |   Name    | Type  | Owner 
    --------+-----------+-------+-------
     public | products  | table | craig
     public | purchases | table | craig
     public | users     | table | craig
    (3 rows)

Joining some data
-----------------

Lets start with an example of wanting to find which products have been purchased recently. To do this we'll obviously need data from both our products able and our purchases table. Look at each of the tables to get a better idea of what columns they have:

    \d products
                 Table "public.products"
       Column    |          Type          | Modifiers 
    -------------+------------------------+-----------
     id          | integer                | 
     title       | character varying(255) | 
     description | text                   | 
     price       | numeric(10,2)          | 

    \d purchases 
         Table "public.purchases"
       Column   |  Type   | Modifiers 
    ------------+---------+-----------
     id         | integer | 
     user_id    | integer | 
     product_id | integer | 
     quantity   | integer |


When two tables are related its done so by keys. We'll explain more on this later, the important part for now is that we can see the product\_id on purchases is intended to reference the id field on products. With this we can now construct our query and retrieve as an example 5 purchases

    SELECT 
       products.title, 
       purchases.quantity
    FROM 
       products,
       purchases
    WHERE
       products.id = purchases.product_id
    LIMIT 5;

