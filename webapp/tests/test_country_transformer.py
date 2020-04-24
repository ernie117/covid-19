import unittest

from webapp.data.transformation.country_transformer import CountryTransformer


class TestCountryTransformer(unittest.TestCase):
    def test_transform_returns_china(self):
        self.assertEqual(CountryTransformer.transform("Mainland China"), "China")

    def test_transform_returns_united_kingdom(self):
        self.assertEqual(CountryTransformer.transform("uk"), "United Kingdom")

    def test_transform_returns_united_states(self):
        self.assertEqual(CountryTransformer.transform("us"), "United States")

    def test_transform_returns_congo_1(self):
        self.assertEqual(CountryTransformer.transform("congo (brazzaville)"), "Congo")

    def test_transform_returns_congo_2(self):
        self.assertEqual(CountryTransformer.transform("congo (kinshasa)"), "Congo")

    def test_transform_returns_congo_3(self):
        self.assertEqual(CountryTransformer.transform("Republic of The Congo"), "Congo")

    def test_transform_returns_vietnam(self):
        self.assertEqual(CountryTransformer.transform("viet nam"), "Vietnam")


if __name__ == "__main__":
    unittest.main()
