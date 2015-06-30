## SF DAT15 Course Repository

Course materials for [General Assembly's Data Science course](https://generalassemb.ly/education/data-science/san-francisco/) in San Francisco, DC (6/15/15 - 8/26/15).

**Instructors:** Sinan Ozdemir (who is awesome)

**Teaching Assistants:**
Liam Foley, Patrick Foley, and Ramesh Sampath (who are all way more awesome)

**Office hours:** All will be held in the student center at GA, 225 Bush Street

* Monday 5:15-6:15pm
* Tuesday 6:30-8:30pm
* Wednesday 5:15-6:15pm
* Friday 12:30-2:30pm
* Saturday 10:00am-12:00pm

**[Course Project information](project.md)**

Monday | Wednesday
--- | ---
6/15: [Introduction / Expectations / Git Intro](#class-1-introduction--expectations--git-intro) | 6/17: [Python](#class-2-python)
6/22: [Data Science Workflow / Pandas](#class-3-data-science-workflow--pandas) | 6/24: [More Pandas](#class-4---more-pandas)
6/29: [Intro to ML / Numpy / KNN](#class-5--Intro-to-ML--Numpy--KNN) | 7/1: Scikit-learn / Model Evaluation<br>**Project Milestone:** Question and Data Set<br> **HW** Homework 1 Due
7/6: Linear Regression | 7/8: Logistic Regression
7/13: Working on a Data Problem | 7/15: Clustering
7/20: Natural Language Processing| 7/22: Naive Bayes <br>**Milestone:** First Draft Due
7/27: Decision Trees | 7/29:Ensembling Techniques <br>**Milestone:** Peer Review Due
8/3: Recommendation Engines | 8/5: Databases / MapReduce
8/10: TBD | 8/17: TBD| 8/12: TBD
8/17: TBD | 8/17: TBD| 8/19: TBD
8/24: Projects | 8/26: Projects


### Installation and Setup
* Install the [Anaconda distribution](http://continuum.io/downloads) of Python 2.7x.
* Install [Git](http://git-scm.com/book/en/v2/Getting-Started-Installing-Git) and create a [GitHub](https://github.com/) account.
* Once you receive an email invitation from [Slack](https://slack.com/), join our "SF\_DAT\_15 team" and add your photo!

### Resources
* [PEP 8 - Style Guide for Python](http://www.python.org/dev/peps/pep-0008)

### Class 1: Introduction / Expectations / Git Intro
* Introduction to General Assembly
* Course overview: our philosophy and expectations ([slides](slides/01_course_overview.pdf))
* Git overview: ([slides](slides/01_git_github.pdf))
* Tools: check for proper setup of Git, Anaconda, overview of Slack

**Homework:**

* Resolve any installation issues before next class.
* Make sure you have a github profile and created a repo called "SF_DAT_15"
* Clone the class repo (this one!)
* Review this [code](code/00_python_refresher.py) for a recap of some Python basics.

**Optional:**

* Read [Analyzing the Analyzers](http://cdn.oreillystatic.com/oreilly/radarreport/0636920029014/Analyzing_the_Analyzers.pdf) for a useful look at the different types of data scientists.
* Look over Data science overview ([slides](slides/01_course_overview.pdf))
* Read about some [Markdown Techniques](http://daringfireball.net/projects/markdown/syntax)

### Class 2: Python
* Brief overview of Python environments: Python interpreter, IPython interpreter, Spyder, Rodeo
* Python quiz ([code](code/02_python_quiz.py))
* Check out some iPython Notebooks!
* Working with data in Python in Spyder
    * Today's data is brought to you by Nate Silver's blog, [FiveThirtyEight](https://github.com/fivethirtyeight/data/tree/master/alcohol-consumption)
    * and also from the [Open Weather Data Project](http://openweathermap.org/) They have a great API!!
    * Reading, writing, and graphing oh my! in Python ([code](code/02_files_and_weather.py))
* [Lab](code/02_files_and_weather_lab.py) on files and API usage

**Homework:**

* Finish the [Python exercise](code/02_files_and_weather_lab.py) 
* Read through the [project page](project.md) in detail.
* Review a few [projects from past Data Science courses](https://github.com/justmarkham/DAT-project-examples) to get a sense of the variety and scope of student projects.

**Optional:**

* If you need more practice with Python, review the "Python Overview" section of [A Crash Course in Python](http://nbviewer.ipython.org/gist/rpmuller/5920182), work through some of [Codecademy's Python course](http://www.codecademy.com/en/tracks/python), or work through [Google's Python Class](https://developers.google.com/edu/python/) and its exercises.
* For more project inspiration, browse the [student projects](http://cs229.stanford.edu/projects2013.html) from Andrew Ng's [Machine Learning course](http://cs229.stanford.edu/) at Stanford.

**Resources:**

* [Online Python Tutor](http://pythontutor.com/) is useful for visualizing (and debugging) your code.

### Class 3: Data Science Workflow / Pandas

**Agenda**

* Slides on the Data Science workflow [here](slides/03_intro_to_ds.pdf)
	* Data Science Workflow
* Intro to Pandas walkthrough [here](code/03_pandas.py)
	* I will give you semi-cleaned data allowing us to work on step 3 of the data science workflow
	* Pandas is an excellent tool for exploratory data analysis
	* It allows us to easily manipulate, graph, and visualize basic statistics and elements of our data
	* [Pandas Lab!](code/03_pandas_lab.py)


**Homework**

* Begin thinking about potential projects that you'd want to work on. Consider the problems discussed in class today (we will see more next time and next Monday as well)
	* Do you want a predictive model?
	* Do you want to cluster similar objects (like words or other)?

**Resources:**

* Pandas
	 * [Split-Apply-Combine](http://i.imgur.com/yjNkiwL.png) pattern
    * Simple examples of [joins in Pandas](http://www.gregreda.com/2013/10/26/working-with-pandas-dataframes/#joining)
    * Check out this excellent example of [data wrangling and exploration in Pandas](http://nbviewer.ipython.org/github/cs109/content/blob/master/lec_04_wrangling.ipynb)
	    * For an extra challenge, try copying over the code into your own .py file
	* To learn more Pandas, review this [three-part tutorial](http://www.gregreda.com/2013/10/26/intro-to-pandas-data-structures/)
    * For more on Pandas plotting, read the [visualization page](http://pandas.pydata.org/pandas-docs/stable/visualization.html) from the official Pandas documentation.

    
    
### Class 4 - More Pandas

#### Agenda
* Class code on Pandas [here](code/04_pandas_2.py)
* We will work with 3 different data sets today:
	* the UFO dataset (as scraped from the [reporting website](http://www.nuforc.org/webreports.html)	
	* Fisher's Iris Dataset (as cleaned from a [machine learning repository](https://archive.ics.uci.edu/ml/datasets/Iris)
	* A dataset of (nearly) every FIFA goal ever scored (as scraped from the website)
* Pandas Lab! [here](code/04_pandas_2_lab.py)
	
	
####Homework
* Please review the [readme](hw/HW1-README.md) for the first homework. It is due NEXT Wednesday (7/1/2015)
* The one-pager for your project is also due. Please see [project guidelines](project.md)
	
	
### Class 5 - Intro to ML / Numpy / KNN

####Agenda

* Intro to numpy [code](code/05_numpy.py)
	* Numerical Python, code adapted from tutorial [here](http://www.engr.ucsb.edu/~shell/che210d/numpy.pdf)
	* Special attention to the idea of the np.array
* Intro to Machine Learning and KNN [slides](slides/05_ml_knn.pdf)
	* Supervised vs Unsupervised Learning
	* Regression vs. Classification
* Iris pre-work [code](code/05_iris_prework.py) and [code solutions](code/05_iris_prework_solutions.py)
	* Using numpy to investigate the iris dataset further
	* Understanding how humans learn so that we can teach the machine!
* [Lab](code/05_knn.py) to create our own KNN model


####Homework
* The one page project milestone as well as the pandas homework!
* Read this excellent article, [Understanding the Bias-Variance Tradeoff](http://scott.fortmann-roe.com/docs/BiasVariance.html), and be prepared to discuss it in class on Wednesday. (You can ignore sections 4.2 and 4.3.) Here are some questions to think about while you read:
    * In the Party Registration example, what are the features? What is the response? Is this a regression or classification problem?
    * In the interactive visualization, try using different values for K across different sets of training data. What value of K do you think is "best"? How do you define "best"?
    * In the visualization, what do the lighter colors versus the darker colors mean? How is the darkness calculated?
    * How does the choice of K affect model bias? How about variance?
    * As you experiment with K and generate new training data, how can you "see" high versus low variance? How can you "see" high versus low bias?
    * Why should we care about variance at all? Shouldn't we just minimize bias and ignore variance?
    * Does a high value for K cause over-fitting or under-fitting?

    
**Resources:**

* For a more in-depth look at machine learning, read section 2.1 (14 pages) of Hastie and Tibshirani's excellent book, [An Introduction to Statistical Learning](http://www-bcf.usc.edu/~gareth/ISL/). (It's a free PDF download!)

	