#!/usr/bin/env python

import argparse
import json
import sys
import time
import os
import twitter

from datetime import datetime
from dateutil.parser import parse

__author__ = "Zulwiyoza Putra"
__version__ = "0.1"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def delete(api, date):
    with open("data.json") as file:

        # Load file as JSON data
        data = json.load(file)

        # Initialize conter
        deleted_count = 0
        failed_count = 0
        total = len(data)

        for entry in data:
            # Get tweet data
            tweet_key = "tweet"
            if tweet_key not in entry:
                error(f"Couldn't find \"{tweet}\" value inside the data")
            
            tweet = entry[tweet_key]

            # Get tweet ID
            tweet_id_key = "id"
            if tweet_id_key not in tweet:
                error(f"Couldn't find \"{tweet_id_key}\" value inside the tweet data")

            tweet_id = tweet[tweet_id_key]

            # Get tweet date
            tweet_date_key = "created_at"
            if tweet_date_key not in tweet:
                error(f"Couldn't find \"{tweet_date_key}\" value inside the tweet data")

            tweet_date = datetime.strptime(tweet[tweet_date_key], "%a %b %d %H:%M:%S +%f %Y").date()

            # Continue if given date is before tweet_date
            if date != "" and tweet_date >= parse(date).date():
                continue

            try:
                # Print header
                date_str = tweet_date.strftime('%a, %d %b %Y')
                print(f"{bcolors.HEADER}==================== DELETING TWEET #{tweet_id} ({date_str}) ===================={bcolors.ENDC}\n")

                # Print full text of the tweet
                print(f'{bcolors.BOLD}"{tweet["full_text"]}"{bcolors.ENDC}\n')

                # Destroy tweet
                api.DestroyStatus(tweet_id)

                # Increment counter
                deleted_count += 1

                # Print progress
                print(f"{bcolors.OKGREEN}Total {deleted_count}/{total} tweets is successfully deleted at {datetime.today().strftime('%a, %d %b %Y %H:%M:%S')}{bcolors.ENDC}\n")

            except twitter.TwitterError as err:
                # Print exception
                error_message = err.message[0]["message"]
                print(f'{bcolors.WARNING}Failed to delete tweet with error: {error_message}{bcolors.ENDC}\n')

                failed_count += 1

            # Print results
            print(f"{bcolors.OKGREEN}Deleted: {deleted_count}/{total}{bcolors.ENDC}")
            print(f"{bcolors.FAIL}Failed: {failed_count}/{total}{bcolors.ENDC}\n")
        
        # Print final results
        print(f"{bcolors.HEADER}==================== COMPLETED ===================={bcolors.ENDC}\n")
        print(f"{bcolors.OKGREEN}Deleted: {deleted_count}/{total}{bcolors.ENDC}")
        print(f"{bcolors.FAIL}Failed: {failed_count}/{total}{bcolors.ENDC}\n")
        
def error(message, exit_code=1):
    sys.stderr.write(f"{bcolors.FAIL}{message}{bcolors.ENDC}\n")
    exit(exit_code)

def confirm(question, default="yes"):
    valid = {
        "yes": True,
        "y": True,
        "no": False,
        "n": False
    }

    if default is None:
        prompt = " [y/n]"
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError(f"invalid default answer: '{default}'")

    while True:
        sys.stdout.write(question + prompt + "\n")
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def main():
    parser = argparse.ArgumentParser(description="Tweets destroyer.")

    parser.add_argument(
        "-d", "--date", 
        dest="date", 
        required=True,
        help="Delete tweets until this date"
    )

    parser.add_argument(
        "-k", "--key", 
        dest="key", 
        required=True,
        help="Consumer API key"
    )

    parser.add_argument(
        "-s", "--secret", 
        dest="secret", 
        required=True,
        help="Consumer API secret key"
    )

    parser.add_argument(
        "--token-key", 
        dest="token_key", 
        required=True,
        help="Access token key"
    )

    parser.add_argument(
        "--token-secret", 
        dest="token_secret", 
        required=True,
        help="Access token secret"
    )

    args = parser.parse_args()

    confirmed = confirm(f"\nAre you sure to destroy all past tweets from {args.date}?\nThis action cannot be reverted.")

    if not confirmed:
        error("Action aborted")

    api = twitter.Api(
        consumer_key=args.key,
        consumer_secret=args.secret,
        access_token_key=args.token_key,
        access_token_secret=args.token_secret,
        sleep_on_rate_limit=True)
    
    delete(api, args.date)


if __name__ == "__main__":
    main()
