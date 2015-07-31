---
layout: page
title:  "Enumerated Data Types"
date:   2015-01-27 22:02:36
categories: General-SQL
permalink: /sexy/enums.html
---

Postgres provides enumerated types or ‘enums’ if you need to make sure some column values need to have a specific value out of a set of values. For example, if you need a column to only have values ‘Email’, ‘SMS’ and ‘Phone’, you can do this by first defining an enumerated type:

    CREATE TYPE e_contact_method AS ENUM (
      'Email', 
      'Sms', 
      'Phone')

Then associate the enum to the column that needs to have a fixed set of values.

    CREATE TABLE contact_method_info (
       contact_name text,
       contact_method e_contact_method,
       value text
    )

Using enums
===========

    INSERT INTO contact_method_info
    VALUES ('Jeff', 'Email', 'jeff@mail.com')

    # select * from contact_method_info;
     contact_name | contact_method |     value     
     --------------+----------------+---------------
     Jeff         | Email          | jeff@mail.com
    (1 row)


You cannot insert a value for the contact_method column thats not in e_contact_method enum.

    # INSERT INTO contact_method_info VALUES ('Jeff', 'Fax', '4563456');
    ERROR:  invalid input value for enum e_contact_method: "Fax"
    LINE 1: INSERT INTO contact_method_info VALUES ('Jeff', 'Fax', '4563...


Viewing/Modifying enum values
=============================

You can view the list of values in an enum:

    # select t.typname, e.enumlabel 
      from pg_type t, pg_enum e 
      where t.oid = e.enumtypid;
      
        typname      | enumlabel
      ------------------+-----------
      e_contact_method | Email
      e_contact_method | Sms
      e_contact_method | Phone
    (3 rows)


You can append values to existing enums:

    ALTER TYPE e_contact_method
     ADD VALUE 'Facebook' AFTER 'Phone';

    # select t.typname, e.enumlabel from pg_type t, pg_enum e 
      where t.oid = e.enumtypid;
        typname      | enumlabel
    ------------------+-----------
    e_contact_method | Email
    e_contact_method | Sms
    e_contact_method | Phone
    e_contact_method | Facebook
    (4 rows)


Values can be added anywhere in between as enums have a sort order which is the order in which the value was inserted, and it is preserved.

    ALTER TYPE e_contact_method
     ADD VALUE 'Twitter' BEFORE 'Sms';

    # select t.typname, e.enumlabel, e.enumsortorder from pg_type t, pg_enum e 
      where t.oid = e.enumtypid order by e.enumsortorder;
        typname      | enumlabel | enumsortorder
    ------------------+-----------+---------------
    e_contact_method | Email     |             1
    e_contact_method | Twitter   |           1.5
    e_contact_method | Sms       |             2
    e_contact_method | Phone     |             3
    e_contact_method | Facebook  |             4
    (5 rows)


At the time of this writing, Postgres does not provide a way to remove values from enums.
