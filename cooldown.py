import asyncio
from random import gauss


class Cooldown:
    """
    The Cooldown class introduces a flexible delay between actions, which can be static or dynamic. For dynamic
    delays, a Gaussian distribution is used, leading to varying delay periods, with a 5% chance that the delay falls
    outside the provided range. However, a maximum limit of 1 hour is enforced to prevent excessively long delays.
    """

    def __init__(self):
        # Default values for min and max timeout if not initialized
        self.min = None
        self.max = None
        self.wait_time_limit = 3600

    async def initialize(self, min_timeout: int or float = None, max_timeout: int or float = None):
        """
        Introduces a delay based on the specified min and max timeout values.
        The delay will be dynamic, following a Gaussian distribution.
        If the delay exceeds 1 hour, it will be capped.

        Initialize the cooldown with specific minimum and maximum timeout values.

                Args:
                    min_timeout (int or float): The minimum timeout value.
                    max_timeout (int or float): The maximum timeout value.

        """
        if min_timeout is None and max_timeout is None:
            self.min, self.max = 0.1, 5
        elif min_timeout is not None and max_timeout is None:
            self.min = self.max = min_timeout
        elif min_timeout is not None and max_timeout is not None:
            self.min, self.max = min_timeout, max_timeout
        else:
            raise ValueError('Invalid cooldown values')

        if self.min is None or self.max is None:
            raise ValueError('Cooldown not initialized. Please call initialize() first.')

        if self.min == self.max:
            await asyncio.sleep(self.min)
            return self.min
        else:
            while True:
                mean = (self.max + self.min) / 2.0
                sigma = (self.max - self.min) / 4.0
                wait_time = gauss(mean, sigma)

                if wait_time > self.wait_time_limit:
                    wait_time = self.wait_time_limit

                if wait_time >= 0:
                    await asyncio.sleep(wait_time)
                    return wait_time
