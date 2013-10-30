About
=====

`Postgres Guide (http://www.postgresguide.com) <http://www.postgresguide.com>`_ 
is intended to be a resource for both novice and knowledgable users of Postgres. 
It intends to cover guides on:

* Getting Postgres setup
* Creating and maintaining the database
* Means for accessing your data
* Special features within Postgres specifically

  - Window Functions
  - Common Table Expressions
  - Extensions


Build Instructions
==================

This project uses `Sphinx <http://sphinx-doc.org/>`_ to build the
documentation. Using `python <http://www.python.org>`_'s `virtualenv
<http://www.virtualenv.org/en/latest>`_ you can build the documentation as
follows:

Cloning the repository
----------------------

::

    git clone https://github.com/craigkerstiens/postgresguide.com.git
    cd postgresguide.com

Creating the virtual environment
--------------------------------

::

    virtualenv venv
    source venv/bin/activate

Notice that your shell prompt will change to indicate your entry into the
virtual environment.

Installing the dependencies
---------------------------

::

    pip install sphinx
    pip install sphinxfeed

Building the documentation (HTML version)
-----------------------------------------

::

    make html

The resulting html documentation will be placed inside the newly created
``build/html`` directory.


Deactivating the virtual environment
------------------------------------

You can deactivate your virtual environment by running the following command in
the root directory of the git repository:

::

    deactivate

Your prompt will reset back to its normal state.  You can re-enter the virtual
environment again by simply running the ``source venv/bin/activate`` command
again.  You will not need to re-install the dependencies again.
