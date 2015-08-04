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

For Linux
---------

### For APT systems (Ubuntu, Debian, Mint, Etc)

    sudo apt-get install postgresql

### For Arch Linux

    sudo pacman -S postgresql

### For YUM installations (Fedora / Red Hat / CentOS / Scientific Linux)


(Example used is for PostgreSQL 9.2 on CentOS 6.4 x64)

1.  Head over to [PostgreSQL Yum Repository](http://yum.postgresql.org/)
2.  Select the version of PostgreSQL that you want to install and then your OS, version and architecture.
3.  Download the RPM for your platform (using the link from step 2)

    `curl -O http://yum.postgresql.org/9.2/redhat/rhel-6-x86_64/pgdg-centos92-9.2-6.noarch.rpm`

4.  Install the RPM

    rpm -ivh pgdg-centos92-9.2-6.noarch.rpm

5.  Do a quick search which will show you available packages for postgres

    yum list postgres*

> Note: It will probably list older versions as well, make sure to select proper version that you want to install and all the packages are of same version i.e server, client, contrib (not always necessary but better to be safe, right?)

6.  Install Packages as per choice

    yum install postgresql92-server.x86_64 postgresql92-contrib.x86_64 postgresql92-devel.x86_64

For Windows
-----------

[Windows Installer](http://www.enterprisedb.com/products-services-training/pgdownload#windows)

