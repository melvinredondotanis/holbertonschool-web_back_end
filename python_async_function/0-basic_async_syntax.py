#!/usr/bin/env python3
""" Coroutine at the same time witha sync """

import random
import asyncio


async def wait_random(max_delay: int = 10) -> float:
    """
        Args:
            max_delay: max wait
        Return:
            float time random
    """
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(max_delay)
    return delay
