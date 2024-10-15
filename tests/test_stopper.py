import unittest
from modules.stopper import stopper

class TestUnpackSpeed(unittest.IsolatedAsyncioTestCase):
    """
    Stopper modul működőképességét tesztelő tesztek.
    """

    async def test(self) -> None:
        """
        Jelenleg még csak skeleton teszt, ami majd az unpack idejét nézi.
        """
        target: float = 1 # milisec

        # Adding the time to run the stopper to the target.
        async def null() -> None: pass
        stopper_imperfection = await stopper(null)
        target += stopper_imperfection

        async def wrapper() -> None:
            pass # Unpack here

        delta: float = await stopper(wrapper)
        self.assertLess(delta, target)

if __name__ == "__main__":
    unittest.main()