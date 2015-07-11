'''
Move this code into your OWN SF_DAT_15_WORK repo

Please complete each question using 100% python code

If you have any questions, ask a peer or one of the instructors!

When you are done, add, commit, and push up to your repo

This is due 7/1/2015
'''

from __future__ import division  # Because we almost always want / to be floating point
import pandas as pd
import matplotlib.pyplot as plt
# pd.set_option('max_colwidth', 50)
# set this if you need to

killings = pd.read_csv('https://raw.githubusercontent.com/sinanuozdemir/SF_DAT_15/master/hw/data/police-killings.csv')
killings.head()

# 1. Make the following changed to column names:
# lawenforcementagency -> agency
# raceethnicity        -> race
killings.columns
killings.rename(
    columns={'lawenforcementagency':'agency',
             'raceethnicity':'race'}, 
    inplace=True)
killings.columns

# 2. Show the count of missing values in each column
killings.isnull().sum()
# Answer: Four Nulls in streetaddress column
# This pattern of putting answers inline as comments is something I copied from Chris Cronin's submission
# 3. replace each null value in the dataframe with the string "Unknown"
killings.fillna(value='Unkown', inplace = True)
killings.isnull().sum()

# 4. How many killings were there so far in 2015?
killings.year.value_counts()
#  Since the data only has 2015, the above only shows the total count, but does not show the year
killings.groupby('year').year.count()  # Shows year and count
# Answer: Four Hundred and Sixty-Seven

# 5. Of all killings, how many were male and how many female?
killings.gender.value_counts()
# Answer: Four Hundred and Forty-Five Male, Twenty-Two Female

# 6. How many killings were of unarmed people?
killings.armed[killings.armed=='No'].value_counts()
# Answer: One Hundred & Two people unarmed

# 7. What percentage of all killings were unarmed?
unarmed_killings = killings.armed[killings.armed=='No'].value_counts()
unarmed_killings / killings.shape[0]
unarmed_killings / len(killings)  # ALternative solution
# Answer: 21.8%

# 8. What are the 5 states with the most killings?
killings.state.value_counts().head(5)

# 9. Show a value counts of deaths for each race
killings.race.value_counts()
# Answer: 236 were wite, 135 Black, 67 Hispanic/Latino, 15 Unkown, 10 A/P, 4 NA

# 10. Display a histogram of ages of all killings
ax = killings.age.hist(bins=20)
ax.set_xlabel('Age')
ax.set_ylabel('Count')
ax.set_title('Histogram of Ages of All Killings')
# Notice how I capture the reutrn of hist function into an axis variable
# Then I use the axis varialbe to set x_label, y_label and titile
# This is a common pattern you will find in using matplotlib with Pandas.

# 11. Show 6 histograms of ages by race
killings.age.hist(by=killings.race,sharex=True, sharey=True)

# 12. What is the average age of death by race?
killings.groupby('race').age.mean()

# 13. Show a bar chart with counts of deaths every month
# I am creating a new column called month_num so that I can order the month values
# This solution is based on a Chris Cronin's answer that I really liked
killings['month_num'] = killings.month.replace({
                                                'January':1,
                                                'February':2,
                                                'March':3,
                                                'April':4,
                                                'May':5,
                                                'June':6
                                            })
counts = killings.groupby('month_num').month_num.count()
counts.index = ['January', 'February', 'March', 'April', 'May', 'June']
ax = counts.plot(kind = 'bar',title='Deaths per Month')
ax.set_xlabel('Month')
ax.set_ylabel('Count')

###################
### Less Morbid ###
###################

majors = pd.read_csv('https://raw.githubusercontent.com/sinanuozdemir/SF_DAT_15/master/hw/data/college-majors.csv')
majors.head()

# 1. Delete the columns (employed_full_time_year_round, major_code)
del majors['Employed_full_time_year_round']
del majors['Major_code']

# 2. Show the cout of missing values in each column
majors.isnull().sum()

# 3. What are the top 10 highest paying majors?
majors.sort_index(by='P75th', ascending = False)[['Major','P75th']].head(10)

# One of the student asked me this what if question -
# What if the question was what is the top ten highest paying major categories?
majors.groupby('Major_category')[['P75th']].max().sort_index(by='P75th', ascending=False).head(10)

# 4. Plot the data from the last question in a bar chart, include proper title, and labels!
top_ten_pay = majors.sort_index(by='P75th', ascending = False)[['Major','P75th']].head(10)
ax = top_ten_pay.plot(x='Major',y='P75th',kind='barh',title='Top Ten Paying Majors')
ax.set_xlabel('Major')
ax.set_ylabel('75th Percentile')

# 5. What is the average median salary for each major category?
majors.groupby('Major_category')[['Median']].mean().sort_index(by='Median', ascending=False)
# Alternative Solution that produces Series instead of DataFrame as above.
# Notice that to make this into a DF,I used the [[column]] syntax to force it to DF
majors.groupby('Major_category').Median.mean().order(ascending=False).head(5)

# 6. Show only the top 5 paying major categories
majors.groupby('Major_category')[['P75th']].mean().sort_index(by='P75th', ascending=False).head(5)
# ALternatively -
majors.groupby('Major_category').P75th.mean().order(ascending=False).head(5)

# 7. Plot a histogram of the distribution of median salaries
ax = majors.Median.hist(bins=20)
ax.set_xlabel('Median Salaries')
ax.set_ylabel('Major Count')
ax.set_title('Distribution of Median Salaries')

# 8. Plot a bar chart of the distribution of median salaries by major category

majors.groupby('Major_category')[['Major_category','Median']].mean().sort_index(by='Median').plot(kind='barh')

# Alternative solution that I liked from Daniel Sacks - notice how he's filtering on DF First before doing groupby
majors[['Major_category','Median']].groupby('Major_category').mean().sort_index(by='Median').plot(kind='bar')

# 9. What are the top 10 most UNemployed majors?
# What are the unemployment rates?
majors.sort_index(by='Unemployed', ascending = False)[ ['Major','Unemployed','Unemployment_rate']].head(10)

# 10. What are the top 10 most UNemployed majors CATEGORIES? Use the mean for each category
# What are the unemployment rates?
majors.groupby('Major_category')[['Unemployed', 'Unemployment_rate']].mean().sort_index(by='Unemployed', ascending = False).head(10)

# 11. the total and employed column refer to the people that were surveyed.
# Create a new column showing the emlpoyment rate of the people surveyed for each major
# call it "sample_employment_rate"
# Example the first row has total: 128148 and employed: 90245. it's 
# sample_employment_rate should be 90245.0 / 128148.0 = .7042
majors['sample_employment_rate'] = majors.Employed / majors.Total
majors.head()

# 12. Create a "sample_unemployment_rate" colun
# this column should be 1 - "sample_employment_rate"
majors['sample_unemployment_rate'] = 1 - majors.sample_employment_rate
majors.head()