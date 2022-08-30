import functools
import asyncio


def run_in_executor(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return loop.run_in_executor(None, lambda: func(*args, **kwargs))
    return inner
