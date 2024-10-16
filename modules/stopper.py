"""
Stopper modul megadott callback függvény lefutási idejének méréséhez.
A visszatérített érték miliszekundumban van.
"""
import time

async def stopper(callback) -> float:
    """
    Stopper függvény megadott callback függvény lefutási idejének méréséhez.
    A visszatérített érték miliszekundumban van.
    """
    start = time.perf_counter()
    await callback()
    end = time.perf_counter()
    
    return (end - start) * 1000  # Return time in milliseconds