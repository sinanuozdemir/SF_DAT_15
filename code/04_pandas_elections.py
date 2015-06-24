# -*- coding: utf-8 -*-
'''
Class 4 Lab - Pandas Practice with US Presidential Elections Data
'''
# Standard imports for data analysis packages in Python
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Limit rows displayed in notebook
pd.set_option('display.max_rows', 10)
pd.set_option('display.precision', 2)

# Let's explore Presidential Elections Dataset

pres_2004 = pd.read_csv('../data/us_pres_elections/2004_election_results.csv')

# last 5 rows

# do a Info to look at datatypes
pres_2004.info()

# Do you see any missing data?

# What columns Exists?
pres_2004.columns

# Notice that 'Bush' has a space in the front.
# Replace column name ' Bush' with 'Bush'

## Your Turn


# Let's convert the string value for votes into numbers
# Here's a sample - pres_2004.Kerry.map(lambda x: x.strip().replace(',', '')).astype(int)

# Do this for Bush, Kerry, All Others, Total Votes

# Try describe now.

# How Many Total Votes did Bush and Kerry get?

# But we need to get Electoral Votes to decide the winner

# OK Now, read the "electoral_votes_by_state.csv" Dataset.  What do you see
# Call it electoral_votes
electoral_votes = pd.read_csv('../data/us_pres_elections/electoral_votes_by_state.csv')

# Merge Electoral votes with pres_2004 to see who won and by how many electoral votes

# pres_2004.merge(electoral_votes)

# Award the electoral Votes to the candidate that had the most votes in the stae
# How much did Kerry and Bush get?

# Now add a NEW Column and set it to 2004.  We are going to merge files later
pres_2004['year'] = 2004


# Read in 2008 and Append the rows of 2008 with 2004

pres_2008 = pd.read_csv('../data/us_pres_elections/2008_election_results.csv')
pres_2004['year'] = 2008

# your turn
# pres_2004.append

# Read in 2012 Election results too

# your turn

# Create a new list to classify each of the candidates as Democrat or Republican

# your turn

# Now, can you give electoral vote counts for the three elections (04, 08, 12) by Party Afiliation

# your turn

# What States are safely Republican or Democratic.


# Challenge: What states decide the fate of elections?

# Your Turn
