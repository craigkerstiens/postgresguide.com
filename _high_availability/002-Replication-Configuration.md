---
layout: page
title:  "Replication configuration"
date:   2015-01-27 22:02:36
categories:
permalink: /ha/replication.html
---


The master configuration
=======================

The master server is responsible for distributing the changes to the stand by servers. We have to change to following settings to achieve that:

    port = 5432
    listen_addresses = '*' # we are using a star (bind to everything) as we want to reuse the same postgresql.conf to all our nodes
    wal_level = hot_standby
    max_wal_senders = 5 # this is the total of wal senders that can be used concurrently by the standbys or streaming base backups
    wal_keep_segments = 8 # how many wal segments should we keep? This has a relation with the speed with which the standbys consume the logs. Increase if you have slow standbys
    archive_mode = on # We keep archives in case we need them for slaves that have fallen behind
    hot_standby = on # this is ignored by the master server

It is much easier to keep a single postgresql.conf and share it between all your nodes. 

Apart from that, we have to permit for stand-by servers to connect to master and request logs. We need to add a line in pg_hba.conf that permits the slaves from the same subnet to connect.

    hostssl    replication     all        10.8.4.0/24            md5

Finally, we need to create a user that is allowed to connect to the server and start replication.

    psql# CREATE USER replicator REPLICATION LOGIN ENCRYPTED PASSWORD 'password';



The slave configuration
=========================

Setting up a stand-by to consume the logs is easy. We just need a base backup of the main database, plus all the archive logs that have happened in the meantime.
The command to do it in one take is

$ sudo -u postgres pg_basebackup -h 10.8.4.1 -U postgres -D /db/data -X stream -R -p 5432 -U replicator -W password

where 10.8.4.1 is the IP address of the master from which we want to make the backup, 5432 the port of the master and /db/data the directory in the filesystem where
the data are to be saved and replicator is the user we defined in the previous step.

The same command generates a recovery.conf file that notifies the postgres instance that it's a standby server and from where it should connect to get the archive logs.

At this point, we can edit the recovery.conf to specify a trigger file. A trigger file is a file that when present, instructs the standby to assume master duties. We don't 
need it, as we will do the failover via the clustware, the setting nevertheless is:

    trigger_file = '/path/to/the/trigger/file'

Keep in mind that the trigger file MUST NOT exist. You create it when you want to promote the standby to master, e.g. via touch /path/to/the/trigger/file


