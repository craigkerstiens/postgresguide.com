---
layout: page
title:  "Working with Dates and Times"
date:   2015-01-27 22:02:36
categories:
permalink: /tips/dates.html

---

A common activity with any database or programming language is interacting with dates and times. Postgres has several date and time datatypes as well as extra functions for working with them that will make your life easier.

Datatypes
---------

-   Date - Date only (2012-04-25)
-   Time - Time only (13:00:00.00)
-   Timestamp - Date and Time (2012-04-25 13:00:00.00)
-   Time with Timezone - Time only (13:00:00.00 PST)
-   Timestamp with Timezone (2012-04-25 13:00:00.00 PST)
-   Interval - A span of time (4 days)

> Keep a special reminder about interval, its a great utility for when you
> :   need to query against some range of specific time.
>

Input Formats
-------------

Postgres will fortunately accept many forms of dates and times. The Postgres Documentation does a great job of documenting these formats so I'll leave it to them: [Date input format](http://www.postgresql.org/docs/9.1/static/datatype-datetime.html#DATATYPE-DATETIME-DATE-TABLE), [Time input format](http://www.postgresql.org/docs/9.1/static/datatype-datetime.html#DATATYPE-DATETIME-TIME-TABLE), and [Timezone input format](http://www.postgresql.org/docs/9.1/static/datatype-datetime.html#DATATYPE-TIMEZONE-TABLE).

Tips
----

### Truncating timestamps

There are often times where you will like query and group by some truncated form of a date. Postgres provides a convenient form for that date_trunc. Given an example users table with some basic columns you could find user signups by day with:

    SELECT count(*), date_trunc('day', created_at)
    FROM users
    GROUP BY 2
    ORDER BY 2 DESC;


You can find more on valid values for what you may truncate to over at the [Postgres Documentation](http://www.postgresql.org/docs/8.1/static/functions-datetime.html#FUNCTIONS-DATETIME-TRUNC).

> Ordering and grouping by a number as above works perfectly fine in Postgres
> :   it will automatically group and order by the column number. This
>     is not something you should use in production, but does work well
>     for ad-hoc queries.

### Intervals

Intervals as mentioned below are a great tool for examining data between two ranges. Similar to the above example with truncate you may want to find users that have signed up within the last 24 hours. Given you're not currently at a perfect split of an hour this becomes slightly more
advanced with the above. But of course there's no need to get the extract timeframe and put it in your condition. Instead we can simply:

    SELECT count(*)
    FROM users
    WHERE created_at >= (now() - '1 day'::INTERVAL);


An alternative syntax for this is available:

    SELECT count(*)
    FROM users
    WHERE created_at >= (now() - interval '1 month');
