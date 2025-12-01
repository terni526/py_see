import unittest

from main import main


class TestMain(unittest.TestCase):
    def test_main(self):
        try:
            main()
        except Exception as error:
            self.fail(f"Exception occurred: {error}")

if __name__ == "__main__":
    unittest.main()
