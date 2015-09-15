---
layout: page
title:  "Options"
date:   2015-01-27 22:02:36
categories:
permalink: /ha/options.html
---



Making postgres highly available

When thinking about high availability and postgres, there are two seperate concerns that we need to address. The first one 
is data replication, that is, how we copy the data to all available nodes and the second one is failover, that is, how we
detect and manage failure of a node.

This guide deals with the standard PostgreSQL distribution and as such the scenario that covers is that of a single master and 
multiple slaves. The master serves requests and upon failure, a new master is chosen from the available nodes. 

Replication
-----------

There are a couple of different options when it comes to replication, with different tradeoffs between them.

The obvious way is to transfer, somehow, the changes in the underlying datafiles that PostgreSQL generates and have the slaves 
waiting on them until they become active. In that setup, there can only be one active node that serves the requests and when 
a failover occures the new active node mounts the datafiles, recovers what needs to be recovered and starts serving requests. The
main advantage of this solution is that the primary (the node that serves the requests) has zero penalty in the write performance
but the disadvantage is that we get to have a few nodes sitting inactive, waiting to resume active duties. 

The second solution is to take advantage of postgres binary replication. By using that we can have a master postgres communicating 
the changes to the standby servers continuously and having them replay those changes, so all slaves are in the same state. The 
advantage in that is that we can use the standby servers to offload read activity (still, we can have only one writeable node) with the 
disadvantage being that we have to pay a small performance drop when writing, as there must be a notification that the changes were
actually applied to the slaves.

This guide covers the second solution, which for applications that are read-oriented, we get an almost linear scale on the read performance,
as read operation (queries) can be performed to a multitude of stand-by servers.

Prerequisites
==============

Network
--------

We assume that all pg nodes are on the same subnet (e.g. 10.8.4.0/24). There are a few ways to achieve that:

1. Physically place them on the same network
2. If the above is not feasible (e.g. a cloud provider, or leased machines) you can use a VPN to establish a private network between the servers 
from which all communication will happen.

Operating System: We assume an ubuntu derivative, something later than 14.04
Postgres Version: 9.3 or later

We assume that the databases will be accessed through a 10.8.3.0/24 network. The master will be 10.8.3.1 and the slave 10.8.3.2.
We assume that the database nodes will have hostnames db[number].dbcluster



