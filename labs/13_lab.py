'''
CLUSTER ANALYSIS ON COUNTRIES
'''

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Import the data
d = pd.read_csv('../data/UNdata.csv')
np.random.seed(0)

############################
##### Cluster Analysis #####
############################


# Run KMeans with k = 3 on the UnData
# Use the the following variables: GPDperCapita, lifeMale, lifeFemale, & infantMortality

# Create at least one data visualization (e.g., Scatter plot grid, 3d plot, parallel coordinates)

# Print out the countries present within each cluster. Do you notice any general trend?

# Print out the properties of each cluster. What are the most striking differences?



#################
##### TREES #####
#################

# map the region column to 5 different columns.
# ie you'll have a column called 
# "Africa" with all trues and falses and another column called
# "Europe" that is also all trues and falses
# DON'T DELETE THE REGION COLUMN


# Use a decision to try and predict infantMortality using the newly made
# 5 region columns and also using lifeMale, lifeFemale and GDPperCapita

# Advanced: use a grid search to make your hunt for the best model better :)



# Use a decision tree to try and predict Region based on 
# lifeMale, lifeFemale and GDPperCapita


# What are the most important features in making this prediction
# Is anything striking?


# Using a cross-val-score as a guide and the accuracy as a metric, use several classification
# techniques in order to get the best model possible to predict Region
# SO try KNN, multinomialNB, etc..
# Is there a model that cann't handle more than 2 classes?
# Why can't we use ROC/AUC for this?



