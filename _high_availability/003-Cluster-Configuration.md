---
layout: page
title:  "Cluster configuration"
date:   2015-01-27 22:02:36
categories:
permalink: /ha/cluster.html
---


The cluster
------------------

Now that we have a correctly replicating database, we need to establish a mechanism for managing the actual failover and promotion of nodes. For this, we will create a cluster
using pacemaker and corosync. 

Packages
==============

The following steps must be run in all nodes of our DB cluster.

Let's start by installing the appropriate packages

    $ sudo apt-get install corosync pacemaker pacemaker-cli-utils cluster-glue

Then we need to update the postgres RA (resource agent) as the one in the standard distribution is a bit old

    $ sudo wget https://raw.githubusercontent.com/ClusterLabs/resource-agents/master/heartbeat/pgsql -O /usr/lib/ocf/resource.d/heartbeat/pgsql


Corosync configuration
=====================

After we have finished with the installations, it's time to configure corosync. 
The corosync configuration should be applied to every database node in /etc/corosync/corosync.conf

    totem {
        version: 2
        secauth: off
        cluster_name: dbcluster
        transport: udpu
    }

    nodelist {
        node {
            ring0_addr: db1.hostname
            nodeid: 1
        }
        node {
            ring0_addr: db2.hostname
            nodeid: 2
        }
    }

    logging {
        fileline: off
        to_logfile: yes
        to_syslog: no
        debug: off
        logfile: /var/log/corosync.log
        timestamp: on
        logger_subsys {
            subsys: AMF
            debug: off
        }
    }

    quorum {
         provider: corosync_votequorum
          expected_votes: 2
           two_nodes: 1
    }


After we restart corosync and pacemaker, we are ready to configure pacemaker. Pacemaker configuration is being done through crm, 
so we execute the following:

Pacemaker/resources configuration
===================================

    crm configure property no-quorum-policy="ignore"
    crm configure property stonith-enabled="false" # we don't need STONITH for now

    crm configure rsc_defaults resource-stickiness="INFINITY"
    crm configure rsc_defaults migration-threshold=1

    # The IP of the MASTER node
    crm configure primitive vip-master ocf:heartbeat:IPaddr2 params ip=10.8.3.1 cidr_netmask=24 \
      op start   timeout="60s" interval="0s"  on-fail="restart" \
      op monitor timeout="60s" interval="10s" on-fail="restart" \
      op stop    timeout="60s" interval="0s"  on-fail="block"

    # The IP of the SLAVE node
    crm configure primitive vip-slave ocf:heartbeat:IPaddr2 params ip=10.8.3.2 cidr_netmask=24 \
      meta \
      resource-stickiness="1" \
      op start   timeout="60s" interval="0s"  on-fail="restart" \
      op monitor timeout="60s" interval="10s" on-fail="restart" \
      op stop    timeout="60s" interval="0s"  on-fail="block"

    crm configure primitive pingCheck ocf:pacemaker:ping \
        params \
            name="default_ping_set" \
            host_list="10.8.3.1" \
            multiplier="100"\
        op start   timeout="60s" interval="0s"  on-fail="restart" \
        op monitor timeout="60s" interval="10s" on-fail="restart" \
        op stop    timeout="60s" interval="0s"  on-fail="ignore"

    crm configure clone clnPingCheck pingCheck 

    crm configure primitive pgsql ocf:heartbeat:pgsql params pgport="5234"\
       pgctl="/usr/lib/postgresql/9.3/bin/pg_ctl" \
       psql="/usr/lib/postgresql/9.3/bin/psql" \
       pgdata="/db/data/" \
       node_list="db1.dbcluster db2.dbcluster" \
       restore_command="cp /db/data/pg_archive/%f %p" \
       primary_conninfo_opt="keepalives_idle=60 keepalives_interval=5 keepalives_count=5" \
       master_ip="10.8.3.1" \
       stop_escalate="0" \
       rep_mode="async" \
       start_opt="-p 5234" \
       op start   timeout="60s" interval="0s"  on-fail="restart" \
       op monitor timeout="60s" interval="4s" on-fail="restart" \
       op monitor timeout="60s" interval="3s"  on-fail="restart" role="Master" \
       op promote timeout="60s" interval="0s"  on-fail="restart" \
       op demote  timeout="60s" interval="0s"  on-fail="stop" \
       op stop    timeout="60s" interval="0s"  on-fail="block" \
       op notify  timeout="60s" interval="0s"

    crm configure ms msPostgresql  pgsql \
        meta \
            master-max="1" \
            master-node-max="1" \
            clone-max="2" \
            clone-node-max="1" \
            notify="true"

    crm configure colocation rsc_colocation-1 inf: msPostgresql        clnPingCheck
    crm configure colocation rsc_colocation-2 inf: vip-master msPostgresql:Master

    # we want the slave to move to the master if the slave fails. This is optional but it helps
    # if we have the read traffic served by the slave node.
    # crm configure colocation rsc_colocation-3 inf: vip-slave msPostgresql:Slave

    crm configure order rsc_order-1 0: clnPingCheck          msPostgresql
    crm configure order rsc_order-2 0: msPostgresql:promote  vip-master:start   symmetrical=false

    # Again, optional but required if we serve read traffic from the slave
    # crm configure order rsc_order-3 0: msPostgresql:demote   vip-slave:start    symmetrical=false

    crm configure location rsc_location-1 vip-slave \
        rule  200: pgsql-status eq "HS:sync" \
        rule  200: pgsql-status eq "HS:async" \
        rule  100: pgsql-status eq "PRI" 

    crm configure location rsc_location-2 msPostgresql \
        rule -inf: not_defined default_ping_set or default_ping_set lt 100

