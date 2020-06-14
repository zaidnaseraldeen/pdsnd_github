#Refactoring change 1
#Refactoring change 2
import time
import datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Would you like to see data for Chicago, New York, or Washington?\n').lower()
    print('You have chosen {} as a city, if this is not the case, restart the program now'.format(city.title()))
    while city not in ('chicago', 'new york','washington'):
        city = input('Error: Please input one of the following: "Chicago", "New York", "Washington"\n').lower()
    # get user input for month (all, january, february, ... , june)
    month = input('Which month?: all, January, February, March, April, May or June?\n').lower()
    while month not in ('all', 'january', 'february', 'march', 'april' , 'may', 'june'):
        month = input('Error: Please make sure you have spelled the month correctly\n').lower()
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Which day? all, monday, tuesday, wednesday, thursday, friday, saturday, sunday\n').lower()
    while day not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
        day = input('Error: Please make sure you have spelled the day correctly\n').lower()

    print('-'*40)
    return city, month, day


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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['month'] = df['Start Time'].dt.month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df,month,day):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        (str) df - name of the city to analyze
        (str) month - reads the month input and if it is not all, it does not display the most popular month
        (str) day - reads the day input and if it is not all, it does not display the most popular month
    Returns:
        df - Statistics showing the most popular month,day and hour.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    if month == 'all':
        popular_month = df['month'].mode()[0]
        print('Most common month : ', popular_month)
    # display the most common day of week
    if day == 'all':
        popular_day_week = df['day_of_week'].mode()[0]
        print('Most common day of week : ' , popular_day_week)
    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most common start hour : ', popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    df['Start Time'] = df['Start Time'].astype(str)
    df['End Time'] = df['Start Time'].astype(str)
    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station : ', popular_start_station)
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station : ', popular_end_station)
    # display most frequent combination of start station and end station trip
    df['Travel'] = df['Start Station'] + ' --> ' + df['End Station']
    popular_travel = df['Travel'].mode()[0]
    print('Most Popular Journey : ' , popular_travel)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    trip_in_sec = int(df['Trip Duration'].sum())
    total_travel_time = datetime.timedelta(seconds=trip_in_sec)
    print('Total Travel Time : ',total_travel_time)
    # display mean travel time
    avg_trip_in_sec = int(df['Trip Duration'].mean())
    average_travel_time = datetime.timedelta(seconds=avg_trip_in_sec)
    print('This is the average travel time : ', average_travel_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """
    Displays statistics on bikeshare users.

    Args:

        (str) city - Reads the city input and if the city is washington it displays a message saying that the gender and age data is not available.

    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Types: ', user_types)
    # Display counts of gender
    if city in ('chicago', 'new york'):
        gender = df['Gender'].value_counts()
        print('Gender: ',gender)
    else:
        print('Washington does not have gender data')

    # Display earliest, most recent, and most common year of birth
    if city in ('chicago', 'new york'):
        earliest_birth = df['Birth Year'].min()
        print('Earliest Birthday: ', earliest_birth)
        latest_birth = df['Birth Year'].max()
        print('Latest Birthday: ' , latest_birth)
        common_birth = df['Birth Year'].mode()[0]
        print('Most common Birthday: ', common_birth)
    else:
        print('Washington does not have age data')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        raw_data = input('\nWould you like to see indivudual date? yes/no.\n')
        n = 0
        while raw_data == 'yes':
            for idx, row in df[n:n+5].iterrows():
                print(row)
                print('\n')
            raw_data = input('\nWould you like to see more date? yes/no.\n')
            n +=5
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
