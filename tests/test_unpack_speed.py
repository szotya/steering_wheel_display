import unittest
import time
from modules.stopper import stopper

class TestUnpackSpeed(unittest.TestCase):
    """
    Csomagok kicsomagolásának idejét mérő teszt. Sikeres, ha adott időn belül csomagol ki egy üzenetet.
    """

    def test(self):
        target: float = 1.5 # milisec

        def wrapper() -> None:
            time.sleep(1)

        delta: float = stopper()
        self.assertTrue(delta <= float)