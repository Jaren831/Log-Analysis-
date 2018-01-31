#!/usr/bin/env python3 for Python 3

import psycopg2


def top_articles():
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute(
        """
         CREATE VIEW articlesQuery as
            SELECT path, count(*) as num
            FROM log
            WHERE status = '200 OK'
            AND NOT path = '/'
            GROUP by path
            ORDER BY num DESC;

        SELECT title, num
          FROM articles, articlesQuery
          WHERE articlesQuery.path = CONCAT('/article/', slug)
          ORDER BY num DESC LIMIT 3;
        """
    )
    results = c.fetchall()
    print("Question 1: What are the most popular three articles of all time?")
    for row in results:
        print(str(row[0]) + "-" + str(row[1]))
    db.close()


def top_authors():
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute(
        """
        CREATE VIEW authorsQuery as
            SELECT author, count(*) as num
            FROM articles, log
            WHERE log.path = concat('/article/', articles.slug)
            GROUP BY articles.author
            ORDER by num desc;

        SELECT * FROM authorsQuery;
        SELECT name, num
          FROM authors, authorsQuery
          WHERE authorsQuery.author = authors.id
        """
    )
    results = c.fetchall()
    print("Question 2: Who are the most popular "
          "article authors of all time?")
    for row in results:
        print(str(row[0]) + "-" + str(row[1]))
    db.close()


def errors():
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute(
        """
        CREATE VIEW totalRequests as
            SELECT time ::timestamp::date, count(*) as rqst
            FROM log GROUP BY time ::timestamp::date;

        CREATE VIEW totalFails as
            SELECT time ::timestamp::date, count(*) as num404
            FROM log WHERE status != '200 OK'
            GROUP BY time ::timestamp::date
            ORDER BY time ::timestamp::date;

        CREATE VIEW percentFail as
            SELECT totalRequests.time,
            (totalFails.num404::FLOAT) /
            (totalRequests.rqst::FLOAT) * 100 as percent
            FROM totalRequests
            join totalFails on totalRequests.time = totalFails.time;

        SELECT time, percent from percentFail;

        SELECT time, percent
            FROM percentFail
            WHERE percent >= 1;
        """
    )
    results = c.fetchall()
    print("Question 3:  On which days did more than "
          "1% of requests lead to errors?")
    for row in results:
        print(str(row[0]) + "-" + str(row[1]))
    db.close()


top_articles()
top_authors()
errors()
