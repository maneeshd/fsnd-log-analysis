# Log Analysis Report Generator

Udacity Full Stack Developer Nanodegree Project 1

-----

### Overview

In this project, we execute complex SQL queries on a large database to extract useful and interesting statistics.

The database is part of a newspaper company's web application - containing 3 tables:

1. `articles` - Contains the articles published in the newspaper.
2. `authors` - Contains the authors who have published above articles.
3. `log` - Contains a log of every HTTP request for each article recieved by the server and their status codes and timestamp.

The tool tries to answer these 3 questions:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

-----

### Requirements

- [Python >= 3.5.2](https://www.python.org/downloads/)
- [Vagrant](https://www.vagrantup.com/downloads.html)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)

### Setup

1. Install `Vagrant` and `VirtualBox`.
2. Clone or download [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm) repository.
3. Clone or download [this(fsnd-log-analysis)](https://github.com/maneeshd/fsnd-log-analysis) repository.
4. Download [newsdata.zip](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and unzip to get the `newsdata.sql` file containing the database data.
5. Copy the contents of `fsnd-log-analysis` and file `newsdata.sql` into directory: `fullstack-nanodegree-vm/vagrant/news` (create directory news)
6. Bring up the Vagrant VM inside `fullstack-nanodegree-vm/vagrant` using the following command (you may have to run this commands multiple times):

```
$ cd fullstack-nanodegree-vm/vagrant
$ vagrant up
```
7. Launch the VM using:

```
$ vagrant ssh
```
8. Change directory into `/vagrant/news` & load the database data using:

```
$ cd /vagrant/news
$ psql -d news -f newsdata.sql
```
9. Check connection to database using:

```
$ psql -d news

news=> \dt;
          List of relations
 Schema |   Name   | Type  |  Owner
--------+----------+-------+---------
 public | articles | table | vagrant
 public | authors  | table | vagrant
 public | log      | table | vagrant
(3 rows)

news=> \q
```
10. Check if python package `psycopg2` is installed:

```
$ pip3 list | grep psycopg2
psycopg2-binary     2.7.6.1

    ~ If not present, install it ~

$ pip3 install psycopg2-binary
```

-----

### Running the tool

*Ensure that steps from Setup are completed*

From `/vagrant/news` directory inside VM run using:

```
$ python3 report_gen.py
```

-----
