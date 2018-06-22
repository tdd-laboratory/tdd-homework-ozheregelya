import unittest
import library

NUM_CORPUS = '''
On the 5th of May every year, Mexicans celebrate Cinco de Mayo. This tradition
began in 1845 (the twenty-second anniversary of the Mexican Revolution), and
is the 1st example of a national independence holiday becoming popular in the
Western Hemisphere. (The Fourth of July didn't see regular celebration in the
US until 15-20 years later.) It is celebrated by 77.9% of the population--
trending toward 80.                                                                
'''

class TestCase(unittest.TestCase):

    # Helper function
    def assert_extract(self, text, extractors, *expected):
        actual = [x[1].group(0) for x in library.scan(text, extractors)]
        self.assertEquals(str(actual), str([x for x in expected]))

    # First unit test; prove that if we scan NUM_CORPUS looking for mixed_ordinals,
    # we find "5th" and "1st".
    def test_mixed_ordinals(self):
        self.assert_extract(NUM_CORPUS, library.mixed_ordinals, '5th', '1st')

    # Second unit test; prove that if we look for integers, we find four of them.
    def test_integers(self):
        self.assert_extract(NUM_CORPUS, library.integers, '1845', '15', '20', '80')

    # Third unit test; prove that if we look for integers where there are none, we get no results.
    def test_no_integers(self):
        self.assert_extract("no integers", library.integers)
    
    def test_date(self):
        self.assert_extract('I was born on 2015-07-25.', library.dates_iso8601, '2015-07-25')

    def test_invalid_month(self):
        self.assert_extract('I was born on 2015-13-25.', library.dates_iso8601)

    def test_dates_fmt2(self):
        self.assert_extract('I was born on 25 Jan 2017.', library.dates_fmt2, '25 Jan 2017')
#1
    def test_date_time_full(self):
        self.assert_extract('Today is 2015-07-25 18:22:19.123.', library.dates_iso8601, '2015-07-25 18:22:19.123')
#2 
    def test_date_time_delimeter(self):
        self.assert_extract('Today is 2015-07-25T18:22:19.123.', library.dates_iso8601, '2015-07-25T18:22:19.123')
#3
    def test_date_time_no_msec(self):
        self.assert_extract('Today is 2015-07-25 18:22:19.', library.dates_iso8601, '2015-07-25 18:22:19')
#4
    def test_date_time_no_sec(self):
        self.assert_extract('Today is 2015-07-25 18:22:19.', library.dates_iso8601, '2015-07-25 18:22')
#5
    def test_date_time_no_min(self):
        self.assert_extract('Today is 2015-07-25 18:22.', library.dates_iso8601, '2015-07-25 18:22')
#6
    def test_date_time_timezone_long(self):
        self.assert_extract('Today is 2015-07-25T18:22:19.123MDT.', library.dates_iso8601, '2015-07-25 18:22:19.123MDT')
#7
    def test_date_time_timezone_short(self):
        self.assert_extract('Today is 2015-07-25 18:22:19Z.', library.dates_iso8601, '2015-07-25 18:22:19Z')
#8
    def test_date_time_timezone_negative_offset(self):
        self.assert_extract('Today is 2015-07-25 18:22:19.123-0800.', library.dates_iso8601, '2015-07-25 18:22:123-0800')
#8
    def test_date_time_timezone_positive_offset(self):
        self.assert_extract('Today is 2015-07-25 18:22+0200.', library.dates_iso8601, '2015-07-25 18:22-0800')
#9
    def test_date_time_not_a_timezone(self):
        self.assert_extract('Today is 2015-07-25 18:22:19QWERTY.', library.dates_iso8601, '2015-07-25 18:22:19')
#10
    def test_dates_fmt2_comma(self):
        self.assert_extract('I was born on 25 Jan, 2017.', library.dates_fmt2, '25 Jan, 2017')

if __name__ == '__main__':
    unittest.main()
