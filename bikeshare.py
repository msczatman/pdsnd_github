import time
import pandas as pd
import numpy as np
import json

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities     = [ "new york city", "chicago", "washington" ]

days       = [ "monday", "tuesday", "wednesday", "thursday",
                        "friday", "saturday", "sunday", "all" ]
months     = [ "january", "february", "march", "april", "may", "june", "all" ]

def questionuserchoice(choices, message):
    while True:
        userfeedback = input(message).strip().lower()

        if userfeedback in choices:
            return userfeedback

        print("\nYou can submit one of the available answers.\n")

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = questionuserchoice(cities,
        "choose the city and please type the name in lowercase: 'chicago', 'new york city' or 'washington' > ")

    # get user input for month (all, january, february, ... , june)
    month = questionuserchoice(months,
        "choose all months or one month and please type the name in lowercase:'all' or 'e.g. january', 'february...'> ")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = questionuserchoice(days,
        "Please enter day and please type the name in lowercase: e.g. 'monday','...' or 'all' > ")


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    it should returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city], index_col = 0)
    # setting index_col=0 we're treating the first column as the index

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # converting the Start Time column to datetime

    df["month"] = df['Start Time'].dt.month
    # extracting month from the Start Time column to create a month column

    df["weekday"] = df['Start Time'].dt.weekday_name
    # extracting the weekday out of the "Start Time" value.

    df["starthour"] = df['Start Time'].dt.hour
    # extracting hour from the Start Time column to create an hour column

    df["start-to-end-station"] = df['Start Station'].astype(str) + ' to ' + df['End Station']

    if month != 'all':
        # that means that the Search keyword of month is not full range of month.
        monthidx = months.index(month) + 1
        # indexing a list for the month.
        df = df[df["month"] == monthidx ]
        # month filtering

    if day != 'all':
        df = df[df["weekday"] == day.title() ]
        # Method .title() will convert the string value in variable day into title case
        # so june will be converted to June


    return df


def time_stats(df):
    """This function displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    monthidx = df["month"].mode()[0] - 1
    toppopmonth = months[monthidx].title()

    print("Most common month: ", toppopmonth)

    # display the most common day of week
    toppopday = df["weekday"].mode()[0]
    print("Most common day: ", toppopday)

    # display the most common start hour
    toppophour = df["starthour"].mode()[0]
    print("Most common hour: ", toppophour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popularstart = df['Start Station'].mode()[0]
    print("start station used the most: ", popularstart)

    # display most commonly used end station
    popularend = df['End Station'].mode()[0]
    print("end station used the most: ", popularend)

    # display most frequent combination of start station and end station trip
    mostfrequentcombination = df["start-to-end-station"].mode()[0]
    print("Most common used combination concerning start- and end-station: ",
            mostfrequentcombination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('\n This is the total travel time: {} \n '.format(df['Trip Duration'].sum()))

    # display mean travel time
    print('\n This is the mean travel time: {} \n'.format(df['Trip Duration'].mean()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\n Count of user types: {} \n'.format(df['User Type'].value_counts()))

    if "Gender" in df:
        print("\nStatistic of client`s gender")
        print("Male people: ", df.query("Gender == 'Male'").Gender.count())
        print("Female people: ", df.query("Gender == 'Female'").Gender.count())

    else:
        print("Gender column does not exist")

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df:
        #  getting the most frequent value in the column
        print("The Most frequent year of birth: ", df["Birth Year"].value_counts().idxmax())
        print("\nThe earliest year of birth is: ", df["Birth Year"].min())
        print("The Most recent year of birth: ", df["Birth Year"].max())

    else:
        print("Birth Year column does not exist")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def showingdata(df):
    lengthrow = df.shape[0]

    #  counting nr of rows till 5
    for i in range(0, lengthrow, 5):

        yes = input('\nMay I show you some more specific data? Please input if yes or no\n> ')
        if yes.lower() != 'yes':
            break

        #  putting data to type json and splitting them and executing print
        drow = df.iloc[i: i + 5].to_json(orient='records', lines=True).split('\n')
        for row in drow:
            rowparse = json.loads(row)
            #converting into JSON:
            rowjson = json.dumps(rowparse, indent=3)
        print(rowjson)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        # below function is to show the bikeshare raw data
        showingdata(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
