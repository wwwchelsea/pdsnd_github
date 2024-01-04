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

def check_data_entry(prompt, valid_entries): 
    """
    Function that asks the user to input data and verifies if it's valid.
    This simplifies the get_filters() function, where we need to ask the user for three inputs.
    Args:
        (str) prompt - message to show to the user
        (list) valid_entries - list of accepted strings 
    Returns:
        (str) user_input - user's valid input
    """
    try:
        user_input = str(input(prompt)).lower()
        while user_input not in valid_entries : 
            print('It looks like your entry is incorrect.')
            print('Let's try again!')
            user_input = str(input(prompt)).lower()

        print('Great! You've chosen: {}\n'.format(user_input))
        return user_input

    except:
        print('There seems to be an issue with your input.')

def get_filters(): 
    """
    Function to ask the user for a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let's explore some US bikeshare data!')
    valid_cities = CITY_DATA.keys()
    prompt_cities = 'Choose one of the 3 cities (chicago, new york city, washington): '
    city = check_data_entry(prompt_cities, valid_cities)

    valid_months = ['all','january','february','march','april','may','june']
    prompt_month = 'Choose a month (all, january, february, ... , june): '
    month = check_data_entry(prompt_month, valid_months)

    valid_days = ['all','monday','tuesday','wednesday','thursday','friday','saturday', 'sunday']
    prompt_day = 'Choose a day (all, monday, tuesday, ... sunday): '
    day = check_data_entry(prompt_day, valid_days)

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

# Set nums of displayed column 
pd.set_option("display.max_columns", 200)

if __name__ == "__main__":
    main()


# In[ ]:




