import schedule
import asyncio
import random
from datetime import datetime
import pytz


class Scheduler:
    def __init__(self, synthenium):
        self.synthenium = synthenium
        self.next_run: datetime | None = None
        self.is_running = False

        self.albanian_tz = pytz.timezone('Europe/Tirane')
        self.weekend_days = {5, 6}

    @staticmethod
    async def run_pending():
        schedule.run_pending()

    async def clear_pending(self):
        schedule.clear()
        self.next_run = None

    async def __execute_function(self, func, *args, **kwargs):
        """Execute the provided async function with arguments."""
        try:
            self.is_running = True

            await func(*args, **kwargs)

            await self.synthenium.log(
                log_type='Success',
                website='Root',
                module='Orchestrator',
                message=f'Forumizer operated successfully'
            )
        except Exception as e:
            await self.synthenium.log(
                log_type='Error',
                website='Root',
                module='Orchestrator',
                message=f'Error while executing Forumizer: {e}'
            )

        self.is_running = False
        return True

    def __schedule(self, start_hour: int, stop_hour: int) -> datetime:
        """Generate a random time between start_hour and stop_hour."""
        hour = random.randint(start_hour, stop_hour)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        microsecond = random.randint(0, 59)

        random_time = datetime.now(self.albanian_tz).replace(
            hour=hour,
            minute=minute,
            second=second,
            microsecond=microsecond
        )

        self.next_run = random_time

        return random_time

    @staticmethod
    def __async_wrapper(coro):
        """Wrapper to handle async coroutines in schedule."""
        asyncio.create_task(coro)

    def __add_schedule(self, start_hour: int, stop_hour: int, func, *args, **kwargs):
        """Add a schedule for the bot."""
        schedule_time = self.__schedule(start_hour, stop_hour).strftime('%H:%M:%S')
        schedule.every().day.at(schedule_time).do(
            lambda: self.__async_wrapper(self.__execute_function(func, *args, **kwargs))
        )

    async def daily_scheduler(self, start_hour: int, stop_hour: int, func, *args, **kwargs):
        """
        Add a schedule, respecting weekend rules.
        :param start_hour: Start of the time range.
        :param stop_hour: End of the time range.
        :param func: The async function to execute.
        :param args: Positional arguments for the function.
        :param kwargs: Keyword arguments for the function.
        """
        schedule.clear()
        self.next_run = None

        if datetime.now(self.albanian_tz).weekday() in self.weekend_days:
            if random.random() < 0.75:
                self.__add_schedule(start_hour, stop_hour, func, *args, **kwargs)
            else:
                await self.synthenium.log(
                    log_type='Information',
                    website='Root',
                    module='Orchestrator',
                    message='Scheduler operations deferred due to weekend'
                )
        else:
            self.__add_schedule(start_hour, stop_hour, func, *args, **kwargs)
