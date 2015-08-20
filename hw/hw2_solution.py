##### Part 1 #####
from __future__ import division
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

print 'MAE:', mean_absolute_error(y_pred, y_test)
print 'RMSE:', np.sqrt(mean_squared_error(y_pred, y_test))
print 'R-Squared:', r2_score(y_pred, y_test)

# 4. Use statsmodels to show your pvalues
# for each of the three predictors
# Using a .05 confidence level, 
# Should we eliminate any of the three?
import statsmodels.formula.api as smf

lm = smf.ols(formula='stars ~ cool + useful + funny', data=yelp).fit()
print lm.pvalues
lm.summary()
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
features = ['cool', 'useful', 'funny']
X = yelp[features]
y = yelp.good_rating
X_train, X_test, y_train, y_test = train_test_split(X, y)
logreg.fit(X_train, y_train)

# 7. Show your Accuracy, Sensitivity, Specificity
# and Confusion Matrix
y_pred = logreg.predict(X_test)
from sklearn.metrics import confusion_matrix
print confusion_matrix(y_test, y_pred)
true_positive = np.sum((y_test == 1) & (y_pred == 1))  # True Positive
true_negative = np.sum((y_test == 0) & (y_pred == 0))  # True Negative
false_positive = np.sum((y_test == 0) & (y_pred == 1))  # Actual 0, Predicted 1 
false_negative = np.sum((y_test == 1) & (y_pred == 0))  # Actual 1, Predicted 0

print "Accuracy Score: ", np.sum(y_pred == y_test) / y_pred.shape[0]
print "Sensitivity: ", true_positive / (true_positive + false_negative)
print "Specificity: ", true_negative / (true_negative + false_positive)

# 8. Perform one NEW operation of your 
# choosing to try to boost your metrics!
# Get Predicted Probability to improve metric
def get_classification_scores(logreg, prob_cutoff, X_test, y_test):
    y_pred_proba = logreg.predict_proba(X_test)  # Returns a 2-D Array with prediction for 0 and 1
    y_pred_proba_1 = y_pred_proba.take(1, axis=1)  # Get the Probability for value == 1 value
    y_pred = (y_pred_proba_1 >= prob_cutoff).astype(int)
    true_positive = np.sum((y_test == 1) & (y_pred == 1))  # True Positive
    true_negative = np.sum((y_test == 0) & (y_pred == 0))  # True Negative
    false_positive = np.sum((y_test == 0) & (y_pred == 1))  # Actual 0, Predicted 1 
    false_negative = np.sum((y_test == 1) & (y_pred == 0))  # Actual 1, Predicted 0\
    return {
        'accuracy': np.sum(y_pred == y_test) / y_pred.shape[0],
        'sensitivity': true_positive / (true_positive + false_negative),
        'specificity': true_negative / (true_negative + false_positive)
    }

# First get the 0.5 Cutoff    
logreg_metrics = get_classification_scores(logreg, 0.5, X_test, y_test)
print "Prob Cutoff:{prob}, Accuracy: {accuracy}, Sensitivity {sensitivity}, Specificity {specificity}".format(prob=0.5, **logreg_metrics)

# Now move the cutoff to 0.6 to reduce the false Positives
logreg_metrics = get_classification_scores(logreg, 0.6, X_test, y_test)
print "Prob Cutoff:{prob}, Accuracy: {accuracy}, Sensitivity {sensitivity}, Specificity {specificity}".format(prob=0.6, **logreg_metrics)

logreg_metrics = get_classification_scores(logreg, 0.6, X_test, y_test)
print "Prob Cutoff:{prob}, Accuracy: {accuracy}, Sensitivity {sensitivity}, Specificity {specificity}".format(prob=0.7, **logreg_metrics)

## As you can see, I traded off Sensitivity for Specificity
# Your answers may vary


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

# First get the 0.5 Cutoff    
logreg_metrics = get_classification_scores(logreg, 0.5, X_test, y_test)
print "Prob Cutoff:{prob}, Accuracy: {accuracy}, Sensitivity {sensitivity}, Specificity {specificity}".format(prob=0.5, **logreg_metrics)


# 8. Show Accuracy, Sensitivity, Specificity and 
# Confusion matrix
## Done above

# 9. now use ANY of your variables as predictors
# Still using survived as a response to boost metrics!
# Add Class and Sex to the model.
# Convert class to str so that we can do get_dummies and convert it to 0 and 1's.
titanic['Pclass'] = titanic.Pclass.astype(str)

logreg = LogisticRegression()
features = ['wife', 'Age', 'Sex', 'Pclass']
X = titanic[features]
X = pd.get_dummies(X)
y = titanic.Survived
X_train, X_test, y_train, y_test = train_test_split(X, y)
logreg.fit(X_train, y_train)

y_pred = logreg.predict(X_test)
print confusion_matrix(y_test, y_pred)

# 10. Show Accuracy, Sensitivity, Specificity
logreg_metrics = get_classification_scores(logreg, 0.5, X_test, y_test)
print "Prob Cutoff:{prob}, Accuracy: {accuracy}, Sensitivity {sensitivity}, Specificity {specificity}".format(prob=0.5, **logreg_metrics)

## We were able to increase all three metrics by adding Sex and Pclass to the model

# REMEMBER TO USE
# TRAIN TEST SPLIT AND CROSS VALIDATION
# FOR ALL METRIC EVALUATION!!!!

