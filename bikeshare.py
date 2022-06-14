import pandas as pd
import datetime as dt
import calendar
import time

cities = ['chicago', 'new york', 'washington']

def main():
    while True:
        while True:
            city = get_city()
            df = create_dataframe(city)
            # Ask the user for the filter type
            Question = input('Would you like to filter the data by month, day or both? Type "none" for no filter.\n').lower()
            if Question == 'none':
                filtered_df = df
                display_rows(filtered_df)
                break

            elif Question == 'both':
                filtered_df = month_filter(df)
                filtered_df = day_filter(filtered_df)
                display_rows(filtered_df)
                break

            elif Question == 'month':
                filtered_df = month_filter(df)
                display_rows(filtered_df)
                break

            elif Question == 'day':
                filtered_df = day_filter(df)
                display_rows(filtered_df)
                break

            else:
                print('Invalid! Please try again.')

        time_stats(filtered_df)
        station_stats(filtered_df)
        trip_duration_stats(filtered_df)
        user_stats(filtered_df, city)

        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
            if restart == 'no' or restart == 'yes':
                break
            elif restart != 'no' or restart != 'yes':
                print('Invalid! Please try again.')

        if restart == 'no':
            break

def get_city():
    """
    Get the city name from the user.

    Args:
        no arguments required.

    Returns:
        - City name
        type: string
    """
        # Ask the user for a city
    while True:
        city = input("Which city do you like to know about, Chicago or New york or Washington?\n").lower()
        if city not in cities:
            print("please choose one from the provided cities\n")
        else:
            break
    return city

def create_dataframe(city_name):
    """
    Create the data frame.

    Args:
        no arguments required.

    Returns:
        - DataFrame
        type: Pandas DataFrame
    """
    # Read the city file
    df = pd.read_csv(city_name.replace(' ','_')+".csv") # new_york_city file is renamed as new_york
    # Convert Start Time column to datetime data type
    df['Start Time'] =  pd.to_datetime(df['Start Time'])
    # Create 'day of week' column
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # Create month column as a name
    df['month_name'] = df['Start Time'].dt.month.apply(lambda x: calendar.month_name[x])

    return df



def month_filter(df):
    """
    Filter the data by a month determined by the user.

    Args:
        - dataframe to be filtered
        type: Pandas DataFrame

    Returns:
        - filtered dataframe by month
        type: Pandas DataFrame
    """
    # Available months
    months = df.month_name.unique()
    while True:
        selected_month = input('Available data is about the following months! Please choose one: \n{}\n'.format(months)).title()
        if selected_month not in months:
            print('Invalid! Please try again.')
        else:
            break

    return df[df['month_name'] == selected_month]

def day_filter(df):
    """
    Filter the data by a day determined by the user.

    Args:
        - dataframe to be filtered
        type: Pandas DataFrame

    Returns:
        -filtered dataframe by day
         type: Pandas DataFrame
    """
    # Available days
    days = df.day_of_week.unique()
    while True:
        selected_day = input('Available data is about the following days! Please choose one: \n{}\n'.format(days)).title() # even if i type capital letter in the middle of the word. title() will only capitalize first letter and make the rest small letters
        if selected_day not in days:
            print('Invalid! Please try again.')
        else:
            break

    return df[df['day_of_week'] == selected_day]

# convert second to h m s
def convert_seconds(seconds):
    """
    Convert seconds to hour:minute:second.

    Args:
        - seconds
          type: integer

    Returns:
        - hour:minute:second
          type: string
    """
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    return "%d:%02d:%02d" % (hour, min, sec)

def display_rows(df):
    """
    Displays rows from the dataframe according to the user choice.

    Args:
        - dataframe to apply statistics on
        type: Pandas DataFrame

    Returns:
        - no return just printing
    """
    start = 0
    while True:
        display_ask = input('Would you want to display rows from the data, yes or no ?\n').lower()
        if display_ask == 'yes':
            while True:
                try:
                    rows_no = int(input('How many rows do you want to display ?\nPlease type it as an integer.\n'))
                    break
                except:
                    print('Invalid! Please try again.')

            print(df.iloc[start : start+rows_no])
            start += rows_no
        elif display_ask == 'no':
            break
        else:
            print('Invalid! Please try again.')

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        - dataframe to apply statistics on.
        type: Pandas DataFrame

    Returns:
        - no return just printing.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month_name'].mode()[0]
    print("Most common Month: ", most_common_month)


    # display the most common day of
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print("Most common Day of Week: ", most_common_day_of_week)


    # display the most common start hour
    most_common_hour_of_day = df['Start Time'].dt.hour.mode()[0]
    print("Most common Hour of Day: ", most_common_hour_of_day)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        - dataframe to apply statistics on.
        type: Pandas DataFrame

    Returns:
        - no return just printing.
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most common Start Station: ", df['Start Station'].mode()[0])


    # display most commonly used end station
    print("Most common End Station: ", df['End Station'].mode()[0])


    # display most frequent combination of start station and end station trip
    df['trip'] =  df['Start Station'] + ' to ' + df['End Station']
    most_common_trip = df['trip'].mode()[0]
    print("Most common Trip: ", most_common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Args:
        - dataframe to apply statistics on.
        type: Pandas DataFrame

    Returns:
        - no return just printing.
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print("Total Travel Time in seconds: ", total_time)
    print("Total Travel Time in h:m:s: ", convert_seconds(total_time))


    # display mean travel time
    average_time = df['Trip Duration'].mean()
    print("Average Travel Time in seconds: ", average_time)
    print("Average Travel Time in h:m:s: ", convert_seconds(average_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """
    Displays statistics on bikeshare users.

    Args:
        - dataframe to apply statistics on.
        type: Pandas DataFrame

    Returns:
        - no return just printing.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Count of users:\n", df['User Type'].value_counts().to_frame())

    # Display counts of gender
    if city == 'washington':
        print('Sorry! No available data about gender')
    else:
        print("Count of genders:\n", df['Gender'].value_counts().to_frame())


    # Display earliest, most recent, and most common year of birth
    if city == 'washington':
        print('Sorry! No available data about Year Of Birth')
    else:
        print("Earliest Year Of Birth: ", df['Birth Year'].min())
        print("Most recent Year Of Birth: ", df['Birth Year'].max())
        print("Most common Year Of Birth: ", df['Birth Year'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

if __name__ == "__main__":
	main()
