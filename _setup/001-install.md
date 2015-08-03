---
layout: page
title:  "Installing Postgres"
date:
categories: setup
permalink: /setup/install.html
---

For Mac
-------

[Postgres App](http://www.postgresapp.com)

For APT installations
----------
(Debian / Ubuntu)

You can install postgresql directly via the repositories provided by the linux distribution:

    `apt-get install postgresql`

As an recommended alternative, you can add the postgresql repository, which is explained [in there wiki](https://wiki.postgresql.org/wiki/Apt).

(Example used is for PostgreSQL 9.4 on Debian 8 x64)

1. Create the repository file:

    `echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list`

2. Import their key:

    `apt-get install -y wget ca-certificates; wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -`

3. Update the package cache and install postgres:

    `apt-get update; apt-get install -y postgresql-94`

4. To be safe, you can also install the contrib and the devel package to ensure everything is in the same version and not mixed with the ones provided by the distribution itself:

    `apt-get install -y postgresql-contrib-9.4 postgresql-server-dev-9.4`

For Windows
-----------

[Windows Installer](http://www.enterprisedb.com/products-services-training/pgdownload#windows)

For YUM insallations
-------------------- 
(Fedora / Red Hat / CentOS / Scientific Linux)


(Example used is for PostgreSQL 9.4 on CentOS 7.1 x64)

1.  Head over to [PostgreSQL Yum Repository](http://yum.postgresql.org/)
2.  Select the version of PostgreSQL that you want to install and then your OS, version and architecture.
3.  Download the RPM for your platform (using the link from step 2)

    `curl -O http://yum.postgresql.org/9.4/redhat/rhel-7-x86_64/pgdg-centos94-9.4-1.noarch.rpm`

4.  Install the RPM

    yum install -y pgdg-centos94-9.4-1.noarch.rpm

5.  Do a quick search which will show you available packages for postgres

    yum list postgres*

> Note: It will probably list older versions as well, make sure to select proper version that you want to install and all the packages are of same version i.e server, client, contrib (not always necessary but better to be safe, right?)

6.  Install Packages as per choice

    yum install postgresql94-server.x86_64 postgresql94-contrib.x86_64 postgresql94-devel.x86_64
