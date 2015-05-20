Ideal Course
============

Objective
---------
Given a query, return top-20 most relevant courses in NYU to the query.

Demo
----
[http://cs.nyu.edu/~xy644/index.html](http://cs.nyu.edu/~xy644/index.html)

Prerequisites
-------------
Python 2.6, NLTK 3.0.2.

Files
-----
**IdealCourse.pdf**: Project write-up.

**interactive.py**: An interactive version of the project which can be run in local terminal. Recommended for testing, for deploying server version would require more steps.

**preprocess.py**: Preprocess all supplementary and short description documents into a form of bag of words.

**stopwords.pickle**: Stopwords used in the project.

**idftable\_desc.pickle**: For every word, the number of supplementary documents that contain this word is stored.

**idftable.pickle**: For every word, the number of short description documents that contain this word is stored.

**extend.json**: All information for every course including bag of words version of description and supplementary documents are stored. Duplicate courses (differ only on course number) are also removed.

**IdealCourseData**: All data needed for preprocessing.

Get Repository
--------------
Without raw data: ```git clone https://github.com/19thhell/IdealCourse```

With raw data: ```git clone https://github.com/19thhell/IdealCourse --recursive```

How to Test
-----------
An interactive command line version of program is provided as **interactive.py**, may take a few minutes to load data set when running on CIMS servers. Average response time is within 10 seconds.

Run following command in *YOUR_DIR* for interactive test:

```python interactive.py```

An empty query terminates the loop.

Access [http://cs.nyu.edu/~NET_ID](#) for further test. Average response time is 10 to 15 seconds.
