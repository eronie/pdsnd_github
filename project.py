import time
import datetime
import pandas as pd
import numpy as np
from os import system, name

# Created using Python 3.8.3, NumPy 1.19.0, Pandas 1.0.5


CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def resetScreen():
    """Clears the screen."""

    system('cls')
    print('\n\n\n')

def userChoiceMenuList(question, itemList, clrScreen):
    """Given a question and options, creates a vertical list of options to choose from.
    Can choose to clear the screen before using or not, depending on use case."""

    numListItems = len(itemList) -1
    userChoice = -1
    invalidInput = False
   
    while userChoice <0 or userChoice > numListItems:
        if clrScreen == True: 
            resetScreen()
        itemNumber = 0
        for item in itemList:
            print('     {} :  {}'.format(itemNumber, item))
            itemNumber += 1
        
        if invalidInput == True:
            print('\n  That is an invalid choice. Please try again.')
            
        userChoice = input('\n' + question + '\n')
        
        if userChoice in ('0','1','2','3','4','5','6','7','8','9'):
            userChoice = int(userChoice)
        else:
            userChoice = -1
            
        invalidInput = True
        
    return userChoice, itemList[userChoice]

def proceedBool(question):
    """Given a question, creates a yes or no option."""
    userChoice  = ''
    invalidInput = False
    options = ('y', 'n')
    while userChoice not in options:
        if invalidInput ==True:
            print('That\'s not a valid answer.')
        userChoice = input('{} y or n?: '.format(question))
        invalidInput = True
        if userChoice == 'y':
            proceed = True
        else: proceed = False
    return proceed

def getCity():
    """Allows user to choose the city from which they'd like to view data."""

    cities = ('Chicago', 'New York City', 'Washington')
    question = 'Which city would you like to explore?'
    answer = userChoiceMenuList(question, cities, True)
    city = answer[1]
    print('You are searching ... ' + city)
    time.sleep(1)
    return city

def getInterval():
    """Allows user to choose to sort by Month, Day, or All data. If user chooses month, 
    they will choose the specific month. If user chooses day, they will choose the day of the week."""

    intervals = ('Month', 'Day', 'All')
    question = 'You can explore the data by month, by day of the week or all data.\nWhich would you prefer?'
    interval = userChoiceMenuList(question, intervals, True)
    print('You are searching by ... ' +interval[1]) 
    time.sleep(1)
    monthChoice = 'All'
    dayChoice = 'All'
        
    if interval[1] == 'Month':
        months = ('January', 'February', 'March', 'April', 'May', 'June')
        monthQuestion = 'All data is from the first half of the year. You can choose any month from January to June.'
        monthChoice = userChoiceMenuList(monthQuestion, months, True)
        print('You are searching ... ' + monthChoice[1])
        time.sleep(1)
   
    if interval[1] == 'Day':
        days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
        DayQuestion = 'Which day of the week?'
        dayChoice = userChoiceMenuList(DayQuestion, days, True)
        print('You are searching ... ' +dayChoice[1]+'s')
        time.sleep(1)
    
    return interval, monthChoice, dayChoice


def load_data(city, interval, monthChoice, dayChoice):
    """Uses user choices from other functions to load the dataframe."""

    df = pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month_name()
    df['day'] = df['Start Time'].dt.day_name()
    
    
    if interval[0] == 0:
        df = df[df['month'] == monthChoice[1]]

    if interval[0] == 1:
        df = df[df['day'] == dayChoice[1]]
    
    return df

def travelStats(df, city, monthChoice, dayChoice, interval):
    """Displays travel statistics using user information from the getCity and getInterval functions."""

    resetScreen()
    print('You are viewing Bikeshare data on {} sorted by {}.\n'.format(city, interval[1]))
    print('Travel information based on month, day, and hour:')
    popularMonth = df.mode()['month'][0]
    popularDay = df.mode()['day'][0]
    popularHour = int(df.mode()['hour'][0])
    
    if interval[0] == 0:
        print('The most popular day for travel during {} was {}.'.format(monthChoice[1], popularDay))
        print('The most popular hour of travel during {} was {}:00.'.format(monthChoice[1], popularHour))
    
    elif interval[0] == 1:
        print('People traveled the most on {}s in {}.'.format(dayChoice[1], popularMonth))
        print('The most popular hour of travel on {}s was {}:00.'.format(dayChoice[1], popularHour))
    
    else:
        print('The most traveled month was {}.'.format(popularMonth))
        print('The most traveled day was {}.'.format(popularDay))
        print('The most popular time to travel was hour {}:00.'.format(popularHour))
    
def stationStats(df):
    """Displays station stats."""

    print('\nStation Information:')
    popularStart = df.mode()['Start Station'][0]
    popularEnd = df.mode()['End Station'][0]
    df['Station Trip'] = df['Start Station'] + '  to  ' + df['End Station']
    popularTrip = df.mode()['Station Trip'][0]
    print ('The most popular station to begin a trip was {}.'.format(popularStart))
    print ('The most popular station to end a trip was {}.'.format(popularEnd))
    print ('The most popular trip was {}.'.format(popularTrip))

def timeStats(df):
    """Displays time stats on travel."""

    print('\nTrip Time Information:')
    totalTime = df['Trip Duration'].sum()
    avgTime = df['Trip Duration'].mean()
    print('The total time of travel was {} minutes'.format(totalTime/60))
    print('The average time of travel for trips was {} minutes.'.format(avgTime/60))
    
def userStats(df, city):
    """Displays user stats based on the city chosen by the user."""

    print('\nUser Information:')
    userCounts = df['User Type'].value_counts() 
    for index, user in userCounts.items():
        print('The number of {} users was {}'.format(index, user))
    
    if city != 'Washington':
        genderCounts = df['Gender'].value_counts()
        avgBirthYear = df['Birth Year'].mean()
        oldestUser = int(df['Birth Year'].min())
        youngestUser = int(df['Birth Year'].max())
        for types, number in genderCounts.items():
            print('The number of {} users was {}'.format(types, number))
        print('The average birth year of users was {}.'.format(avgBirthYear))
        print('The oldest user was born in {}.'.format(oldestUser))
        print('The youngest user was born in {}.'.format(youngestUser))
    
    print('\n')

def rawData(df):
    """Displays rows of raw data in 5 row increments, allowing user to choose to see more or not."""

    totalRows = len(df.index)
    for i in range(1, totalRows, 5):
        begin = i
        end = begin + 5
        if end > totalRows:
            totalRows = end
        print('Bikeshare Raw Data: \nYou are viewing rows {0} to {1} out of {2}.'.format(begin, end, totalRows))
        print(df[begin:end])
        time.sleep(1)

        question = 'Would you like to see 5 more rows?'
        proceed = proceedBool(question)
        
        if proceed == False:
            return 
            
def main():
    proceed = True
    while proceed == True:
        city = getCity()
        interval, monthChoice, dayChoice = getInterval()
        df = load_data(city, interval, monthChoice, dayChoice)
        travelStats(df, city, monthChoice, dayChoice, interval)
        stationStats(df)
        timeStats(df)
        userStats(df, city)
        rawData(df)
        question = '\nWould you like to start over?'
        proceed = proceedBool(question)
        if proceed == False:
            print('\n\nThank you for viewing Bikeshare data! Have a great day!\n\n')
    

if __name__ == "__main__":
	main()
