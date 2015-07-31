---
layout: page
title:  "Conditional Constraints"
date:   2015-01-27 22:02:36
categories: General-SQL
permalink: /performance/conditional.html

---
Conditional Constraints
=======================

There are times where you may want data constraints, but only want them to exist in certain cases. Take an example case where you don't want to physically delete users, but rather wish to logically delete them. If a user were to come back months later your option would then be to undelete the logically deleted user. By using a [Partial Indexes](http://www.postgresql.org/docs/9.1/static/indexes-partial.html) this becomes simpler by placing a unique index on only non-deleted users:

    CREATE UNIQUE INDEX user_email ON users (email) WHERE deleted_at IS NULL;
