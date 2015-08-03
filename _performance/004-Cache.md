---
layout: page
title:  "Cache"
date:   2015-01-27 22:02:36
categories: General-SQL
permalink: /performance/cache.html

---

Cache
=====

The typical rule for most applications is that only a fraction of its data is regularly accessed. As with many other things data can tend to follow the 80/20 rule with 20% of your data accounting for 80% of the reads and often times its higher than this. Postgres itself actually tracks access patterns of your data and will on its own keep frequently accessed data in cache. Generally you want your database to have a cache hit rate of about 99%. You can find your cache hit rate with:

    SELECT
           sum(heap_blks_read) as heap_read, 
           sum(heap_blks_hit) as heap_hit, 
           (sum(heap_blks_hit) - sum(heap_blks_read)) / sum(heap_blks_hit) as ratio

    FROM
         pg_statio_user_tables;

<!-- more -->

We can see in this
[dataclip](<https://postgres.heroku.com/dataclips/jfrtizxdthixfxkcdesxwesiibly>) that the cache rate for [Heroku Postgres](<https://postgres.heroku.com?utm_source=referral&utm_medium=content&utm_campaign=craigkerstiens>) is 99.99%. If you find yourself with a ratio significantly lower than 99% then you likely want to consider increasing the cache available to your database, you can do this on Heroku Postgres by [performing a fast database changeover](<https://devcenter.heroku.com/articles/fast-database-changeovers?utm_source=referral&utm_medium=content&utm_campaign=craigkerstiens>) or on something like EC2 by performing a dump/restore to a larger
instance size.

### Understanding Index Usage

The other primary piece for improving performance is [indexes](<https://devcenter.heroku.com/articles/postgresql-indexes?utm_source=referral&utm_medium=content&utm_campaign=craigkerstiens>). Several frameworks will add indexes on your primary keys, though if you're searching on other fields or joining heavily you may need to manually add such indexes.

Indexes are most valuable across large tables as well. While accessing data from cache is faster than disk, even data within memory can be slow if Postgres must parse through hundreds of thousands of rows to identify if they meet a certain condition. To generate a list of your tables in your database with the largest ones first and the percentage of time which they use an index you can run:

    SELECT
          relname, 100 * idx_scan / (seq_scan + idx_scan) percent_of_times_index_used, 
          n_live_tup rows_in_table
    FROM
         pg_stat_user_tables
    WHERE
         seq_scan + idx_scan \> 0
    ORDER BY
         n_live_tup DESC;

While there is no perfect answer, if you're not somewhere around 99% on any table over 10,000 rows you may want to consider adding an index. When examining where to add an index you should look at what kind of queries you're running. Generally you'll want to add indexes where you're looking up by some other id or on values that you're commonly filtering on such as created_at fields.

Pro tip: If you're adding an index on a production database use `CREATE INDEX CONCURRENTLY` to have it build your index in the background and not hold a lock on your table. The limitation to creating indexes [concurrently](<http://www.postgresql.org/docs/9.1/static/sql-createindex.html#SQL-CREATEINDEX-CONCURRENTLY>) is they can typically take 2-3 times longer to create and can't be run within a transaction. Though for any large production site these trade-offs are worth the trade-off in experience to your end users.

### Heroku Dashboard as an Example

Looking at a real world example of the recently launched Heroku dashboard, we can run this query and see our results:

    SELECT relname, 
           100 * idx_scan / (seq_scan + idx_scan) percent_of_times_index_used, 
           n_live_tup rows_in_table 
    FROM pg_stat_user_tables 
    ORDER BY n_live_tup DESC;

     relname              | percent_of_times_index_used | rows_in_table
     ---------------------+-----------------------------+--------------- 
     events               |             0               |       669917
     app_infos_user_info  |             0               |       198218 
     app_infos            |            50               |       175640
     user_info            |             3               |       46718 
     rollouts             |             0               |       34078 favorites            |             0               |       3059
     schema_migrations    |             0               |       2 
     authorizations       |             0               |       0 
     delayed_jobs         |            23               |       0

From this we can see the events table which has around 700,000 rows has no indexes that have been used. From here you could investigate within my application and see some of the common queries that are used, one example is pulling the events for this blog post which you are reading. You can see your [execution plan](<https://postgresguide.com/performance/explain.html?utm_source=referral&utm_medium=content&utm_campaign=craigkerstiens>) by running an [`EXPLAIN ANALYZE`](<https://postgresguide.com/performance/explain.html?utm_source=referral&utm_medium=content&utm_campaign=craigkerstiens>) which gives you can get a better idea of the performance of a specific query:

    EXPLAIN ANALYZE SELECT * FROM events WHERE app_info_id = 7559;
    QUERY PLAN
     -------------------------------------------------------------------
     Seq Scan on events (cost=0.00..63749.03 rows=38 width=688) (actual
     time=2.538..660.785 rows=89 loops=1) Filter: (app_info_id = 7559)
     Total runtime: 660.885 ms

Given there's a sequential scan across all that data this is an area we can optimize with an index. We can add our index concurrently to prevent locking on that table and then see how performance is:

    CREATE INDEX CONCURRENTLY idx_events_app_info_id ON
    events(app_info_id); 
    EXPLAIN ANALYZE SELECT * FROM events WHERE app_info_id = 7559;

    ---------------------------------------------------------------------- 
    Index Scan using idx_events_app_info_id on events (cost=0.00..23.40 rows=38 width=688) (actual time=0.021..0.115 rows=89 loops=1)
     :   Index Cond: (app_info_id = 7559)

     Total runtime: 0.200 ms

While we can see the obvious improvement in this single query we can
examine the results in [New Relic](https://elements.heroku.com/addons/newrelic) and see that we've significantly reduced our time spent in the database with the addition of this and a few other indexes:

![NewRelicGraph](<http://f.cl.ly/items/2x3g2h2220162C2M0w0r/Pasted%20Image%2010:1:12%208:55%20AM-2.png>)

### Index Cache Hit Rate

Finally to combine the two if you're interested in how many of your indexes are within your cache you can run:

    SELECT
       sum(idx_blks_read) as idx_read, 
       sum(idx_blks_hit) as idx_hit, 
       (sum(idx_blks_hit) - sum(idx_blks_read)) / sum(idx_blks_hit) as ratio
    FROM
         pg_statio_user_indexes;

Generally, you should also expect this to be in the 99% similar to your regular cache hit rate.
