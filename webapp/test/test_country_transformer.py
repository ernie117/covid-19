import unittest

from webapp.mongo import transform


class MyTestCase(unittest.TestCase):

    def test_returns_china(self):
        self.assertEqual(transform.transform_country("mainland china"), "China")

    def test_returns_united_kingdom(self):
        self.assertEqual(transform.transform_country("uk"), "United Kingdom")

    def test_returns_united_states(self):
        self.assertEqual(transform.transform_country("us"), "United States")


if __name__ == '__main__':
    unittest.main()
