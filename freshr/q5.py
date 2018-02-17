import argparse
import os.path
from datetime import datetime
from math import ceil

import pandas as pd



# Find the best moment to notify a user. 
# We define "best" as the latest hour of the day where the user is the most likely to have interactions with Freshr during a short period of time (defined by the "MINUTES" variable)
# If the user is not found, we return the default value 7h45


DEFAULT_BEST = 465  # 7h45
MINUTES = 20


def load_user_data(user, file):
    df = pd.read_csv(file).set_index('message_read_id')
    return df[df['user_id'] == user]


def to_minutes(timestamp):
    time = datetime.fromtimestamp(timestamp / 1000)
    return 60 * time.hour + time.minute


def window_sum(serie, count, index):
    # Sum of number of messages sent between now and now + count minute. And we take in account the midnight problem
    if index + count >= len(serie):
        rest = (index + count) - len(serie)
        return serie[index:rest].sum() + serie[0:(count - rest)].sum()
    else:
        return serie[index:index + count].sum()


def aggregate_messages(message_read_by_minute, minutes):
    # There may be an elegant way to do this. Perhaps.
    all_day_long = pd.Series([0] * (60 * 24)).add(message_read_by_minute, fill_value=0)
    sum_of_next_minutes = pd.Series([0] * (60 * 24))
    for idx in all_day_long.index:
        sum_of_next_minutes[idx] = window_sum(all_day_long, minutes, idx)
    return sum_of_next_minutes


def find_best_time(user_data):
    if len(user_data) == 0:
        print("No data has been found for this user, falling back to default value")
        return DEFAULT_BEST

    # Compute the serie of the times of the day around where the user is active
    # Returns a serie of hours block
    day_blocks = user_data['timestamp'].map(to_minutes)

    # Group them by equality
    message_read_by_minute = day_blocks.value_counts()

    # Aggregates the counts in a windowed representation
    sum_of_next_minutes = aggregate_messages(message_read_by_minute, MINUTES)

    # The best time to send a push notification is just before their usual max of activity
    return sum_of_next_minutes[sum_of_next_minutes == sum_of_next_minutes.max()].last_valid_index()


def format_time(time_in_minutes):
    hour = int(time_in_minutes / 60)
    minutes = ceil((time_in_minutes / 60 - hour) * 60)
    return '{}:{}'.format(hour, minutes)


def find_and_print_time(user, file):
    print("Processing...")
    user_data = load_user_data(user, file)
    best_time = find_best_time(user_data)
    formatted_time = format_time(best_time)
    print("The best time to notify the user {} is {}".format(user, formatted_time))


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Freshr Push notification')
    parser.add_argument('user', type=int, help='User to look for')
    parser.add_argument('-f', type=str, metavar='file', dest='file', help='File with the data to read')
    args = parser.parse_args()
    if not os.path.isfile(args.file):
        print("{} is not a file", args.file)
        return
    find_and_print_time(args.user, args.file)
