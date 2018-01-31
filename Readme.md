
# Log Analysis Readme

To run this program, first you will need to create the SQL views, then run python in terminal with "python Log_Analysis.py" in directory with files.

# Files

-  Log_Analysis.py
-  Output.txt
-  Readme.txt

# Purpose

- This project is for Udacity's Full Stack Nanodegree program.
- "You've been hired onto a team working on a newspaper site. The user-facing newspaper site frontend itself, and the database behind it, are already built and running. You've been asked to build an internal reporting tool that will use information from the database to discover what kind of articles the site's readers like."
- "You will get practice interacting with a live database both from the command line and from your code. You will explore a large database with over a million rows. And you will build and refine complex queries and use them to draw business conclusions from data."

# How To

- First I would recommend getting Vagrant using these instructions - [here](https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0)
- This is the database data used - [from udacity](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
- First build sql views in vagrant
- Then run in terminal - "python Log_Analysis.py"

# Create Views
In top_articles():

    CREATE VIEW articlesQuery as
                SELECT path, count(*) as num
                FROM log
                WHERE status = '200 OK'
                AND NOT path = '/'
                GROUP by path
                ORDER BY num DESC;
In top_authors():

    CREATE VIEW authorsQuery as
                SELECT author, count(*) as num
                FROM articles, log
                WHERE log.path = concat('/article/', articles.slug)
                GROUP BY articles.author
                ORDER by num desc;

In errors():

    CREATE VIEW totalRequests as
		        SELECT time ::timestamp::date, count(*) as rqst
		        FROM log GROUP BY time ::timestamp::date;

    CREATE VIEW totalFails as
		        SELECT time ::timestamp::date, count(*) as num404
		        FROM log WHERE status != '200 OK'
		        GROUP BY time ::timestamp::date
		        ORDER BY time ::timestamp::date;

    CREATE VIEW percentFail as
		        SELECT totalRequests.time, (totalFails.num404::FLOAT) / (totalRequests.rqst::FLOAT) * 100 as percent
		        FROM totalRequests join totalFails on totalRequests.time = totalFails.time;
