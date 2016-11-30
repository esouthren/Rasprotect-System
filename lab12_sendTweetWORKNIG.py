#!/usr/bin/python3
# lab12_twitter.py
from twython import Twython
import datetime

# twitter screen name - edit yours here
your_screen_name="1513195Cm2540"

# twitter credentials - edit yours here
api_token='0RBDB6riMgANFGCAy5V0MgkQ1'
api_secret='i08pUWVmxcjnoSxwP0mUZfHHehhgaxRl5In5EYbwbKtfArfwer'
access_token='797784532481142784-JNgbn9vyqXU27nlOt5WyIjZ3ioRdbMY'
access_token_secret='7uwsbpLf89J5TDSxHJgGUzed77NW2e4PptviHXYuqsWON'

def main():
    # create twitter object
    twitter=Twython(api_token, api_secret, access_token, access_token_secret)

    # send direct message, enter your Twitter screen name
  #  twitter.send_direct_message(\
   #     screen_name=your_screen_name, \
    #    text="Another message sent at {}".format(datetime.datetime.now()))

    # update status
    twitter.update_status(status='Hello from Python! CM2540 student at {}'.format(datetime.datetime.now()))
    
    print("Tweet sent")

if __name__ == '__main__':
    main()
