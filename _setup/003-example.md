---
layout: page
title:  "Example Database"
date:
categories: setup
permalink: /setup/example.html
---

For those interested in the querying portion of Postgres guide and less on designing their application you can load an example database provided by us. This example database is used through the SQL section and allows you to follow along without having to have your own schema/data.

Local Setup
-----------

First you'll want to download the data, then load it:

    curl -L -O http://cl.ly/173L141n3402/download/example.dump
    createdb pgguide
    pg_restore --no-owner --dbname pgguide example.dump
    psql --dbname pgguide

If you don't already have Postgres running locally you can use [Heroku Postgres](https://postgres.heroku.com) to provision a free database to use for development. Once you've provisioned a Heroku Postgres database you can load it with:

    heroku pgbackups:restore DATABASE 'http://cl.ly/173L141n3402/download/example.dump'

Understanding the Schema
------------------------

The schema contains an example set of products, purchases, and the users that made purchases. The basic layout of the tables and the relationship between them is laid out as:

![image](http://f.cl.ly/items/2p2W3e2y3p0T362w3t0R/Screenshot%2012:14:12%2012:37%20PM.png)
