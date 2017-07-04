# /r/WritingPrompts bot for /u/Layne-Staley
#
# Takes /r/WritingPrompts comments by /u/Layne-Staley, crossposts them as text submissions to /r/Layne_Staley
#
# By Eli Anderson
#
# Last edited July 02, 2017
#
# Once you get this code, you'll need to do some editing (nothing too complicated)
#
# 1) Open up praw.ini, should be in the same folder as the .py code
# 2) Put in your username, password, client_secret, and client_id
#       - If you don't know what your client_secret/id is, then send me a PM. I'll explain what they are and how to get
#         them
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
    reddit = praw.Reddit('LaneyBot', user_agent='writing_prompts_bot_test v0.1')
    print('Authenticated as ' + str(reddit.user.me()))
    return reddit


def run_bot(reddit, comments_replied_to4) :

    # Loop through the comment history of /u/Layne-Staley
    # I set the limit to be 25 comments so the bot won't automatically post stories that you've already posted yourself.
    # However I don't know how far back your last posted story is, so you might have to edit the limit
    print('Looping through comments...')

    for comment in reddit.redditor('Layne-Staley').comments.new(limit=25):

        # if the comment is in /r/WritingPrompts and is a top level comment: (meaning the bot will ignore your comments
        # if they aren't stories)

        if comment.subreddit.display_name == 'WritingPrompts' and comment.is_root and comment.id not in comments_replied_to4:

            print('New prompt response found!')

            # Copy the URL
            url = 'https://reddit.com' + comment.permalink(fast=False)

            # Copy the title of the prompt and title of story
            title_index = 7 + comment.body.index('Title:')
            story_beginning_index = comment.body.index('\n\n')
            story_title = comment.body[title_index : story_beginning_index]

            submission = comment.submission
            prompt_title = submission.title

            # Copy the story of the prompt
            story = comment.body[story_beginning_index : len(comment.body)]

            # Submit the comment as new text post in /r/Layne_Staley
            #       - Title of post is specified by Layne
            #       - First line of post is hyperlink to /r/WritingPrompts post (Title of post is the link)
            #
            
            print('Submitting post...')

            reddit.subreddit('test').submit(story_title,
                                            '[' + prompt_title + '](' + url + ')\n\n' + story)

            print('Post submitted!')

            # Add comment ID to replied to list
            comments_replied_to4.append(comment.id)

            # Save comment ID to comments_replied_to4.txt (the 'a' means I am appending to the file)

            with open('comments_replied_to4.txt', 'a') as file:
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

    if not os.path.isfile('comments_replied_to4.txt') :
        comments_replied_to4 = []

    else :
        with open('comments_replied_to4.txt', 'r') as file :

            # Read contents of the file
            comments_replied_to4 = file.read()

            # split() by new line
            comments_replied_to4 = comments_replied_to4.split('\n')

            # Filter out the empty string at end of the .txt file
            # filter() filters out the first argument from the second argument
            # comments_replied_to4 = filter('', comments_replied_to4)

    return comments_replied_to4

reddit = authenticate()

# To prevent spam, create list of comments already replied to

comments_replied_to4 = get_saved_comments()
print(comments_replied_to4)

# To automatically reply to comments, a while loop is used

while True :
    run_bot(reddit, comments_replied_to4)