"""
Storage modul tesztek.
"""

import unittest
from unittest.mock import patch
from modules.storage import Storage

class TestByteSlicer(unittest.TestCase):
	"""
	Storage modul működőképességét tesztelő tesztek.
	"""

	async def setUp(self) -> None:
		self.storage = Storage()

	async def test_read_single_valid(self) -> None:
		"""
		Storage modul írás olvasás tesztelése sikeres körülmények között. Egy mély szinten.
		"""
		
		data = "érték"
		key = "single_level"

		self.storage.write([key], data)
		result = self.storage.read([key])

		self.assertEqual(data, result)
		self.assertEqual(self.storage.dict[key], result)

	async def test_read_multiple_valid(self) -> None:
		"""
		Storage modul írás olvasás tesztelése sikeres körülmények között. Több szint mélyen.
		"""

		data = "érték"
		keys = ["level1", "level2"]

		self.storage.write(keys, data)
		result = self.storage.read(keys)

		self.assertEqual(data, result)
	
	async def test_read_single_fallback(self) -> None:
		"""
		Storage modul írás olvasás tesztelése üres érték lekérdezésével.
		"""
		
		keys = ["single_level"]
		fallback = 12
		result = self.storage.read(keys, fallback=fallback)

		self.assertEqual(fallback, result)

if __name__ == "__main__":
	unittest.main()