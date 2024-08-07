import time
import pandas as pd




def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    THe function aims to return the selected city ,month and day based on user input

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    select_city_str = "Would you like to see the data for Chicago ,New York city or Washington?\n"

    select_month_str = """\nWould you like to filter the data based on specific month
    \rplease select on of the mentioned months or type 'all' if no filter needed
    \r(January,February,March,April, May ,June)\n"""

    select_day_str = """\nWould you like to filter the data based on specific day
    \rplease select on of the mentioned months or type 'all' if no filter needed
    \r(Saturday,Sunday,Monday,Tuesday,Wednesday,Thursday,Friday)\n"""

    wrong_selection_str = "\nwrong selection , please choose on of the mentioned options\n-----------"

    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input(select_city_str).lower().strip()
    while city not in ('chicago', 'new york city', 'washington'):
        print(wrong_selection_str)
        city = input(select_city_str).lower()

    # get user input for month (all, january, february, ... , june)
    month = input(select_month_str).lower().strip()
    while month not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
        print(wrong_selection_str)
        month = input(select_month_str).lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input(select_day_str).lower().strip()
    while day not in ('all', 'saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday'):
        print(wrong_selection_str)
        day = input(select_day_str).lower()

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    the function use pandas methods to filter the city , month ,day and returns a filterd Data frame
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    CITY_DATA = {'chicago': 'chicago.csv',
                 'new york city': 'new_york_city.csv',
                 'washington': 'washington.csv'}

    df = pd.read_csv(CITY_DATA[city],index_col=[0])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['hour'] = df['Start Time'].dt.hour
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'].str.lower() == day]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month


    month_occurrence = df.groupby(['month'])["month"].count().sort_values(ascending=False)
    common_month = month_occurrence.index[0]
    common_month_count = month_occurrence.values[0]
    print("the Most popular month is {} with occurrence count : {} Based on the given filters".format
          (common_month, common_month_count))

    # display the most common day of week

    week_occurrence = df.groupby(['day_of_week'])["day_of_week"].count().sort_values(ascending=False)
    common_week = week_occurrence.index[0]
    common_week_count = week_occurrence.values[0]
    print("the Most popular week day is {} with occurrence count : {} Based on the given filters".format
          (common_week, common_week_count))

    # display the most common start hour
    hour_occurrence = df.groupby(['hour'])["hour"].count().sort_values(ascending=False)
    common_hour = hour_occurrence.index[0]
    common_hour_count = hour_occurrence.values[0]
    print('the Most popular hour is {} with occurrence count : {} Based on the given filters'.format
          (common_hour, common_hour_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station_occurrence = df.groupby(['Start Station'])["Start Station"].count().sort_values(ascending=False)
    start_station = start_station_occurrence.index[0]
    start_station_count = start_station_occurrence.values[0]
    print("the Most popular Start Station is '{}' with occurrence count : {} Based on the given filters".format(
        start_station, start_station_count))

    # display most commonly used end station
    end_station_occurrence = df.groupby(['End Station'])["End Station"].count().sort_values(ascending=False)
    end_station = end_station_occurrence.index[0]
    end_station_count = end_station_occurrence.values[0]
    print("the Most popular end Station is '{}' with occurrence count : {} Based on the given filters".format(
        end_station, end_station_count))

    # display most frequent combination of start station and end station trip
    df['start-stop'] = df['Start Station'] + "*towards*" + df['End Station']
    start_end_station_occurrence = df.groupby(['start-stop'])['start-stop'].count().sort_values(ascending=False)
    start_station = start_end_station_occurrence.index[0].split(sep="*towards*")[0]
    end_station = start_end_station_occurrence.index[0].split(sep="*towards*")[-1]
    start_end_station_count = start_end_station_occurrence.values[0]
    print(
        "the Most popular Start and End Station are '{}' towards '{}' with occurrence count : {} Based on the given filters".format(
            start_station, end_station, start_end_station_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = round(df['Trip Duration'].values.sum(), 1)

    print("Total Trip Duration is {}  Based on the given filters".format(total_duration))

    # display mean travel time

    Mean_duration = round(df['Trip Duration'].values.mean(), 1)
    print("Mean Trip Duration is {}  Based on the given filters".format(Mean_duration))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    user_types = df['User Type'].value_counts()
    user_str = ""
    for index, value in user_types.items():
        user_str += f"( {index}  , count :{value} ) "

    print("Users are {} based on the given filters".format(user_str))

    # Display counts of gender
    if "Gender" in df.columns:
        gender = df['Gender'].value_counts()
        gender_str = ""
        for index, value in gender.items():
            gender_str += f"( {index}  , count :{value} ) "

        print("Genders are {} based on the given filters".format(gender_str))
    else:
        print("Gender Information is not available")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        birth_years = df['Birth Year'].value_counts()
        common_year = birth_years.index[0]
        earliest_year = birth_years.index.min()
        most_recent_year = birth_years.index.max()

        print(
            """earliest year of Birth : {}     , Most recent year of Birth : {}    ,  most common year of birth : {} based on given filters""".format(
                earliest_year, most_recent_year, common_year))
    else:
        print("Birth Year Information is not available")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def print_trips_details(df):
    """
    Displays row details of all trips in the data frame based on the selected filters
    the function display 5 trips at once and iterate based on user request
    Args:
        (DateFrame) df - Data frame of the selected filters

     Returns:
        None
    """
    df = df.drop('start-stop', axis=1)
    mydata_generator = df.iterrows()
    i=0
    while (True):
        while i <5:
            try:
                print("-----------------------------------------")
                print(dict(next(mydata_generator)[1]))
                i+=1
            except StopIteration:
                print("All Records have been displayed")
                return None
        show_customer_details =input('\nDo you want to check another 5 rows of the dataset (yes/no)?\n')
        if show_customer_details.lower() != "yes":
            return None
        i=0


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, month, day)
        station_stats(df)

        trip_duration_stats(df)
        user_stats(df)

        print_trips=input ('\nDo you want to check the first 5 rows of the dataset related to the chosen city (yes/no)?\n')
        if print_trips.lower().strip() == "yes":
            print_trips_details(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
