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
3. Clone or download [current(fsnd-log-analysis)](https://github.com/maneeshd/fsnd-log-analysis) repository.
4. Download [newsdata.zip](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and unzip to get the `newsdata.sql` file containing the database data.
5. Copy the contents of `fsnd-log-analysis` and file `newsdata.sql` into directory: `fullstack-nanodegree-vm/vagrant/news` (create directory news)
6. Bring up the Vagrant VM inside `fullstack-nanodegree-vm/vagrant` using the following command (you may have to run this commands multiple times):

```shell
$ cd fullstack-nanodegree-vm/vagrant
$ vagrant up
```
7. Launch the VM using:

```shell
$ vagrant ssh
```
8. Change directory into `/vagrant/news` & load the database data using:

```shell
$ cd /vagrant/news
$ psql -d news -f newsdata.sql
```
9. Check connection to database using:

```shell
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

```shell
$ pip3 list | grep psycopg2
psycopg2-binary     2.7.6.1

    ~ If not present, install it ~

$ pip3 install psycopg2-binary
```

*Note: The database views required are created by the tool. No need to manually create them. If required look at the `Database Views` section below.*

-----

### Running the tool

*Ensure that steps from Setup are completed*

From `/vagrant/news` directory inside VM run using:

```shell
$ python3 report_gen.py
```

**Sample output can be viewed in [output.txt](output.txt)**

-----

### Database Views

**Database Views required are auto-generated by the tool itself upon initial run.**

The views it generates are:

```sql
CREATE OR REPLACE VIEW top_articles AS
SELECT A.title, A.author, COUNT(*) AS views
FROM articles AS A, log AS L
WHERE POSITION(A.slug in L.path)>0
GROUP BY A.title, A.author
ORDER BY views DESC;

CREATE OR REPLACE VIEW top_authors AS
SELECT U.name AS author, SUM(SUBQ.views) AS agg_views
FROM (SELECT A.title, A.author, COUNT(*) AS views
FROM articles AS A, log AS L
WHERE POSITION(A.slug in L.path)>0
GROUP BY A.title, A.author) AS SUBQ, authors AS U
WHERE SUBQ.author=U.id
GROUP BY U.name
ORDER BY agg_views DESC;

CREATE OR REPLACE VIEW error_log AS
SELECT SUBQ.day, SUBQ.error_rate
FROM (SELECT DATE(time) AS day,ROUND(100.0*SUM(CASE status WHEN '200 OK' THEN 0 ELSE 1 END)/COUNT(status), 2) AS error_rate
FROM log GROUP BY day) AS SUBQ
WHERE SUBQ.error_rate>1.0
ORDER BY error_rate DESC;
```
