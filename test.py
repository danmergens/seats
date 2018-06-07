import unittest
import requests
from seats import events, get_events, create_event, get_seats, create_seat


class EventTests(unittest.TestCase):
    """
    Integration Tests - must run the server before these can be run
    """

    def setUp(self):
        self.host = 'http://localhost:5000'
        self.response = None

    def url(self, endpoint):
        return self.host + endpoint

    def post(self, endpoint, json=None):
        if json:
            return requests.post(self.url(endpoint), json=json)
        return requests.post(self.url(endpoint))

    def get(self, endpoint, json=None):
        if json:
            return requests.get(self.url(endpoint), json=json)
        return requests.get(self.url(endpoint))

    @staticmethod
    def valid_response(r):
        return r.status_code == requests.codes.ok

    # These are progressive tests and must be run in the following order.
    def test_a_no_events(self):
        # when there are no events loaded:

        # the events return should be an empty list
        r = self.get('/events')
        self.assertTrue(self.valid_response(r))
        self.assertListEqual(r.json(), [])

        # and attempts to access an event id should fail
        r = self.get('/events/1')
        self.assertFalse(self.valid_response(r))
        r = self.get('/events/1/seats')
        self.assertFalse(self.valid_response(r))

    def test_b_create_empty_event(self):
        empty_event = {u'event_id': 1, u'seats': []}
        # after creating an empty event:

        # the event id will exist, but the seats will be empty:
        r = self.post('/events')
        self.assertTrue(self.valid_response(r))
        self.assertDictEqual(r.json(), empty_event)

        # the same event will be available through the GET interface
        r = self.get('/events/1')
        self.assertDictEqual(r.json(), empty_event)

        # one event id will be returned
        r = self.get('/events')
        self.assertTrue(self.valid_response(r))
        self.assertListEqual(r.json(), [empty_event['event_id']])

    def test_c_create_seats(self):
        def create_seat(event_id, seat_id, seat_type, aisle, available):
            return self.post('/events/%d/seats/%d' % (event_id, seat_id),
                             json={'type': seat_type, 'aisle': aisle, 'available': available})

        def assertSeatCreated(event_id, seat_id, seat_type, aisle, available):
            r = create_seat(event_id, seat_id, seat_type, aisle, available)
            self.assertTrue(self.valid_response(r))
            expected = {'seat_id': str(seat_id), 'type': seat_type, 'aisle': aisle, 'available': available}
            self.assertDictEqual(r.json(), expected)

        assertSeatCreated(event_id=1, seat_id=1, seat_type='adult', aisle=True, available=False)
        assertSeatCreated(event_id=1, seat_id=2, seat_type='adult', aisle=True, available=True)
        assertSeatCreated(event_id=1, seat_id=3, seat_type='adult', aisle=False, available=False)
        assertSeatCreated(event_id=1, seat_id=4, seat_type='adult', aisle=False, available=True)
        assertSeatCreated(event_id=1, seat_id=5, seat_type='child', aisle=True, available=False)
        assertSeatCreated(event_id=1, seat_id=6, seat_type='child', aisle=True, available=True)
        assertSeatCreated(event_id=1, seat_id=7, seat_type='child', aisle=False, available=False)
        assertSeatCreated(event_id=1, seat_id=8, seat_type='child', aisle=False, available=True)

        # a total of 8 seats were created
        r = self.get('/events/1/seats')
        self.assertTrue(self.valid_response(r))
        self.assertEqual(len(r.json()), 8)

        # four seats should be available:
        r = self.get('/events/1/seats', json={'available': True})
        self.assertTrue(self.valid_response(r))
        self.assertEqual(len(r.json()), 4)
        self.assertListEqual(r.json(), [u'2', u'4', u'6', u'8'])

        # filtering will return expected results, e.g. one available non-aisle, child seat (8)
        r = self.get('/events/1/seats', json={'type': 'child', 'aisle': False})
        self.assertTrue(self.valid_response(r))
        self.assertListEqual(r.json(), ['8'])

