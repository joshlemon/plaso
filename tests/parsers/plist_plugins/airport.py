#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the airport plist plugin."""

import unittest

# pylint: disable=unused-import
from plaso.formatters import plist as plist_formatter
from plaso.parsers import plist
from plaso.parsers.plist_plugins import airport

from tests.parsers.plist_plugins import test_lib


class AirportPluginTest(test_lib.PlistPluginTestCase):
  """Tests for the airport plist plugin."""

  def setUp(self):
    """Sets up the needed objects used throughout the test."""
    self._plugin = airport.AirportPlugin()
    self._parser = plist.PlistParser()

  def testProcess(self):
    """Tests the Process function."""
    plist_name = u'com.apple.airport.preferences.plist'
    event_queue_consumer = self._ParsePlistFileWithPlugin(
        self._parser, self._plugin, [plist_name], plist_name)
    event_objects = self._GetEventObjectsFromQueue(event_queue_consumer)

    self.assertEqual(len(event_objects), 4)

    timestamps = []
    for event_object in event_objects:
      timestamps.append(event_object.timestamp)
    expected_timestamps = frozenset([
        1375144166000000, 1386874984000000, 1386949546000000,
        1386950747000000])
    self.assertTrue(set(timestamps) == expected_timestamps)

    event_object = event_objects[0]
    self.assertEqual(event_object.key, u'item')
    self.assertEqual(event_object.root, u'/RememberedNetworks')
    expected_desc = (
        u'[WiFi] Connected to network: <europa> using security '
        u'WPA/WPA2 Personal')
    self.assertEqual(event_object.desc, expected_desc)
    expected_string = u'/RememberedNetworks/item {0:s}'.format(expected_desc)
    expected_short = expected_string[:77] + u'...'
    self._TestGetMessageStrings(
        event_object, expected_string, expected_short)


if __name__ == '__main__':
  unittest.main()