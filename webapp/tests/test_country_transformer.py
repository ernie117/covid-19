import unittest

from webapp.data.transformation.country_transformer import CountryTransformer


class TestCountryTransformer(unittest.TestCase):

    def test_transform_returns_china(self):
        t = CountryTransformer("Mainland China").transform()
        self.assertEqual(t, "China")

    def test_transform_returns_united_kingdom(self):
        t = CountryTransformer("uk").transform()
        self.assertEqual(t, "United Kingdom")

    def test_transform_returns_united_states(self):
        t = CountryTransformer("us").transform()
        self.assertEqual(t, "United States")

    def test_transform_returns_congo_1(self):
        t = CountryTransformer("congo (brazzaville)").transform()
        self.assertEqual(t, "Congo")

    def test_transform_returns_congo_2(self):
        t = CountryTransformer("congo (kinshasa)").transform()
        self.assertEqual(t, "Congo")

    def test_transform_returns_congo_3(self):
        t = CountryTransformer("Republic of The Congo").transform()
        self.assertEqual(t, "Congo")

    def test_transform_returns_vietnam(self):
        t = CountryTransformer("viet nam").transform()
        self.assertEqual(t, "vietnam")


if __name__ == '__main__':
    unittest.main()
