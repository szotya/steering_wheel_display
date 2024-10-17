"""
Stopper modul tesztek.
"""

import unittest
import asyncio
from modules.stopper import stopper

class TestUnpackSpeed(unittest.IsolatedAsyncioTestCase):
    """
    Stopper modul működőképességét tesztelő tesztek.
    """

    async def test_valid(self) -> None:
        """
        Stopper tesztelése azonnali visszatérésű fügvénnyel.
        """

        async def null() -> None: pass
        delta = await stopper(null)

        self.assertLess(delta, 10)

    async def test_fail(self) -> None:
        """
        Stopper tesztelése várakozásos visszatérésű fügvénnyel.
        """

        wait_time = 1 # in seconds

        async def async_mock() -> None: await asyncio.sleep(wait_time)
        delta = await stopper(async_mock)

        self.assertGreaterEqual(delta, wait_time)

if __name__ == "__main__":
    unittest.main()