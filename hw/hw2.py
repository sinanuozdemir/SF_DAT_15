##### Part 1 #####

import pandas as pd

# 1. read in the yelp dataset
yelp = pd.read_csv('../hw/optional/yelp.csv')
# 2. Perform a linear regression using 
# "stars" as your response and 
# "cool", "useful", and "funny" as predictors
from sklearn.linear_model import LinearRegression
features = ['cool', 'useful', 'funny']
X = yelp[features]
y = yelp.stars
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y)

linreg = LinearRegression()
linreg.fit(X_train, y_train)

# 3. Show your MAE, R_Squared and RMSE
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import numpy as np

y_pred = linreg.predict(X_test)

mean_absolute_error(y_pred, y_test)
np.sqrt(mean_squared_error(y_pred, y_test))
r2_score(y_pred, y_test)

# 4. Use statsmodels to show your pvalues
# for each of the three predictors
# Using a .05 confidence level, 
# Should we eliminate any of the three?
import statsmodels.formula.api as smf

lm = smf.ols(formula='stars ~ cool + useful + funny', data=yelp).fit()
lm.pvalues
# They all seem significant!


# 5. Create a new column called "good_rating"
# this could column should be True iff stars is 4 or 5
# and False iff stars is below 4
yelp['good_rating'] = yelp.stars >= 4

# 6. Perform a Logistic Regression using 
# "good_rating" as your response and the same
# three predictors
from sklearn.linear_model import LogisticRegression

logreg = LogisticRegression()
logreg.fit(X_train, y_train)
features = ['cool', 'useful', 'funny']
X = yelp[features]
y = yelp.good_rating
X_train, X_test, y_train, y_test = train_test_split(X, y)

# 7. Show your Accuracy, Sensitivity, Specificity
# and Confusion Matrix
y_pred = logreg.predict(X_test)
from sklearn.metrics import confusion_matrix
print confusion_matrix(y_test, y_pred)


# 8. Perform one NEW operation of your 
# choosing to try to boost your metrics!

# answers may vary


##### Part 2 ######

# 1. Read in the titanic data set.
titanic = pd.read_csv('../data/titanic.csv')

# 4. Create a new column called "wife" that is True
# if the name of the person contains Mrs.
# AND their SibSp is at least 1

titanic['wife'] = (titanic.SibSp >=1) & (titanic.Name.str.contains('Mrs'))

# 5. What is the average age of a male and
# the average age of a female on board?
male_avg_age = titanic[titanic.Sex=='male']['Age'].mean()
male_avg_age

female_avg_age = titanic[titanic.Sex=='female']['Age'].mean()
female_avg_age

# 5. Fill in missing MALE age values with the
# average age of the remaining MALE ages
titanic.Age = np.where((titanic.Age.isnull()) & (titanic.Sex == 'male'), male_avg_age, titanic.Age)

titanic.Age
# 6. Fill in missing FEMALE age values with the
# average age of the remaining FEMALE ages
titanic.Age = np.where((titanic.Age.isnull()) & (titanic.Sex == 'female'), female_avg_age, titanic.Age)


# 7. Perform a Logistic Regression using
# Survived as your response and age, wife
# as predictors
logreg = LogisticRegression()
features = ['wife', 'Age']
X = titanic[features]
y = titanic.Survived
X_train, X_test, y_train, y_test = train_test_split(X, y)
logreg.fit(X_train, y_train)

# 7. Show your Accuracy, Sensitivity, Specificity
# and Confusion Matrix
y_pred = logreg.predict(X_test)
from sklearn.metrics import confusion_matrix
print confusion_matrix(y_test, y_pred)


# 8. Show Accuracy, Sensitivity, Specificity and 
# Confusion matrix


# 9. now use ANY of your variables as predictors
# Still using survived as a response to boost metrics!


# 10. Show Accuracy, Sensitivity, Specificity



# REMEMBER TO USE
# TRAIN TEST SPLIT AND CROSS VALIDATION
# FOR ALL METRIC EVALUATION!!!!

