# -*- coding: utf-8 -*-
'''
Class 4 Lab - Pandas Practice with US Presidential Elections Data
'''
# Standard imports for data analysis packages in Python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Make the Plots Pretty - More style options - http://matplotlib.org/users/style_sheets.html
plt.style.use("fivethirtyeight")

# Limit rows displayed
pd.set_option('display.max_rows', 10)
pd.set_option('display.precision', 4)

# Let's explore Presidential Elections Dataset

pres_2004 = pd.read_csv('../data/us_pres_elections/2004_election_results.csv')

# last 5 rows


pres_2004.info()
# Do you see any missing data?

# What columns Exists?
pres_2004.columns

# Notice that 'Bush' has a space in the front.
# Replace column name
pres_2004.rename(columns={' Bush': 'republican', 
                          'Kerry': 'democrat',
                  'All Others': 'others', 
                  'Total Vote': 'total'
                  }, inplace=True)

# Now add a NEW Column and set it to 2004.  We are going to merge files later
pres_2004['year'] = 2004

# print first 5 rows
pres_2004.head()

# Read in 2008 and Append the rows of 2008 with 2004

pres_2008 = pd.read_csv('../data/us_pres_elections/2008_election_results.csv')
pres_2008['year'] = 2008

pres_2008.info()

pres_2008.rename(columns={'McCain': 'republican', 
                          'Obama': 'democrat',
                          'State': 'STATE',
                  'All Others': 'others', 
                  'Total Vote': 'total'
                  }, inplace=True)

# Read in 2012 Election results
pres_2012 = pd.read_csv('../data/us_pres_elections/2012_election_results.csv')
pres_2012['year'] = 2012

pres_2012.head()

pres_2012.rename(columns={'Romney': 'republican', 
                          'Obama': 'democrat',
                  'All Others': 'others', 
                  'Total Vote': 'total'
                  }, inplace=True)
                  
pres_2012.info()

## Rename the columns

## Your Turn


# Verify that all three dataframes have same columns
pres_2004.columns
pres_2008.columns
pres_2012.columns

## Let's Merge the three data frames - Use concat to append on rows
pres_votes = pd.concat([pres_2004, pres_2008, pres_2012])
pres_votes.head()

# Describe
pres_votes.describe()

# Lets check the datatype of columns
pres_votes.info()

# Let's convert the string value for votes into numbers
# Method 1
# Do this for Bush, Kerry, All Others, Total Votes
def convert_val_to_numb(val):
    val = val.strip()  # First Strip any empty space
    val = val.replace(',', '')  # Next, remove any thousands separator
    return val
        
# Test the function
print convert_val_to_numb('100,000')

# Now use the convert val to number function to convert the votes for each candidate
pres_votes['democrat'] = pres_votes['democrat'].map(convert_val_to_numb)

# Let's see if Kerry's vote was converted to numbers
pres_votes.head()

# confirm by looking up the datatype
pres_votes.info()

# What gives?
pres_votes['democrat']

# Note:Pandas may not convert the Datatype from object (string) to int
# You will have to convert it by calling astype function
pres_votes['democrat'] = pres_votes['democrat'].map(convert_val_to_numb).astype(int)
pres_votes['republican'] = pres_votes['republican'].map(convert_val_to_numb).astype(int)
pres_votes['others'] = pres_votes['others'].map(convert_val_to_numb).astype(int)
pres_votes['total'] = pres_votes['total'].map(convert_val_to_numb).astype(int)


## Method 2 - pres_votes.democrat.map(lambda x: x.strip().replace(',', '')).astype(int)


# Try describe now.
pres_votes.describe()

# How Many Total Votes did Republicans or democrats get?
pres_votes[['democrat', 'republican']].sum()

# That's not that useful. Let's do it by Year
pres_votes.groupby('year')[['democrat', 'republican']].sum()


# Lets create two new columns 'dem_pct' and 'rep_pct' for % of votes they got in each state
pres_votes['dem_pct'] = pres_votes['democrat'] / pres_votes['total']
pres_votes['rep_pct'] = pres_votes['republican'] / pres_votes['total']


# Let's look at what the dataframe contains
pres_votes.head()

# But we need is Electoral Votes to decide the winner

# OK Now, read the "electoral_votes_by_state.csv" Dataset.  What do you see
# Call it electoral_votes
electoral_votes = pd.read_csv('../data/us_pres_elections/electoral_votes_by_state.csv')

electoral_votes.head()

electoral_votes.info()

# Merge Electoral votes with pres_votes to see who won and by how many electoral votes
results = pres_votes.merge(electoral_votes, on='STATE', how='inner')

# Award the electoral Votes to the candidate that had the most votes in the stae
# How much did Kerry and Bush get?
def get_dem_ev(row):
    if row.democrat > row.republican:
        return row['Electoral Votes']
    return 0

def get_rep_ev(row):
    if row.republican > row.democrat:
        return row['Electoral Votes']
    return 0

results['ev_dem'] = results.apply(get_dem_ev, axis=1)
results['ev_rep'] = results.apply(get_rep_ev, axis=1)

results.head()

results[['year', 'STATE', 'democrat', 'republican', 'ev_dem', 'ev_rep']].head()

## Questions:

# Give electoral vote counts for the three elections (04, 08, 12) by Party Afiliation

# What States are safely Republican and Democrat.

# What states always went to the Winner (Swing States?)

# What states changed hands between 2008 and 2012?

# In what states did we see largest % dip in voter turnout between 2008 and 2012?
# Did that matter more to Republican or Democrat?
