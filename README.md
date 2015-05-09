Ideal Course
============

Prerequisite
------------
Python 2.6, NLTK 3.0.2.

Files
-----
**IdealCourse.pdf**: Project write-up.

**interactive.py**: An interactive version of the project which can be run in local terminal. Recommended for testing, for deploying server version would require more steps.

**source_code.tar.gz**: Source code and relevant data to deploy and run project.

**scrapy.tar.gz**: Source code for scraping raw data from web. THE CODE CAN BE RUN ON CIMS SERVER, BUT IS NOT RECOMMENDED, STORAGE ON CIMS SERVER IS NOT LARGE ENOUGH TO STORE ALL DATA AND IT TAKES MORE THAN ONE WEEK TO FINISH.

How to Test
-----------
An interactive command line version of program is provided as **interactive.py**, may take a few minutes to load data set when running on CIMS servers. Average response time is within 10 seconds.

An empty query terminates the loop. Strongly recommend to use this code for testing, since deploying a server version could be troublesome. Extract **source_code.tar.gz** under *YOUR_DIR*, then run following command in *YOUR_DIR* for interactive test:

```python interactive.py```

How to Deploy
-------------
Extract **source_code.tar.gz** into *$HOME/public_html* (backup everything before extracting).

Run

```python server.py```

on *crunchy6*.

Access http://cs.nyu.edu/~NET\_ID for further test. Average response time is 10 to 15 seconds.

Demo
----
[http://cs.nyu.edu/~xy644/index.html](http://cs.nyu.edu/~xy644/index.html)
