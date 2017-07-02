# /r/WritingPrompts bot for /u/Layne-Staley
#
# Takes /r/WritingPrompts comments by /u/Layne-Staley, crossposts them as text submissions to /r/Layne_Staley
#
# By Eli Anderson
#
# Last edited July 02, 2017
#


# praw is a tool that makes interacting with reddit much easier.
#


import praw

# time module is used so the bot won't go crazy

import time
import os


# Login the bot into reddit


def authenticate() :
    print('Authenticating...')
    reddit = praw.Reddit('YeahBot', user_agent='yeah_bot_test v0.1')
    print('Authenticated as ' + str(reddit.user.me()))
    return reddit


def run_bot(reddit, comments_replied_to) :

    # Loop through the comment history of /u/Layne-Staley
    username = 'Layne-Staley'

    for comment in reddit.redditor(username).comments.new(limit=None):

        # if the comment is in /r/WritingPrompts and is a top level comment:

        if comment.subreddit.display_name == 'WritingPrompts' and comment.is_root :

            # Copy the URL
            url = 'https://reddit.com' + comment.permalink(fast=False)

            # Copy the title of the prompt and title of story
            comment_split = comment.split(' ')
            index = comment.body.index('\n')
            story_title = comment_split[1:index]

            submission = comment.submission
            prompt_title = submission.title

            # Copy the story of the prompt
            story = comment_split[index]

            # Submit the comment as new text post in /r/Layne_Staley
            #       - Title of post is specified by Layne
            #       - First line of post is hyperlink to /r/WritingPrompts post (Title of post is the link)
            #

            reddit.subreddit('Layne_Staley').submit(story_title,
                                                   '[' + prompt_title + '](' + url + ')\n\n' + story)


            # Add comment ID to replied to list
            comments_replied_to.append(comment.id)

            # Save comment ID to comments_replied_to.txt (the 'a' means I am appending to the file)

            with open('comments_replied_to.txt', 'a') as file:
                file.write(comment.id + '\n')

    # Sleep for ten seconds

    print('Sleeping for 10 seconds...')
    time.sleep(10)

# Save the comments that have been replied to in the past so the bot doesn't reply to same comments the after each time
# it is run
#
# Uses .txt file to store the comment IDs


def get_saved_comments() :

    # If .txt file with comment IDs doesnt exist, create one and return a blank array

    if not os.path.isfile('comments_replied_to.txt') :
        comments_replied_to = []

    else :
        with open('comments_replied_to.txt', 'r') as file :

            # Read contents of the file
            comments_replied_to = file.read()

            # split() by new line
            comments_replied_to = comments_replied_to.split('\n')

            # Filter out the empty string at end of the .txt file
            # filter() filters out the first argument from the second argument
            # comments_replied_to = filter('', comments_replied_to)

    return comments_replied_to

reddit = authenticate()

# To prevent spam, create list of comments already replied to

comments_replied_to = get_saved_comments()
print(comments_replied_to)

# To automatically reply to comments, a while loop is used

while True :
    run_bot(reddit, comments_replied_to)