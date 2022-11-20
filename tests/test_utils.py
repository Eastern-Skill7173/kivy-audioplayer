import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

import unittest  # NOQA
from kivy_audioplayer import _utils  # NOQA


class TestUtils(unittest.TestCase):

    def test_humanize_duration(self):
        ten_seconds = 10
        two_minutes = 60 * 2
        two_minutes_thirty_seconds = 60 * 2 + 30
        one_hour = 60 * 60
        self.assertEqual(
            _utils.humanize_duration(ten_seconds),
            "0:10"
        )
        self.assertEqual(
            _utils.humanize_duration(two_minutes),
            "2:00"
        )
        self.assertEqual(
            _utils.humanize_duration(two_minutes_thirty_seconds),
            "2:30"
        )
        self.assertEqual(_utils.humanize_duration(one_hour), "1:00:00")
        self.assertEqual(
            _utils.humanize_duration(ten_seconds, False),
            "0:00:10"
        )
        self.assertEqual(
            _utils.humanize_duration(two_minutes, False),
            "0:02:00"
        )
        self.assertEqual(
            _utils.humanize_duration(two_minutes_thirty_seconds, False),
            "0:02:30"
        )
        self.assertEqual(
            _utils.humanize_duration(one_hour, False),
            "1:00:00"
        )

    def test_normalize_index(self):
        test_array = [0, 1, 2]
        self.assertEqual(_utils.normalize_index(test_array, 0), 0)
        self.assertEqual(_utils.normalize_index(test_array, 1), 1)
        self.assertEqual(_utils.normalize_index(test_array, 2), 2)
        self.assertEqual(_utils.normalize_index(test_array, -1), 2)
        self.assertEqual(_utils.normalize_index(test_array, -2), 1)
        self.assertEqual(_utils.normalize_index(test_array, -3), 0)
        with self.assertRaises(IndexError):
            _utils.normalize_index(test_array, 3)
            _utils.normalize_index(test_array, -4)


if __name__ == "__main__":
    unittest.main()
