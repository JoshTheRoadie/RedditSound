# Gets new posts from Subreddits on reddit.com
# Updated to save a list of dictionaries instead of lists that represent the Subreddit posts.

import datetime
import cPickle
import sys
import praw


USER_AGENT = 'get_new_posts.py 1.0, Learning code by /u/thesubtlecreep'


def get_date(submission):
    """
    Returns the time that a *submission* was created as a datetime.datetime object.
    :param submission: praw submission object
    :return: datetime.datetime object
    """
    time = submission.created
    return datetime.datetime.fromtimestamp(time)


def get_new_posts(subreddit_names):
    """
    Returns a list of dicts where each dict represents the a subreddit post.
    :param subreddit_names: iterable of strings, names of subreddits
    :return: list of dicts
    The dictionaries in the list are of the form:
    {'name': sub_name, 'id': sub_id, 'timestamp': sub_timestamp, 'title': sub_title, 'message': sub_text}
    """
    reddit = praw.Reddit(user_agent=USER_AGENT)
    new_posts = list()
    for subreddit_name in subreddit_names:
        subreddit = reddit.get_subreddit(subreddit_name)
        for submission in subreddit.get_new(limit=100):
            new_posts.append({'name': subreddit_name,
                              'id': submission.id,
                              'timestamp': get_date(submission),
                              'title': submission.title,
                              'message': submission.selftext})
    return new_posts


def main(subreddit_file, new_post_file):
    try:
        with open(subreddit_file, 'rb') as subs_file:
            subreddit_names = subs_file.read().split()
    except IOError:
        print 'ERROR: {} does not exist.'.format(subreddit_file)
        sys.exit()
    new_posts = get_new_posts(subreddit_names)
    with open(new_post_file, 'wb') as pickle_file:
        cPickle.dump(new_posts, pickle_file)


if __name__ == '__main__':
    assert len(sys.argv) == 3, 'Improper number of parameters.'
    main(sys.argv[1], sys.argv[2])
    sys.exit()
