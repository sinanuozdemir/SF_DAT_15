'''
CLASS: Reading and Writing Files in Python
'''

'''
Part 1: Reading files
Note: 'rU' mode (read universal) converts different line endings into '\n'
'''

# read the whole file at once, return a single string
f = open('../data/drinks.csv', 'rU')
f.read()        # one big string including newlines
f.read()        # empty string
f.close()

# read one line at a time (entire file does not have to fit into memory)
f = open('../data/drinks.csv', 'rU')
f.readline()    # one string per line (including newlines)
f.readline()    # next line
f.close()

# read the whole file at once, return a list of lines
f = open('../data/drinks.csv', 'rU')
f.readlines()   # one list, each line is one string
f.close()

# use list comprehension to duplicate readlines without reading entire file at once
f = open('../data/drinks.csv', 'rU')
[row for row in f]
f.close()
# Recall a list comprehension is nothing more than a shortened for loop


# use a context manager to automatically close your file
with open('../data/drinks.csv', 'rU') as f:
    [row for row in f]

# split on commas to create a list of lists
with open('../data/drinks.csv', 'rU') as f:
    [row.split(',') for row in f]

# use the built-in csv module instead
import csv
with open('../data/drinks.csv', 'rU') as f:
    [row for row in csv.reader(f)]

# use next to grab the next row
with open('../data/drinks.csv', 'rU') as f:
    header = csv.reader(f).next()
    data = [row for row in csv.reader(f)]


'''
Part 2: Writing files
Note: 'wb' mode (write binary) is usually the recommended option
'''

# write a string to a file
nums = range(5)
with open('nums.txt', 'wb') as f:
    for num in nums:
        f.write(str(num) + '\n')

# convert a list of lists into a CSV file
output = [['col1', 'col2', 'col3'], [4, 5, 6]]
with open('example.csv', 'wb') as f:
    for row in output:
        csv.writer(f).writerow(row)

# use writerows to do this in one line
with open('example.csv', 'wb') as f:
    csv.writer(f).writerows(output)
    
    
    
''' 
Part 3, taking data from the web and graphing it
'''

import requests # a module for reading the web
api_endpoint = 'http://api.openweathermap.org/data/2.5/weather/forecast'
params = {}
params['id'] = '745044'
params['units'] = 'metric'
params['APPID'] = '80575a3090bddc3ce9f363d40cee36c2'
request = requests.get(api_endpoint, params = params)

# A request objects
request
# Note response of 200 is OK!

# Look at the text
request.text

# OH It's a JSON (javascript object notation) Good thing
# requests has a built in json function

# parse out the json from this request
data = request.json()

# Let's inspect by using the keys method of dictionaries
data.keys()

data['city']

data['cnt']

data['list']

### POP LEARNING OPPORTUNITY ###
# How many items are in this list? What is the first one?






### ANSWER ###
len(data['list']) # == 36
data['list'][0]


# Let's store the lists as their own variables

weather_data = data['list']

# use a list comprehension to get the dates and temperatures out of the data



temperatures = [data_point['main']['temp'] for data_point in weather_data]

# Average temperature
sum(temperatures) / len(temperatures)

# range of temperatures
min(temperatures), max(temperatures)



dates = [data_point['dt'] for data_point in weather_data]
# the dates are in EPOCH, which is standard
# The number is the number of seconds since January 1st, 1970
# Luckily we can easily convert to a python standard, datetime!

from datetime import datetime
dates = [datetime.fromtimestamp(epoch) for epoch in dates]

dates # now in datetime format




# Data is awesome, and so are graphs
import matplotlib.pyplot as plt

plt.plot(dates, temperatures)


# Awesome! But not that pretty, let's do a makeover
plt.xlabel("Time")                          # set the x axis label
plt.ylabel("Temperature (Celsius)")         # set the y axis label
plt.title("Temperature today in Istanbul")  # set the title
locs, labels = plt.xticks()                 # get the x tick marks
plt.setp(labels, rotation=70)               # rotate the x ticks marks by 70 degrees
plt.plot(dates, temperatures)               # plot again :)

# Plot two things at once!

humidity = [data_point['main']['humidity'] for data_point in weather_data]


plt.legend()                                # Create a legend
plt.plot(dates, humidity, label='Humidity')
plt.plot(dates, temperatures, marker='o', linestyle='--', color='r', label='Temperature')

# OK Not terrible but let's normalize this data..

### POP LEARNING OPPORTUNITY ###
# Let's keep it simple, for each value, divide it by the max in the list
# so for example, if the max temperature is 25.11, a value of 24 becomes
# 24 / 25.11 = 0.956
# Hint, try using a list comprehension!!





### Answer ###


temperatures_normalized = [float(t) / max(temperatures) for t in temperatures]
humidity_normalized = [float(h) / max(humidity) for h in humidity]

plt.legend()
ocs, labels = plt.xticks()                 # get the x tick marks
plt.setp(labels, rotation=70)               # rotate the x ticks marks by 70 degrees
plt.plot(dates, humidity_normalized, label='Humidity')
plt.plot(dates, temperatures_normalized, marker='o', linestyle='--', color='r', label='Temperature')

# Much better!!!



# Let's try a scatter plot!

plt.scatter(temperatures, humidity)


# No discernable pattern, huh?...


