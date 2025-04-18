# -*- coding: utf-8 -*-
import praw
import os
import argparse
import logging

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action = "store_true", help = "display messages")
    parser.add_argument("--sub", default = "funny")    
    parser.add_argument("--link", default = "https://www.redgifs.com/watch/something")
    parser.add_argument("--title", default = "my cat is sooo hilarious, dont ya think?!?")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("running in verbose mode")
    else:
        logging.basicConfig(level=logging.INFO)

    return args

def main():
    args = parse_args()
    
    # Initialize Reddit instance using the 'bot1' section of praw.ini
    reddit = praw.Reddit("bot1")

    # Set your target subreddit
    subreddit_name = args.sub # Replace with your desired subreddit
    subreddit = reddit.subreddit(subreddit_name)
    
    # Post a link
    title = args.title
    url = args.link
    
    # Submit the link post
    submission = subreddit.submit(title=title, url=url)
    
    print(f"Post created: {submission.title} (URL: {submission.url})")
    print(f"Reddit link: https://www.reddit.com{submission.permalink}")

if __name__ == '__main__':
    main()




