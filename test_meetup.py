# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase

from meetup import _PYLUGMeetup, Connection


class TestConnection(TestCase):
    def test_fetches_body_of_page(self):
        fake_response = FakeResponse('Page Content')
        urllib2_mock = FakeUrllib2(fake_response)
        connection = Connection(urllib2_mock)
        some_url = 'some-fake-url'

        response = connection.get(some_url)

        self.assertTrue(urllib2_mock.called, 'Connection wasnt called')
        self.assertEquals(urllib2_mock.args, (some_url, ))
        self.assertEquals(response, 'Page Content')


class TestMeetupApi(TestCase):
    def setUp(self):
        self.some_key = 'fake-key'
        self.connection = FakeConnection()
        self.meetup = _PYLUGMeetup(self.some_key, self.connection)

    def test_fetches_next_event(self):
        event = self.meetup.next_event()

        self.assertEquals(event.name, u'Ikmēneša saiets')
        self.assertEquals(event.date, date('2013.04.03 19:00'))
        self.assertEquals(event.description, 'Some event description')
        self.assertEquals(event.url,
                          'http://www.meetup.com/python-lv/events/108519452/')
        self.assertEquals(event.location,
                          'TechHub Riga, Citadeles iela 12, Riga')

    def test_asks_meetup_server_for_information(self):
        self.meetup.next_event()

        self.assertTrue(self.connection.called, 'Connection wasnt called')
        self.assertEquals(self.connection.args, (URL, ))


def date(date_str):
    from datetime import datetime
    return datetime.strptime(date_str, '%Y.%m.%d %H:%M')


class FakeResponse(object):
    def __init__(self, content):
        self.content = content

    def read(self):
        return self.content


class FakeUrllib2(object):
    def __init__(self, return_value):
        self.called = False
        self.args = None
        self.kwargs = None
        self.return_value = return_value

    def urlopen(self, *args, **kwargs):
        self.called = True
        self.args = args
        self.kwargs = kwargs
        return self.return_value


class FakeConnection(object):
    def __init__(self):
        self.args = None
        self.called = False

    def get(self, *args, **kwargs):
        self.called = True
        self.args = args
        return RESPONSE


URL = 'https://api.meetup.com/2/events?key=fake-key&sign=true&group_urlname=python-lv&page=20'

RESPONSE = """
{
    "results": [
        {
            "visibility": "public",
            "status": "upcoming",
            "maybe_rsvp_count": 0,
            "venue": {
                "id": 4808132,
                "lon": 24.100813,
                "repinned": false,
                "name": "TechHub Riga",
                "address_1": "Citadeles iela 12",
                "lat": 56.955326,
                "country": "lv",
                "city": "Riga"
            },
            "id": "dlxsfdyrgbfb",
            "utc_offset": 10800000,
            "time": 1365004800000,
            "waitlist_count": 0,
            "created": 1343986491000,
            "yes_rsvp_count": 16,
            "updated": 1363358101000,
            "event_url": "http://www.meetup.com/python-lv/events/108519452/",
            "description": "Some event
 description",
            "headcount": 0,
            "name": "Ikmēneša saiets",
            "group": {
                "id": 3889622,
                "group_lat": 56.970001220703125,
                "name": "Python User Group Latvia",
                "group_lon": 24.1299991607666,
                "join_mode": "open",
                "urlname": "python-lv",
                "who": "Members"
            }
        }
    ],
"meta": {
    "lon": "",
    "count": 1,
    "signed_url": "http://api.meetup.com/2/events?status=upcoming&_=1363638434013&order=time&limited_events=False&group_urlname=python-lv&desc=false&offset=0&callback=jQuery171031021942128427327_1363638360545&format=json&page=1&fields=&sig_id=13802288&sig=1d45d6aa313a46a69e97f7aca5c1a837413ee880",
    "link": "https://api.meetup.com/2/events",
    "next": "https://api.meetup.com/2/events?key=3b6a2c23416b587c54452c2f75263830&status=upcoming&_=1363638434013&order=time&limited_events=False&group_urlname=python-lv&desc=false&offset=1&callback=jQuery171031021942128427327_1363638360545&format=json&page=1&fields=&sign=true",
    "total_count": 13,
    "url": "https://api.meetup.com/2/events?key=3b6a2c23416b587c54452c2f75263830&status=upcoming&_=1363638434013&order=time&limited_events=False&group_urlname=python-lv&desc=false&offset=0&callback=jQuery171031021942128427327_1363638360545&format=json&page=1&fields=&sign=true",
    "id": "",
    "title": "Meetup Events v2",
    "updated": 1363358101000,
    "description": "Access Meetup events using a group, member, or event id. Events in private groups are available only to authenticated members of those groups. To search events by topic or location, see [Open Events](/meetup_api/docs/2/open_events).",
    "method": "Events",
    "lat": ""
    }
}
"""

if __name__ == '__main__':
    unittest.main()
