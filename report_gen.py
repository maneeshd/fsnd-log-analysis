
#!/usr/bin/env python3
"""
Author: Maneesh Divana <maneeshd77@gmail.com>
Date: 01-01-2019
Python Interperter: 3.5.2

Log Analysis Report Generator
"""
from traceback import print_exc
from psycopg2 import connect as psql_connect


Q1 = """What are the most popular three articles of all time?"""

Q2 = """Who are the most popular article authors of all time?"""

Q3 = """On which days did more than 1% of requests lead to errors?"""

# DB View Statements for auto-generation in constructor
TOP_ARTICLES_VIEW = """CREATE OR REPLACE VIEW top_articles AS
SELECT A.title, A.author, COUNT(*) AS views
FROM articles AS A, log AS L
WHERE L.path=CONCAT('/article/', A.slug)
GROUP BY A.title, A.author
ORDER BY views DESC;"""

TOP_AUTHORS_VIEW = """CREATE OR REPLACE VIEW top_authors AS
SELECT U.name AS author, SUM(SUBQ.views) AS agg_views
FROM (SELECT A.title, A.author, COUNT(*) AS views
FROM articles AS A, log AS L
WHERE L.path=CONCAT('/article/', A.slug)
GROUP BY A.title, A.author) AS SUBQ, authors AS U
WHERE SUBQ.author=U.id
GROUP BY U.name
ORDER BY agg_views DESC;"""

ERROR_LOG_VIEW = """CREATE OR REPLACE VIEW error_log AS
SELECT SUBQ.day, SUBQ.error_rate
FROM (SELECT DATE(time) AS day,ROUND(100.0*SUM(CASE status WHEN '200 OK'
THEN 0 ELSE 1 END)/COUNT(status), 2) AS error_rate
FROM log GROUP BY day) AS SUBQ
WHERE SUBQ.error_rate>1.0
ORDER BY error_rate DESC;"""


class ReportGen:
    """
    Generate Log Analysis Report
    """
    def __init__(self, db_name="news", create_views=True):
        """
        Constructor for ReportGen class

        :param db_name: PostgreSQL DB name to connect to
        :param create_views: If True will create the views mentioned above
        :return: None
        """
        self.db_con = None
        self.cursor = None
        try:
            # Connect to database and create a cursor
            self.db_con = psql_connect("dbname={0}".format(db_name))
            self.cursor = self.db_con.cursor()

            if create_views:
                # Create views
                self.cursor.execute(TOP_ARTICLES_VIEW)
                self.db_con.commit()
                self.cursor.execute(TOP_AUTHORS_VIEW)
                self.db_con.commit()
                self.cursor.execute(ERROR_LOG_VIEW)
                self.db_con.commit()
        except Exception as error:
            raise error

    def __del__(self):
        """
        Destructor for ReportGen class

        :return: None
        """
        if self.cursor:
            self.cursor.close()
        if self.db_con:
            self.db_con.close()

    def get_top_3_articles(self):
        """
        Get the Top-3 articles accessed

        :return: List of Tuples
        """
        try:
            query = "SELECT title, views FROM top_articles LIMIT 3;"
            self.cursor.execute(query)
            output = self.cursor.fetchall()
            return output
        except Exception as exp:
            raise exp

    def get_popular_authors(self):
        """
        Get the most popular authors

        :return: List of Tuples
        """
        try:
            query = "SELECT author, agg_views FROM top_authors;"
            self.cursor.execute(query)
            output = self.cursor.fetchall()
            return output
        except Exception as exp:
            raise exp

    def get_most_error_logged_days(self):
        """
        Get the days where HTTP errors logged is more than 1%

        :return: List of Tuples
        """
        try:
            query = "SELECT day, error_rate FROM error_log;"
            self.cursor.execute(query)
            output = self.cursor.fetchall()
            return output
        except Exception as exp:
            raise exp


def main():
    """
    Report Generator

    :return: None
    """
    report_gen = None
    try:
        # Create ReportGen object
        report_gen = ReportGen()

        # Question 1
        print("\n" + Q1 + "\n")
        data = list(report_gen.get_top_3_articles())
        for idx, element in enumerate(data):
            article, views = element
            print("\t{0}. {1} ----> {2}".format(idx + 1, article, views))

        # Question 2
        print("\n" + Q2 + "\n")
        data = list(report_gen.get_popular_authors())
        for idx, element in enumerate(data):
            author, agg_views = element
            print("\t{0}. {1} ----> {2}".format(idx + 1, author, agg_views))

        # Question 3
        print("\n" + Q3 + "\n")
        data = list(report_gen.get_most_error_logged_days())
        for idx, element in enumerate(data):
            day, error_rate = element
            print("\t{0}. {1} ----> {2}%".format(idx + 1,
                                                 day.strftime("%B %m, %Y"),
                                                 error_rate))
    except Exception as runtime_error:
        print("[ERROR] Unexpected error has occurred:", runtime_error)
        print_exc()
    finally:
        print("")
        if report_gen:
            del report_gen


if __name__ == "__main__":
    main()
