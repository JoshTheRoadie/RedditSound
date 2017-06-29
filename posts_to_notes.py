# Processing the new posts for MIDI

import cPickle
import sys


MIDI_NOTE_MAX = 127
MIDI_NOTE_MIN = 0
MIDI_VELOCITY_MAX = 127
MIDI_VELOCITY_MIN = 0
DEFAULT_MIDI_VELOCITY = 64


def load_subreddit_posts(filename):
    with open(filename, 'rb') as posts_file:
        new_posts = cPickle.load(posts_file)
    new_posts.sort(key=lambda post: post['timestamp'])
    return new_posts


def save_subreddit_posts(filename, posts):
    with open(filename, 'wb') as output_file:
        cPickle.dump(posts, output_file)


def title_to_note(post_title):
    note_num = len(post_title)
    if note_num > MIDI_NOTE_MAX:
        return MIDI_NOTE_MAX
    elif note_num < MIDI_NOTE_MIN:
        return MIDI_NOTE_MIN
    else:
        return note_num


def message_to_velocity(post_message):
    message_num = len(post_message) / 25
    if message_num <= MIDI_VELOCITY_MIN:
        return DEFAULT_MIDI_VELOCITY
    elif message_num + DEFAULT_MIDI_VELOCITY > MIDI_VELOCITY_MAX:
        return MIDI_VELOCITY_MAX
    else:
        return message_num + DEFAULT_MIDI_VELOCITY


def seconds_from_time_zero(post_timestamp, time_zero):
    return (post_timestamp - time_zero).total_seconds()


def main(post_file, output_file):
    new_sub_posts = load_subreddit_posts(post_file)
    new_sub_posts.sort(key=lambda post: post['timestamp'])
    time_zero = new_sub_posts[0]['timestamp']
    for post in new_sub_posts:
        post['note'] = title_to_note(post['title'])
        post['velocity'] = message_to_velocity(post['message'])
        post['sec_from_zero'] = seconds_from_time_zero(post['timestamp'], time_zero)
    save_subreddit_posts(output_file, new_sub_posts)


if __name__ == '__main__':
    assert len(sys.argv) == 3, 'Improper number of parameters.'
    main(sys.argv[1], sys.argv[2])
    sys.exit()
