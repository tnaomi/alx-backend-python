#!/usr/bin/env python3
""" 4. The basics of async """

import asyncio
import random
from typing import List

task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """
    spawn task_wait_random n times with the specified max_delay.
    """
    queue, result_array = [], []

    for _ in range(n):
        queue.append(task_wait_random(max_delay))

    for Q in asyncio.as_completed(queue):
        result = await Q
        result_array.append(result)

    return result_array
