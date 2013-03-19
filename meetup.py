# -*- coding: utf-8 -*-
import urllib2
from collections import namedtuple
from functools import partial


Event = namedtuple('Event', ['url', 'name', 'date', 'location', 'description'])


class Connection(object):
    def __init__(self, lib):
        self.lib = lib

    def get(self, url):
        response = self.lib.urlopen(url)
        return response.read()


class _PYLUGMeetup(object):
    def __init__(self, key=None, connection=None):
        self.connection = connection
        self.url = ('https://api.meetup.com/2/events?key={0}'
                    '&sign=true&group_urlname=python-lv&page=20'.format(key))

    def next_event(self):
        import json
        from datetime import datetime

        response = self.connection.get(self.url)
        response = response.replace('\n', '')

        events = json.loads(response)
        event_dict = events['results'][0]

        utc_ts = event_dict['time']
        utc_offset = event_dict['utc_offset']
        event_datetime = datetime.utcfromtimestamp((utc_ts + utc_offset) / 1e3)

        venue = event_dict['venue']
        location = ', '.join(
            [venue['name'], venue['address_1'], venue['city']])

        event = Event(url=event_dict['event_url'],
                      name=event_dict['name'],
                      location=location,
                      date=event_datetime,
                      description=event_dict['description'])

        return event


connection = Connection(urllib2)
PYLUGMeetup = partial(_PYLUGMeetup, connection=connection)
