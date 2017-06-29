# Turn processed Subreddit posts into a MIDI file.

import cPickle
from midi.MidiOutFile import MidiOutFile


NOTE_DURATION = 80


def midi_event(command, post):
    return {'command': command, 'note': post['note'], 'velocity': post['velocity'], 'sec_from_last': None}


def midi_events_for_file(posts):
    events = list()
    for post in posts:
        note_on = post['sec_from_zero']
        note_off = note_on + NOTE_DURATION
        events.append([note_on, midi_event('on', post)])
        events.append([note_off, midi_event('off', post)])
    events.sort(key=lambda event: event[0])
    seconds_from_previous_event(events)
    return [event[1] for event in events]


def seconds_from_previous_event(events):
    previous_time = 0
    for event in events:
        event[1]['sec_from_last'] = int(event[0] - previous_time)
        previous_time = event[0]


def generate_midi_command(midi_file, event):
    midi_file.update_time(event['sec_from_last'])
    getattr(midi_file, 'note_{}'.format(event['command']))(
        channel=0, note=event['note'], velocity=event['velocity']
    )


def make_midi_file(filename, events):
    out_file = filename
    midi = MidiOutFile(out_file)

    # Non-optional midi framework
    midi.header()
    midi.start_of_track()

    # Events
    for event in events:
        generate_midi_command(midi, event)

    # Non-optional midi framework
    midi.update_time(0)
    midi.end_of_track()

    midi.eof()


if __name__ == '__main__':
    with open('notes.pkl', 'rb') as input_file:
        midi_posts = cPickle.load(input_file)
    midi_events = midi_events_for_file(midi_posts)
    for event in midi_events:
        print event
    make_midi_file('my_sub_song.mid', midi_events)
