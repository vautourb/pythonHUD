0
"""Tests for the geocolocation module."""

import responses

import googlemaps

import unittest
import codecs

from urllib.parse import urlparse, parse_qsl


class TestCase(unittest.TestCase):
    def assertURLEqual(self, first, second, msg=None):
        """Check that two arguments are equivalent URLs. Ignores the order of
        query arguments.
        """
        first_parsed = urlparse(first)
        second_parsed = urlparse(second)
        self.assertEqual(first_parsed[:3], second_parsed[:3], msg)

        first_qsl = sorted(parse_qsl(first_parsed.query))
        second_qsl = sorted(parse_qsl(second_parsed.query))
        self.assertEqual(first_qsl, second_qsl, msg)

    def u(self, string):
        """Create a unicode string, compatible across all versions of Python."""
        # NOTE(cbro): Python 3-3.2 does not have the u'' syntax.
        return codecs.unicode_escape_decode(string)[0]

class GeolocationTest(TestCase):
    def setUp(self):
        self.key = "AIzaSyAXyjUTd63knxXyHIpFhCuacMlUjIKwBos"
        self.client = googlemaps.Client(self.key)

    @responses.activate
    def test_simple_geolocate(self):
        responses.add(
            responses.POST,
            "https://www.googleapis.com/geolocation/v1/geolocate",
            body='{"location": {"lat": 51.0,"lng": -0.1},"accuracy": 1200.4}',
            status=200,
            content_type="application/json",
        )

        results = self.client.geolocate()

        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            "https://www.googleapis.com/geolocation/v1/geolocate?" "key=%s" % self.key,
            responses.calls[0].request.url,
        )