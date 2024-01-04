#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
import pandas as pd
import numpy as np


# In[ ]:


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }


# In[ ]:


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    month ='all'
    day = 'all'
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago, New York, or Washington:\n')
        #check if input city is one of the 3 cities
        if city.title() in ['Chicago','New York', 'Washington']:
            break
        else:
            print('The input is not valid, please choose one of the 3 given cities')   

    #get user input for by which method would the user like to filter the data         
    while True:
        filter = input('Would you like to filer the data by month, day, both or not at all? Type \"none\" for no time filer.\n')
        if filter.lower() in ['month','day', 'both','none']:
            break
        else:
            print('Invalid input, please enter again')
            
    # get user input according to the choosen filtering method 
    # get user input for month (all, january, february, ... , june)
    if filter.lower() == 'month': 
        while True:
            month = input('Which month? Choose one from January to June or all:\n')
            if month.lower() in ['january', 'february','march','april','may','june','all']:
                break
            else:
                print('Invalid input for month, please enter input again')
                               
    # get user input for day of week (all, monday, tuesday, ... sunday)
    elif filter.lower() == 'day':
        while True:
            day = input('Which weekday? Choose of of the weekday or all:\n')
            if day.lower() in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']:    
                break
            else:
                print('Invalid input for day, please enter input again')
       
    # get user input for both month and day of week    
    elif filter.lower() =='both':
        while True:
            month = input('Which month? Choose one from January to June or all:\n')
            if month.lower() in ['january', 'february','march','april','may','june','all']:
                break
            else:
                print('Invalid input for month, please enter input again')
        while True:
            day = input('Which weekday? Enter one weekday or all:\n')
            if day.lower() in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']:    
                break
            else:
                print('Invalid input for day, please enter input again')
    
         


    print('-'*40)
    return city, month, day


# In[ ]:


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # filter by month if applicable
    if month.lower() != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower())+1
    
        # filter by month to create the new dataframe
        df = df[df['month']==month]
    # filter by day of week if applicable
    if day.lower() != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]

    return df


# In[ ]:


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print(f'The most common month is {common_month}.')

    # display the most common day of week
    common_dayofweek = df['day_of_week'].mode()[0]
    print(f'The most common day of week is {common_dayofweek}.')

    # display the most common start hour
    common_starthour = df['Start Time'].dt.hour.mode()[0]
    print(f'THe most common start hour is {common_starthour}.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[ ]:


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station is {}, count: {}'.format(df['Start Station'].mode()[0], df['Start Station'].value_counts()[0]))

    # display most commonly used end station
    print('The most commonly used end station is {}, count: {}.'.format(df['End Station'].mode()[0], df['End Station'].value_counts()[0]))

    # display most frequent combination of start station and end station trip
    df['Combination'] = df['Start Station']+ ' to '+df['End Station']
    print('The most frequently combination of start and end station trip is {}, count: {}.'.format(df['Combination'].mode()[0], df['Combination'].value_counts()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[ ]:


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total traval time is {}'.format(df['Trip Duration'].sum()))

    # display mean travel time
    print('The average travel time is {}'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[ ]:


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    pd.set_option("display.max_columns", 200)
    
    if 'User Type' in df:
        print(df['User Type'].value_counts())
    else:
        print('User Type stats cannot be calculated because User Type does not appear in the dataframe')

    # Display counts of gender
    if 'Gender' in df:
        print(df['Gender'].value_counts())
    else:
        print('Gender stats cannot be calculated because Gender does not appear in the dataframe')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print('The earliest year of birth is {}.'.format(df['Birth Year'].min()))
        print('The most recent year of birth is {}.'.format(df['Birth Year'].max()))
        print('The most common year of birth is {}.'.format(df['Birth Year'].mode()[0]))
    else:
        print('Birth Year stats cannot be calculated because Birth Year does not appear in the dataframe')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[ ]:


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        index=0
        
        # check if user wants to see 5 lines of raw data
        while True:
            answer = input('Would you like to see (next) 5 lines of raw data? Please enter Yes or No:\n')
            if answer.lower() == 'yes':
                print(df.iloc[index:index+5])
                index+=5
                continue
            elif answer.lower()=='no':
                break
            else:
                print('Invalid input, please enter Yes or No')
                
                 
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


# In[ ]:


if __name__ == "__main__":
    main()


# In[ ]:




